import os
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
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=path)
    httpd = socketserver.TCPServer(("", port), handler)
    print("Serving at port", port)
    httpd.serve_forever()

def main(): 
    print(defs.FLINGERN_HEADER.format(version))

    parser = argparse.ArgumentParser(description=header)
    parser.add_argument("path", help="build the website specified by path")
    parser.add_argument('-w', '--watch', help='creates a webserver and watches for changes', action='store_true')
    parser.add_argument('-f', '--force', help='force rebuild; that will rebuild whole site from scratch', action='store_true')
    args = parser.parse_args()

    defs.flingern_directory = Path(os.path.dirname( __file__)).absolute()
    
    site = website.FlingernWebsite(args.path, args.force)
    site.build()

    if args.watch:
        # create webserver
        t = threading.Thread(target=run_webserver, args=(os.path.join(".", args.path, "public/"),))
        t.start()

        # create watchdog
        watchdog_site = watchdog.watchdog_at(args.path)
        watchdog_theme = watchdog.watchdog_at(os.path.join(defs.flingern_directory, defs.DIR_THEME))

        try:
            while True:
                time.sleep(1)
                if watchdog.filesystem_changed:
                    watchdog.filesystem_changed = False
                    site.build()

        except KeyboardInterrupt:
            watchdog_site.stop()
            watchdog_theme.stop()

        t.join()

if __name__ == '__main__':
    main()
