import time
import argparse
import threading
import http.server
import socketserver

from functools import partial
from pathlib import Path

from flingern import website
from flingern import watchdog
from flingern import defs

version = "0.1"
header = f"flingern {version}"
port = 8089

def run_webserver(path):
    class ReusableTCPServer(socketserver.TCPServer):
        allow_reuse_address = True

    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(path))
    httpd = ReusableTCPServer(("", port), handler)
    print("Serving at port", port)
    httpd.serve_forever()

def main(): 
    print(defs.FLINGERN_HEADER.format(version))

    parser = argparse.ArgumentParser(description=header)
    parser.add_argument("path", help="build the website specified by path")
    parser.add_argument('-w', '--watch', help='creates a webserver and watches for changes', action='store_true')
    parser.add_argument('-f', '--force', help='force rebuild; that will rebuild whole site from scratch', action='store_true')
    args = parser.parse_args()

    defs.flingern_directory = Path(__file__).parent.resolve()
    
    project_path = Path(args.path)
    site = website.FlingernWebsite(project_path, args.force)
    site.build()

    if args.watch:
        # create webserver
        public_dir = project_path / "public"
        t = threading.Thread(target=run_webserver, args=(public_dir,), daemon=True)
        t.start()

        # build lock to prevent concurrent builds from multiple watchers
        build_lock = threading.Lock()

        def safe_build():
            with build_lock:
                print("\nRebuilding site...")
                site.build()

        # create watchdog
        watchdog_site = watchdog.watchdog_at(project_path, safe_build)
        watchdog_theme = watchdog.watchdog_at(defs.flingern_directory / defs.DIR_THEME, safe_build)

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            watchdog_site.stop()
            watchdog_theme.stop()
            watchdog_site.join()
            watchdog_theme.join()

if __name__ == '__main__':
    main()
