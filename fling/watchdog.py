from importlib.resources import path
import os
from importlib.metadata import files
from operator import truediv
import time

from fling import defs

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

filesystem_changed = False
site_path = ""

class WatchdogHandler(FileSystemEventHandler):
    last_call = 0

    @staticmethod
    def on_any_event(event):
        if time.time() - WatchdogHandler.last_call < 3.0: return
        WatchdogHandler.last_call = time.time()
  
        if event.event_type == 'created' or event.event_type == 'modified':
            if os.path.join(site_path, defs.DIR_PUBLIC) in event.src_path: return

            print("File %s: %s" % (event.event_type, event.src_path))
            global filesystem_changed
            filesystem_changed = True

def watchdog_at(path):
    path_default = path

    event_handler = WatchdogHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("Watching file changes within", path)

    return observer
    