from threading import Thread
import Queue
import Num

'''
x = 0           CPU
x = 1,2         SysDisc
x = 3, .. k+3   UserDisc
'''


class Resource(Thread):
    '''
    usage = total_time / elapsed_time
    flow = jobs_done / elapsed_time
    response time = avg from jobs
    average job number = response * flow
    '''
    def __init__(self, beta, total_time, x):
        self.x = x
        self.beta = beta
        self.queue = Queue.Fifo()
        self.elapsed_time = 0
        self.total = total_time
        self.is_working = 0  # start working in run()
        self.next_res = []
        self.k = 0
        self.jobs_done = 0
        Thread.__init__(self)

    def get_usage(self):
        return self.total/self.elapsed_time

    def get_flow(self):
        return self.jobs_done/self.elapsed_time

    def set_k(self, k):
        self.k = k

    def set_elapsed_time(self, t):
        self.elapsed_time = t

    def getx(self):
        return self.x

    def add_res(self, *res):
        for i in res:
            self.next_res.append(i)

    def accept_job(self, job):
        if self.x == 0:  # cpu
            job.compute_avg(self.elapsed_time)
        self.queue.append(job)

    def load_next_res_with_dummies(self):
        for i in self.next_res:
            for res in i:
                res.accept_job(Job(1))

    def run(self):
        self.is_working = 1
        while self.is_working == 1:
            # print('id = ', self.getx(), 'is working ')
            '''
            queue is not finished and job is not dummy and elapsed time > total
            '''
            if not self.queue.is_finished():
                job = self.queue.take()
                if job.is_dummy():
                    print("Resource with id =", self.x, "is finished, time busy is ", self.elapsed_time)
                    self.is_working = 0
                    self.load_next_res_with_dummies()
                else:
                    self.jobs_done += 1
                    self.elapsed_time += Num.exponential(self.beta)
                    if (self.elapsed_time > self.total) or self.queue.is_finished():  # cpu is done
                        print("Resource with id =", self.x, "is finished, time busy is ", self.elapsed_time)
                        self.is_working = 0
                        self.load_next_res_with_dummies()
                    else:
                        self.calc_next().accept_job(job)
            else:
                self.is_working = 0
                print("Resource with id =", self.x, "is finished, time busy is ", self.elapsed_time)
        # sim is done, checking jobs in queue
        for elem in self.queue.d:
            if not elem.is_dummy():
                elem.compute_glob_avg()
        '''TODO writing to file'''

    def calc_next(self):
        """
        overridden in children
        """
        pass


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
            for i in self.next_res:
                for res in i:
                    if res.getx() == 1:
                        return res
        if 0.15 <= rand < 0.3:
            for i in self.next_res:
                for res in i:
                    if res.getx() == 2:
                        return res
        else:
            rand -= 0.3  # rand is > 0  and < 0.7
            aux = divmod(rand, 0.7 / self.k)[0] + 3  # formatting for id -> uniform(0 to k)+3
            for i in self.next_res:
                for res in i:
                    if res.getx() == aux:
                        return res


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
            for i in self.next_res:
                for res in i:
                    if res.getx() == 0:
                        return res
        else:
            # finding UserDisc
            rand -= 0.5  # rand is > 0  and < 0.5
            aux = divmod(rand, 0.5/self.k)[0] + 3  # formatting for id -> uniform(0 to k)+3
            for i in self.next_res:
                for res in i:
                    if res.getx() == aux:
                        return res


class UserDisc(Resource):

    def __init__(self, beta, total_time, x):
        Resource.__init__(self, beta, total_time, x)

    def calc_next(self):
        '''
        100% cpu
        '''
        for i in self.next_res:
            for res in i:
                if res.getx() == 0:
                    return res


class Job:
    # global average job time
    avg_sum = 0
    avg_num = 0
    avg = 0

    def __init__(self, dummy=0):
        self.dummy = dummy
        self.last_cpu_enter = -1
        self.avg_sum = 0
        self.avg_num = 0

    def is_dummy(self):
        return self.dummy

    def compute_avg(self, elapsed_time):
        if self.last_cpu_enter != -1:
            time_diff=elapsed_time - self.last_cpu_enter
            self.last_cpu_enter = elapsed_time
            self.avg_num += 1
            self.avg_sum += time_diff
        else:
            self.last_cpu_enter = elapsed_time  # no computing at initial state

    def compute_glob_avg(self):
        Job.avg_num += self.avg_num
        Job.avg_sum += self.avg_sum
        Job.avg = Job.avg_sum/Job.avg_num