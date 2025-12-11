import time
from pathlib import Path
from typing import Callable, Union

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from flingern import defs


class WatchdogHandler(FileSystemEventHandler):
    def __init__(self, callback: Callable[[], None]):
        self.callback = callback
        self.last_call = 0.0

    def on_any_event(self, event):
        if time.time() - self.last_call < 3.0:
            return

        if event.event_type in ("created", "modified"):
            if defs.DIR_PUBLIC in event.src_path:
                return

            self.last_call = time.time()
            print("File %s: %s" % (event.event_type, event.src_path))
            self.callback()


def watchdog_at(path: Union[str, Path], callback: Callable[[], None]) -> Observer:
    path_str = str(path)

    event_handler = WatchdogHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, path_str, recursive=True)
    observer.start()
    print("Watching file changes within", path_str)

    return observer
