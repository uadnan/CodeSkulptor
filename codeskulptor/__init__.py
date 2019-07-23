import logging
import os

__version__ = "0.1.1"
__author__ = "Adnan Umer <u.adnan@outlook.com>"

DEFAULT_HOST = os.getenv("CODESKULPTOR_HOST", "127.0.0.1")
DEFAULT_PY2_PORT = 9080
DEFAULT_PY3_PORT = 9081

USER_HOME = os.path.expanduser("~")
WWW_ROOT = os.path.join(USER_HOME, ".codeskulptor")
WWW_ROOT_ZIP = os.path.join(os.path.dirname(__file__), "www.zip")

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s - %(levelname)-8s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
