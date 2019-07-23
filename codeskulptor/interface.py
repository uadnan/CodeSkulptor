import os
import zipfile

from codeskulptor import DEFAULT_HOST, DEFAULT_PY2_PORT, DEFAULT_PY3_PORT, WWW_ROOT, WWW_ROOT_ZIP
from codeskulptor import logger


def run_grabber():
    from codeskulptor.grabber import Grabber

    logger.info("Downloading fresh copy of CodeSkulptor from live site.")
    logger.info("This requires an active internet connection")
    logger.info("Please be patient while downloading as that might take few moments based on your internet connection")

    www_dir = os.path.join(WWW_ROOT, "py2")
    logger.info("Saving http://www.codeskulptor.org to %s..." % www_dir)
    Grabber("http://www.codeskulptor.org").grab(www_dir, clean=True)

    www_dir = os.path.join(WWW_ROOT, "py3")
    logger.info("Saving http://py3.codeskulptor.org to %s..." % www_dir)
    Grabber("http://py3.codeskulptor.org").grab(www_dir, clean=True)

    logger.info("\nAll Done!")


def run_server(address, version, open_browser=True):
    this_www = os.path.join(WWW_ROOT, version)

    if not os.path.exists(this_www) and os.path.exists(WWW_ROOT_ZIP):
        with zipfile.ZipFile(WWW_ROOT_ZIP, "r") as f:
            f.extractall(WWW_ROOT)

    logger.info("Starting CodeSkulptor server at http://%s:%s/" % address)
    logger.debug("Serving from %s" % this_www)
    logger.info("Quit the server with CONTROL-C.")

    from codeskulptor.server import serve

    serve(address, this_www, open_browser=open_browser)


def run_py2(host=DEFAULT_HOST, port=DEFAULT_PY2_PORT):
    run_server((host, port), version=2)


def run_py3(host=DEFAULT_HOST, port=DEFAULT_PY3_PORT):
    run_server((host, port), version=3)
