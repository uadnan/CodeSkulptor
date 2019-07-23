import os
import shutil
import zipfile

from codeskulptor import DEFAULT_HOST, DEFAULT_PY2_PORT, DEFAULT_PY3_PORT, WWW_ROOT, WWW_ROOT_ZIP
from codeskulptor import logger


def archive_www():
    archive_path = os.path.join(WWW_ROOT, "www.zip")
    logger.info("Archiving grabbed files...")

    with zipfile.ZipFile(archive_path, "w") as zip_file:
        for codeskulptor_version in ("py2", "py3"):
            www_dir = os.path.join(WWW_ROOT, codeskulptor_version)

            for dir_path, _, files in os.walk(www_dir):
                for file_name in files:
                    file_path = os.path.join(dir_path, file_name)

                    dest_path = os.path.relpath(file_path, WWW_ROOT)
                    zip_file.write(file_path, dest_path)

    logger.info("Archived grabbed files to {}".format(archive_path))


def run_grabber(clean=False, archive=False):
    from codeskulptor.grabber import Grabber

    logger.info("Downloading fresh copy of CodeSkulptor from live site.")
    logger.info("This requires an active internet connection")
    logger.info("Please be patient while downloading as that might take few moments based on your internet connection")

    www_dir = os.path.join(WWW_ROOT, "py2")
    if clean:
        logger.info("Cleaning {}".format(www_dir))
        shutil.rmtree(www_dir)

    logger.info("Saving http://www.codeskulptor.org to %s..." % www_dir)
    Grabber("http://www.codeskulptor.org").grab(www_dir, clean=True)

    www_dir = os.path.join(WWW_ROOT, "py3")
    if clean:
        logger.info("Cleaning {}".format(www_dir))
        shutil.rmtree(www_dir)

    logger.info("Saving http://py3.codeskulptor.org to %s..." % www_dir)
    Grabber("http://py3.codeskulptor.org").grab(www_dir, clean=True)

    if archive:
        archive_www()

    logger.info("\nAll Done!")


def run_server(address, codeskulptor_version, open_browser=True):
    this_www = os.path.join(WWW_ROOT, codeskulptor_version)

    if not os.path.exists(this_www) and os.path.exists(WWW_ROOT_ZIP):
        with zipfile.ZipFile(WWW_ROOT_ZIP, "r") as f:
            f.extractall(WWW_ROOT)

    logger.info("Starting CodeSkulptor server at http://%s:%s/" % address)
    logger.debug("Serving from %s" % this_www)
    logger.info("Quit the server with CONTROL-C.")

    from codeskulptor.server import serve

    serve(address, this_www, open_browser=open_browser)


def run_py2(host=DEFAULT_HOST, port=DEFAULT_PY2_PORT):
    run_server((host, port), codeskulptor_version="py2")


def run_py3(host=DEFAULT_HOST, port=DEFAULT_PY3_PORT):
    run_server((host, port), codeskulptor_version="py3")
