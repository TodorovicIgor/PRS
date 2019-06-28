from collections import deque


class Fifo:

    def __init__(self):
        self.__d = deque()

    def append(self, task):
        self.__d.appendleft(task)

    def is_empty(self):
        return len(self.__d) == 0

    def take(self):
        return self.__d.pop()
