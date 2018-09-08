import logging
import os
import requests
import shutil
import string
from urllib.parse import urlparse

from .files import get_file_handler
from .urls import UrlStorage, normalise_url

LEGAL_FILENAME_CHAR = "-_.() %s%s" % (string.ascii_letters, string.digits)


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def legalise_name(name):
    return ''.join(c for c in name if c in LEGAL_FILENAME_CHAR).lower()


class Grabber:
    def __init__(self, base_url="http://www.codeskulptor.org"):
        self.base_url = normalise_url(base_url)
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "Mozilla/5.0 Chrome/68.0.3440.106 Safari/537.36"

        self.urls = UrlStorage()
        self.base_target = None
        self._pending_files = []

    def grab(self, target, clean=False):
        if clean and os.path.exists(target):
            shutil.rmtree(target)

        self.base_target = target
        ensure_directory(target)

        self.urls.clean()
        self._pending_files.clear()

        start_url = self.base_url
        if start_url[-1] != "/":
            start_url += "/"

        self.urls.push(start_url)

        counter = 0
        for url in self.urls:
            counter += 1
            file_content = self.download(url)
            if file_content is not None:
                for href in file_content.crawl():
                    self.urls.push(href)

                self._pending_files.append(file_content)

            if counter % 50 == 0:
                self.try_commit()

        self.try_commit(force=True)

    def try_commit(self, force=False):
        index = 0
        while index < len(self._pending_files):
            file_content = self._pending_files[index]
            if force or not file_content.has_pending_dependencies():
                self._pending_files.pop(index)
                file_content.write()
            else:
                index += 1

    def download(self, url):
        logging.error("GET: %s" % url)

        try:
            response = self.session.get(url, stream=True)
        except Exception:
            logging.exception("GET: %s failed" % url)
            return

        destination = self._suggest_destination(response.url)
        if response.url != url:  # Handle redirect
            self.urls.set_local_path(url, destination)
            url = normalise_url(response.url)

        extension = os.path.splitext(destination)[-1]
        file_handler_class = get_file_handler(extension)

        self.urls.set_local_path(url, destination)
        touch(destination)
        if file_handler_class is not None:
            return file_handler_class(url, destination, response.text, self)

        with open(destination, "wb") as out:
            for block in response.iter_content(1024):
                out.write(block)

    def _suggest_destination(self, url):
        directories = []

        if url.startswith(self.base_url):
            url = url.replace(self.base_url, "")

        parsed_url = urlparse(url)
        if parsed_url.netloc:
            directories.append(legalise_name(parsed_url.netloc))

        for p in parsed_url.path.lstrip("/").split("/"):
            p = legalise_name(p)
            if p:
                directories.append(p)

        filename = "index.html" if url.endswith("/") else directories.pop(-1)
        filename, extension = os.path.splitext(filename)

        owner_directory = os.path.join(self.base_target, *directories)
        os.makedirs(owner_directory, exist_ok=True)

        if parsed_url.query:
            filename += legalise_name(parsed_url.query)

        suggested_path = "%s/%s%s" % (owner_directory, filename, extension)
        counter = 0
        while os.path.exists(suggested_path):
            suggested_path = "%s/%s_%s%s" % (owner_directory, filename, counter, extension)
            counter += 1

        return suggested_path
