from collections import deque
from threading import Semaphore


class Fifo:

    def __init__(self):
        self.__d = deque()
        self.sem = Semaphore(0)

    def append(self, task):
        self.__d.appendleft(task)
        self.sem.release()

    def is_empty(self):
        return len(self.__d) == 0

    def take(self):
        self.sem.acquire(True)
        return self.__d.pop()
