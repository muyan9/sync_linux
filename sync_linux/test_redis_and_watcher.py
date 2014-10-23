import redis

import os, time, signal
from pyinotify import  WatchManager, ProcessEvent, ThreadedNotifier, IN_MOVED_TO
flag_run = True 
num_filetotal = 0

class FileRsyncWatcher(ProcessEvent):
    _redis = redis.Redis(host='localhost', port=6379, db=0)
    #TODO: put into config file
    _queue_name = "rsync_files_changed"
    
    def process_IN_MOVED_TO(self, event):
        if os.path.basename(event.name)[0] != ".":
            self._redis.lpush(self._queue_name, os.path.join(event.path, event.name))

path = "."
wm = WatchManager()
mask = IN_MOVED_TO
notifier = ThreadedNotifier(wm, FileRsyncWatcher()) 
wm.add_watch(path, mask,auto_add=True, rec=True) 
notifier.start()

def fun_quit(a,b):
    global flag_run
    flag_run = False
    notifier.stop()

signal.signal(signal.SIGINT, fun_quit)
signal.signal(signal.SIGTERM, fun_quit)

while flag_run:
    time.sleep(1)
#     print len(list_file_newer)#, #list_file_newer
