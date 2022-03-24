from importlib.metadata import files
from operator import truediv
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

filesystem_changed = False

class WatchdogHandler(FileSystemEventHandler):
    last_call = 0

    @staticmethod
    def on_any_event(event):
        if time.time() - WatchdogHandler.last_call < 3.0: return
        WatchdogHandler.last_call = time.time()
  
        if event.event_type == 'created' or event.event_type == 'modified':
            print("File %s: %s" % (event.event_type, event.src_path))
            global filesystem_changed
            filesystem_changed = True

def watchdog_at(path):
    event_handler = WatchdogHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("Watching file changes within", path)

    return observer
    