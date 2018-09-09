import os

from . import WWW_ROOT, LOCAL_WWW_ROOT, DEFAULT_HOST, DEFAULT_PY2_PORT, DEFAULT_PY3_PORT
from . import __version__


def run_grabber(verbose=False):
    from .grabber import Grabber

    print("Downloading fresh copy of CodeSkulptor from live site.")
    print("This requires an active internet connection")
    print("Please be patient while downloading as that might take few moments based on your internet connection")
    print("")

    www_dir = os.path.join(LOCAL_WWW_ROOT, "py2")
    print("Saving http://www.codeskulptor.org to %s..." % www_dir)
    Grabber("http://www.codeskulptor.org", verbose=verbose).grab(www_dir, clean=True)

    www_dir = os.path.join(LOCAL_WWW_ROOT, "py3")
    print("Saving http://py3.codeskulptor.org to %s..." % www_dir)
    Grabber("http://py3.codeskulptor.org", verbose=verbose).grab(www_dir, clean=True)

    print("\nAll Done!")


def run_server(address, version, ignore_local_www=False):
    print("""Unofficial CodeSkulptor Local Server (version {version})
    
    For further details and issue reporting please visit https://github.com/uadnan/CodeSkulptor
    """.format(
        version=__version__
    ))

    www_root = WWW_ROOT
    if os.path.exists(LOCAL_WWW_ROOT):
        if not ignore_local_www:
            www_root = LOCAL_WWW_ROOT
    elif ignore_local_www:
        print("WARNING: There is no local copy of www directory. --no-local-www has no impact")

    www_root = os.path.join(www_root, "py%s" % version)

    print("""Starting CodeSkulptor server at http://{host}:{port}/
    Serving from {directory}
    Quit the server with CONTROL-C.""".format(
        host=address[0],
        port=address[1],
        directory=www_root
    ))

    from .server import serve

    serve(address, www_root)


def run_py2():
    run_server((DEFAULT_HOST, DEFAULT_PY2_PORT), version=2)


def run_py3():
    run_server((DEFAULT_HOST, DEFAULT_PY3_PORT), version=3)
