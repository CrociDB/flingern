import argparse
import http.server
import socketserver
import sys
import threading
import time
from functools import partial
from pathlib import Path
from importlib.metadata import version, PackageNotFoundError

from flingern import defs, watchdog, website

def get_version():
    try:
        return version(__package__ or __name__)
    except PackageNotFoundError:
        return "0.0.0"

port = 8089


def run_webserver(path):
    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(path))
    httpd = ReusableTCPServer(("", port), handler)
    print("Serving at port", port)
    httpd.serve_forever()


def build(args):
    project_path = Path(args.path)
    site = website.FlingernWebsite(project_path, args.force)
    site.build()


def serve(args):
    project_path = Path(args.path)
    site = website.FlingernWebsite(project_path, args.force)
    site.build()

    # create webserver
    public_dir = project_path / defs.DIR_PUBLIC
    t = threading.Thread(target=run_webserver, args=(public_dir,), daemon=True)
    t.start()

    # build lock to prevent concurrent builds from multiple watchers
    build_lock = threading.Lock()

    # watch for changes?
    if args.watch:

        def safe_build():
            with build_lock:
                print("\nRebuilding site...")
                site.build()

        # create watchdog
        watchdog_site = watchdog.watchdog_at(project_path, safe_build)
        watchdog_theme = watchdog.watchdog_at(Path(defs.flingern_directory) / defs.DIR_THEME, safe_build)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            watchdog_site.stop()
            watchdog_theme.stop()
            watchdog_site.join()
            watchdog_theme.join()
    else:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    print("\nk bye")


# CLI Commands
def cmd_serve(args):
    serve(args)


def cmd_build(args):
    build(args)


def cmd_new(args):
    print(f"New command is not implemented yet. Target path: {args.path}")


def main():
    version_header = get_version()
    l = len(version_header)
    for _ in range(10 - l): version_header = version_header + " "

    print(defs.FLINGERN_HEADER.format(version_header))

    # set the flingern directory global definition
    defs.flingern_directory = Path(__file__).parent.resolve()

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True, help="sub-command help")

    # new
    parser_new = subparsers.add_parser("new", help="Create a new flingern project")
    parser_new.add_argument("path", help="Path where the new project should be created")
    parser_new.set_defaults(func=cmd_new)

    # build
    parser_build = subparsers.add_parser("build", help="Build the website")
    parser_build.add_argument("path", help="Path to the website")
    parser_build.add_argument(
        "-f",
        "--force",
        help="force rebuild the whole site",
        action="store_true",
    )
    parser_build.set_defaults(func=cmd_build)

    # serve
    parser_serve = subparsers.add_parser("serve", help="Build and serve the website")
    parser_serve.add_argument("path", help="Path to the website")
    parser_serve.add_argument(
        "-f",
        "--force",
        help="force rebuild the whole site",
        action="store_true",
    )
    parser_serve.add_argument("-w", "--watch", help="watches for changes", action="store_true")
    parser_serve.set_defaults(func=cmd_serve)

    # help
    parser_help = subparsers.add_parser("help", help="Show this help message")
    parser_help.set_defaults(func=lambda _: parser.print_help())

    # if no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
