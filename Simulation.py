import Resources


class Simulation:
    def __init__(self, k):
        aux = input('Stepen multiprogramiranja: ')
        self.n = int(aux)
        cond = input('Podrazumevano vreme simulacije je 18h, promeniti ? [y/n] ')
        if cond == 'y':
            self.time = input('Unesite vreme simulacije u minutima: ')
        else:
            self.time = 1080

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
        #aux = self.UserDiscList.append(self.SysDisc1)  # MOZDA GRESKA !!!!!!!!!!!!!!!
        #aux.append(self.SysDisc2)
        self.CPU.append_resources([self.UserDiscList, self.SysDisc2, self.SysDisc1])
        self.SysDisc1.append_resources(self.CPU, self.UserDiscList)
        self.SysDisc2.append_resources(self.CPU, self.UserDiscList)
        for ud in self.UserDiscList:
            ud.append_resources(self.CPU)

        #loading jobs
        for i in range(self.n):
            self.jobList = [Resources.Job() for _ in range(self.n)]
        for j in self.jobList:
            self.CPU.accept_job(j)

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


s = Simulation(5)
s.run_simulation(4)

