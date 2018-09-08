import re
from urllib.parse import urlparse, urljoin

ABSOLUTE_URL_RE = re.compile(r"^https?://", re.IGNORECASE)


def is_absolute_url(url):
    return bool(ABSOLUTE_URL_RE.match(url))


def normalise_url(url, base_path=None):
    if url.startswith("www."):
        url = "http://" + url

    if base_path is not None and not is_absolute_url(url):
        url = urljoin(base_path, url)

    return Url(url)


class Url(str):
    # noinspection PyArgumentList
    def __new__(cls, url):
        parsed_url = urlparse(url)
        scheme = None

        rewritten_url = ""
        if parsed_url.netloc:
            scheme = parsed_url.scheme or "http"

            rewritten_url += scheme + "://"
            rewritten_url += parsed_url.netloc.lower()

        rewritten_url += parsed_url.path
        if parsed_url.query:
            rewritten_url += "?" + parsed_url.query

        type_ = super().__new__(cls, rewritten_url)

        type_.scheme = scheme
        type_.netloc = parsed_url.netloc
        type_.path = parsed_url.path
        type_.query = parsed_url.query

        return type_


class UrlStorage:
    def __init__(self):
        self._urls = []
        self._local_path = {}

    def __iter__(self):
        index = 0

        while index < len(self._urls):
            yield self._urls[index]
            index += 1

    def clean(self):
        self._urls.clear()
        self._local_path.clear()

    def push(self, url):
        if not isinstance(url, Url):
            url = normalise_url(url)

        if url not in self._urls:
            self._urls.append(url)

    def set_local_path(self, url, local_path):
        self._local_path[url] = local_path

    def get_local_path(self, url):
        return self._local_path[url]

    def get_url_from_local_path(self, destination):
        urls = []

        for url, target in self._local_path.items():
            if target == destination:
                urls.append(url)

        if not urls:
            raise KeyError(destination)

        return max(urls, key=lambda x: len(x))
