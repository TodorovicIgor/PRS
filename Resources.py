import Queue, Num


class Resource:
    def __init__(self, beta, total_time):
        self.beta = beta
        self.queue = Queue.Fifo()
        self.elapsed_time = 0
        self.total = total_time

    def accept(self, task, k):
        self.queue.append(task)
        while self.queue.is_empty() != 1: #while not empty
            self.queue.take()
            self.elapsed_time += Num.exponential(self.beta)
            if self.elapsed_time > self.total: #simulation over
                return 0
            else:
                self.transferTask(task , k)


class SysDisc(Resource):

    def __init__(self, time):
        Resource.__init__(self, time)


class UserDisc(Resource):

    def __init__(self, time):
        Resource.__init__(self, time)


class CPU(Resource):

    def __init__(self, total ):
        Resource.__init__(self, 0.005, total)

    def send(self):
        rand = Num.random()
        return rand


class Task:

    def __init__(self):

    def next(self, Resource):


class System:

    def __init__(self, k, n):
