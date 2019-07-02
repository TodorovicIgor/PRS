import Resources, FileWriter, Num


class Simulation:
    def __init__(self, n, k, time=1080):
        '''
        aux = input('Stepen multiprogramiranja: ')
        self.n = int(aux)
        cond = input('Podrazumevano vreme simulacije je 18h, promeniti ? [y/n] ')
        if cond == 'y':
            self.time = int(input('Unesite vreme simulacije u minutima: '))
        else:
            self.time = 1080
        self.k = k
        # self.time = 20
        # self.n = 5'''

        # initializing
        self.CPU = Resources.CPU(0.005, time, 0)
        self.CPU.set_k(k)
        self.CPU.set_elapsed_time(0)
        self.SysDisc1 = Resources.SysDisc(0.012, time, 1)
        self.SysDisc1.set_k(k)
        self.SysDisc2 = Resources.SysDisc(0.015, time, 2)
        self.SysDisc2.set_k(k)
        self.UserDiscList = [Resources.UserDisc(0.02, time, i+3) for i in range(k)]
        for ud in self.UserDiscList:
            ud.set_k(k)

        self.f1 = FileWriter.BlockingFileWriter("out1.txt")

        # linking resources
        self.cpu_next_res = []
        self.cpu_next_res.append(self.SysDisc1)
        self.cpu_next_res.append(self.SysDisc2)
        for ud in self.UserDiscList:
            self.cpu_next_res.append(ud)
        self.CPU.add_res(self.cpu_next_res)

        self.sys_next_res = []
        self.sys_next_res.append(self.CPU)
        for ud in self.UserDiscList:
            self.sys_next_res.append(ud)
        self.SysDisc1.add_res(self.sys_next_res)
        self.SysDisc2.add_res(self.sys_next_res)

        self.user_next_res = []
        for ud in self.UserDiscList:
            self.user_next_res.append(self.CPU)
            ud.add_res(self.user_next_res)

        #loading jobs
        for i in range(n):
            self.jobList = [Resources.Job() for _ in range(n)]
        for j in self.jobList:
            self.CPU.accept_job(j)

        print('Initialization done')

    def run_simulation(self):
        for ud in self.UserDiscList:
            ud.start()
        self.SysDisc1.start()
        self.SysDisc2.start()
        self.CPU.start()

        for ud in self.UserDiscList:
            ud.join()
        self.SysDisc1.join()
        self.SysDisc2.join()
        self.CPU.join()

        print('Simulation over, writing results...')

        header = "Stepen multiprogramiranja = " + str(n) + ", vreme simulacije u minutima = " + str(time)
        header += " broj korisnickih diskova = " + str(k) + ", odziv sistema = "+str(Resources.Job.avg)
        self.f1.append_to_file(header)
        self.CPU.write_statistics(self.f1, Resources.Job.avg)
        self.SysDisc1.write_statistics(self.f1, Resources.Job.avg)
        self.SysDisc2.write_statistics(self.f1, Resources.Job.avg)
        for ud in self.UserDiscList:
            ud.write_statistics(self.f1, Resources.Job.avg)

        print("Simulation over, preparing resources for next simulation")
        self.CPU.clear()
        self.SysDisc1.clear()
        self.SysDisc2.clear()
        for ud in self.UserDiscList:
            ud.clear()


n = int(input('Stepen multiprogramiranja: '))
cond = input('Podrazumevano vreme simulacije je 18h, promeniti ? [y/n] ')
time = None
if cond == 'y':
    time = int(input('Unesite vreme simulacije u minutima: '))

f2 = open("out2.txt", "w+")
f3 = open("out3.txt", "w+")
for k in range(2, 9):
    GN = Num.solveGN(k)
    f2.write(str(GN))
    B = Num.solveB(GN, n)
    f3.write(str(B))

    f2.close()
    f3.close()
    if cond == 'y':
        s = Simulation(n, k, time)
    else:
        s = Simulation(n, k)
    s.run_simulation()



