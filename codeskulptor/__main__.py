import logging

import click

from codeskulptor import __version__, DEFAULT_HOST, DEFAULT_PY2_PORT, DEFAULT_PY3_PORT
from codeskulptor import logger, interface


@click.group()
@click.option('--version', is_flag=True)
@click.option('-v', '--verbose', count=True, default=1, help="Increase verbosity")
def cli(verbose, version):
    """
    Unofficial CodeSkulptor Local Server
    """
    if version:
        print(__version__)
        exit(0)

    print("Unofficial CodeSkulptor Local Server (version %s)" % __version__)
    print("For further details and issue reporting please visit https://github.com/uadnan/CodeSkulptor")
    print()

    if verbose >= 2:
        logger.setLevel(logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)


@cli.command()
@click.option('-p', '--port', type=click.IntRange(1, 65534), help='Optional server port number')
@click.option('-h', '--host', default=DEFAULT_HOST, show_default=True,
              help='Optional server host address')
@click.option('--browser/--no-browser', default=True, show_default=True,
              help='Open browser automatically after launching the server')
@click.option('-c', '--codeskulptor', type=click.Choice(["py2", "py3"]), default="py2", show_default=True,
              help='Codeskulptor version to use')
def runserver(host, port, codeskulptor, browser):
    """
    Starts a lightweight Web server for CodeSkulptor and also serves static files.
    """
    if port is None:
        port = DEFAULT_PY2_PORT if codeskulptor == "py2" else DEFAULT_PY3_PORT

    interface.run_server((host, port), codeskulptor, browser)


@cli.command()
def grabber():
    """
    Grab fresh copy of http://www.codeskulptor.org and https://py3.codeskulptor.org
    """
    interface.run_grabber()


if __name__ == "__main__":
    cli()
