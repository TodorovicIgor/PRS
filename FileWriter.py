import os
from threading import Semaphore


class BlockingFileWriter:

    def __init__(self, s):
        if os.path.isfile(s):
            self.f = open(s, "a+")
        else:
            self.f = open(s, "w+")
        self.lock = Semaphore(1)

    def append_to_file(self, s):
        self.lock.acquire(True)
        self.f.write(s+"\n")
        self.lock.release()

    def __del__(self):
        self.f.close()
