import time
from pathlib import Path

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from flingern import defs

filesystem_changed = False

class WatchdogHandler(FileSystemEventHandler):
    last_call = 0

    @staticmethod
    def on_any_event(event):
        if time.time() - WatchdogHandler.last_call < 3.0: return
        WatchdogHandler.last_call = time.time()
  
        if event.event_type in ('created', 'modified'):
            # Ignore changes in the public directory (build output)
            if defs.DIR_PUBLIC in event.src_path: return

            print("File %s: %s" % (event.event_type, event.src_path))
            global filesystem_changed
            filesystem_changed = True

def watchdog_at(path):
    # path can be Path object or string
    path_str = str(path)

    event_handler = WatchdogHandler()
    observer = Observer()
    observer.schedule(event_handler, path_str, recursive=True)
    observer.start()
    print("Watching file changes within", path_str)

    return observer

