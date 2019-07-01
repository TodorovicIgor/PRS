import Resources


class Simulation:
    def __init__(self, k):
        aux = input('Stepen multiprogramiranja: ')
        self.n = int(aux)
        cond = input('Podrazumevano vreme simulacije je 18h, promeniti ? [y/n] ')
        if cond == 'y':
            self.time = int(input('Unesite vreme simulacije u minutima: '))
        else:
            self.time = 1080
        # self.time = 20
        # self.n = 5

        # initializing
        self.CPU = Resources.CPU(0.005, self.time, 0)
        self.CPU.set_k(k)
        self.CPU.set_elapsed_time(0)
        self.SysDisc1 = Resources.SysDisc(0.012, self.time, 1)
        self.SysDisc1.set_k(k)
        self.SysDisc2 = Resources.SysDisc(0.015, self.time, 2)
        self.SysDisc2.set_k(k)
        self.UserDiscList = [Resources.UserDisc(0.02, self.time, i+3) for i in range(k)]
        for ud in self.UserDiscList:
            ud.set_k(k)

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
        for i in range(self.n):
            self.jobList = [Resources.Job() for _ in range(self.n)]
        for j in self.jobList:
            self.CPU.accept_job(j)

        # file variable
        self.f1 = open("out1.txt", "w+")
        header = "Stepen multiprogramiranja = "+str(self.n)+", vreme simulacije u minutima = "+str(self.time)
        self.f1.write(header)
        self.f1.close()
        print('Initialization done')

    def run_simulation(self, k):
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

        print('Simulation over')

        # writing to file
        f1 = open("out1.txt", "a+")
        f1.write("Simulation over")



s = Simulation(5)
s.run_simulation(4)


