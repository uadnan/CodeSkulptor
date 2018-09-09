import argparse
import os
from pathlib import Path

from . import __version__
from .server import serve

parser = argparse.ArgumentParser(
    description="CodeSkulptor Local Server (version %s)" % __version__,
    prog="codeskulptor",
)


def validate_host(value):
    parts = value.split(":")

    if len(parts) == 1:
        host = DEFAULT_HOST
        port = parts[0]
    elif len(parts) == 2:
        host = parts[0]
        port = parts[1]
    else:
        raise argparse.ArgumentTypeError("Either provider port number or ip:port")

    if not port.isdigit():
        raise argparse.ArgumentTypeError("%s is not a valid port" % port)
    else:
        port = int(port)

    return host, port


DEFAULT_HOST = os.getenv("CODESKULPTOR_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.getenv("CODESKULPTOR_PORT", "9080"))

WWW_ROOT = os.path.join(os.path.dirname(__file__), "www")
LOCAL_WWW_ROOT = os.path.join(Path.home(), ".codeskulptor")

parser.add_argument(
    "address",
    nargs='?',
    type=validate_host,
    help="Optional port number, or ip:port",
    default=(DEFAULT_HOST, DEFAULT_PORT)
)

parser.add_argument(
    "--version",
    choices=["2", "3"],
    help="Which version of CodeSkulptor to serve",
    required=False,
    default="2"
)

parser.add_argument(
    "--download-again",
    dest="download_again",
    action="store_true",
    help="Download fresh copy of CodeSkulptor",
    default=False
)

parser.add_argument(
    "--no-local-www",
    dest="ignore_local_www",
    action="store_true",
    help="Don't serve local copy of www directory instead server www shipped with module",
    default=False
)

args = parser.parse_args()

print("""Unofficial CodeSkulptor Local Server (version {version})

For further details and issue reporting please visit https://github.com/uadnan/CodeSkulptor
""".format(
    version=__version__
))

if args.download_again:
    from .grabber import Grabber

    print("Downloading fresh copy of CodeSkulptor. This might take few moments, please be patient")

    # Grabber().grab(os.path.join(LOCAL_WWW_ROOT, "py2"), clean=True)
    Grabber(base_url="https://py3.codeskulptor.org").grab(os.path.join(LOCAL_WWW_ROOT, "py3"), clean=True)

    print("Download Completed")

www_root = WWW_ROOT
if os.path.exists(LOCAL_WWW_ROOT):
    if not args.ignore_local_www:
        www_root = LOCAL_WWW_ROOT
elif args.ignore_local_www:
    print("WARNING: There is no local copy of www directory. --no-local-www has no impact")

www_root = os.path.join(www_root, "py%s" % args.version)

print("""Starting CodeSkulptor server at http://{host}:{port}/
Serving from {directory}
Quit the server with CONTROL-C.""".format(
    host=args.address[0],
    port=args.address[1],
    directory=www_root
))
serve(args.address, www_root)
