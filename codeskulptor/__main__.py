import argparse

from . import __version__, interface, DEFAULT_HOST, DEFAULT_PY3_PORT, DEFAULT_PY2_PORT


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


def parse_args():
    parser = argparse.ArgumentParser(
        description="CodeSkulptor Local Server (version %s)" % __version__,
        prog="codeskulptor",
    )

    subparsers = parser.add_subparsers(title="action", description="Action to perform")

    runserver = subparsers.add_parser(
        "runserver",
        help="Starts a lightweight Web server for CodeSkulptor and also serves static files.",
        usage='%(prog)s [options] ...'
    )
    runserver.add_argument(
        "address",
        nargs='?',
        type=validate_host,
        help="Optional port number, or ip:port",
        default=None
    )
    runserver.add_argument(
        "--version",
        choices=["2", "3"],
        help="Which version of CodeSkulptor to serve",
        required=False,
        default="2"
    )
    runserver.add_argument(
        "--no-browser",
        dest="open_browser",
        help="Don't automatically open Web browser",
        required=False,
        action="store_false",
        default=True
    )
    runserver.set_defaults(action="runserver")

    grabber = subparsers.add_parser(
        "grabber",
        help="Grab fresh copy of http://www.codeskulptor.org and https://py3.codeskulptor.org",
        usage='%(prog)s [options] ...'
    )
    grabber.add_argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Output logs while grabbing",
        default=False
    )
    grabber.set_defaults(action="grabber")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.action == "runserver":
        address = args.address
        if address is None:
            address = (DEFAULT_HOST, DEFAULT_PY2_PORT if args.version == 2 else DEFAULT_PY3_PORT)

        interface.run_server(address, args.version, args.open_browser)
    elif args.action == "grabber":
        interface.run_grabber(args.verbose)
