from threading import Thread
import Queue, Num, Link

'''
id = x
x = 0           CPU
x = 1,2         SysDisc
x = 3, .. k+3   UserDisc
'''


class Resource(Thread):
    '''
    usage = total_time / elapsed_time
    flow = jobs_done / elapsed_time
    average job number =
    '''
    def __init__(self, beta, total_time, x):
        self.x = x
        self.beta = beta
        self.queue = Queue.Fifo()
        self.elapsed_time = 0
        self.total = total_time
        self.is_working = 0  # start working in run()
        self.links = []
        self.k = 0
        self.jobs_done = 0
        Thread.__init__(self)

    def set_k(self, k):
        self.k = k

    def set_elapsed_time(self, t):
        self.elapsed_time = t

    def getx(self):
        return self.x

    def add_links(self, *links):
        for i in links:
            self.links.append(i)

    def accept_job(self, job):
        if self.x == 0:  # cpu
            job.compute_avg(self.elapsed_time)
        self.queue.append(job)

    def run(self):
        self.is_working = 1
        while self.is_working == 1:
            print('id = ', self.getx(), 'is working ')
            job = self.queue.take()
            self.jobs_done += 1
            self.elapsed_time += Num.exponential(self.beta)
            if self.elapsed_time > self.total:  # simulation over
                self.is_working = 0
            else:
                self.calc_next().Link.transfer_job(job)
        print("Resource with id = ", self.x(), "is finished")
        '''TODO writing to file'''

    def calc_next(self):
        """
        overriden in children
        """
        return Link


class SysDisc(Resource):

    def __init__(self, beta, total_time, x):
        Resource.__init__(self, beta, total_time, x)

    def calc_next(self):
        '''
        50% cpu
        50% some of user discs
        '''
        rand = Num.random()
        if 0 <= rand < 0.5:
            # finding cpu, id=0
            for link in self.links:
                if link.getx() == 0:
                    return link
        else:
            # finding UserDisc
            rand -= 0.5  # rand is > 0  and < 0.5
            aux = divmod(rand, 0.5/self.k)[0] + 3  # formatting for id -> uniform(0 to k)+3
            for link in self.links:
                if link.getx() == aux:
                    return link


class UserDisc(Resource):

    def __init__(self, beta, total_time, x):
        Resource.__init__(self, beta, total_time, x)

    def calc_next(self):
        '''
        100% cpu
        '''
        for link in self.links:
            if link.getx() == 0:
                return link


class CPU(Resource):

    def __init__(self, beta, total_time, x):
        Resource.__init__(self, beta, total_time, x)

    def calc_next(self):
        '''
        15% system disc1
        15% system disc2
        70% some of user discs
        '''
        rand = Num.random()
        if 0 <= rand < 0.15:
            for link in self.links:
                if link.getx() == 1:
                    return link
        if 0 <= rand < 0.3:
            for link in self.links:
                if link.getx() == 1:
                    return link
        else:
            rand -= 0.3  # rand is > 0  and < 0.7
            aux = divmod(rand, 0.7 / self.k)[0] + 3  # formatting for id -> uniform(0 to k)+3
            for link in self.links:
                if link.getx() == aux:
                    return link


class Job:

    def __init__(self):
        self.last_cpu_enter = -1
        self.avg_sum = 0
        self.avg_num = 0
        self.avg = 0

    def compute_avg(self, elapsed_time):
        if self.last_cpu_enter != -1:
            time_diff=elapsed_time - self.last_cpu_enter
            self.last_cpu_enter = elapsed_time
            self.avg_num += 1
            self.avg_sum += time_diff
            self.avg = self.avg_sum/self.avg_num
        else:
            self.last_cpu_enter = elapsed_time  # no computing at initial state
