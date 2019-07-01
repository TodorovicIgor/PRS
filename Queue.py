from collections import deque
from threading import Semaphore, Lock


class Fifo:
    cpu_finished = 0

    def __init__(self):
        self.__d = deque()
        self.sem = Semaphore(0)
        self.sem_finished = Semaphore(1)

    def is_finished(self):
        self.sem_finished.acquire(True)
        ret = Fifo.cpu_finished
        self.sem_finished.release()
        return ret == 1

    def finish(self):
        self.sem_finished.acquire(True)
        Fifo.cpu_finished = 1
        self.sem_finished.release()

    def append(self, task):
        self.__d.appendleft(task)
        self.sem.release()

    def is_empty(self):
        return len(self.__d) == 0

    def take(self):
        self.sem.acquire(True)
        return self.__d.pop()
