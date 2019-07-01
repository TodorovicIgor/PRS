import Resources, Link


class Simulation:
    def __init__(self, k):
        #aux = input('Stepen multiprogramiranja: ')
        #self.n = int(aux)
        #cond = input('Podrazumevano vreme simulacije je 18h, promeniti ? [y/n] ')
        #if cond == 'y':
        #    self.time = int(input('Unesite vreme simulacije u minutima: '))
        #else:
        #    self.time = 1080
        self.time = 10
        self.n = 5

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
        '''
        k+2 links for cpu
        k+1 links for 1 sysdisc
        1 link for userdisc
        '''
        self.cpu_links = []
        for i in range(k):
            li = Link.Link(self.CPU, self.UserDiscList[i])
            self.cpu_links.append(li)
        self.cpu_links.append(Link.Link(self.CPU, self.SysDisc1))
        self.cpu_links.append(Link.Link(self.CPU, self.SysDisc2))

        self.sys1_links = []
        for i in range(k):
            self.sys1_links.append(Link.Link(self.SysDisc1, self.UserDiscList[i]))
        self.sys1_links.append(Link.Link(self.SysDisc1, self.CPU))

        self.sys2_links = []
        for i in range(k):
            self.sys2_links.append(Link.Link(self.SysDisc2, self.UserDiscList[i]))
        self.sys2_links.append(Link.Link(self.SysDisc2, self.CPU))

        #self.user_links = [[Link.Link(self.UserDiscList[i], self.CPU) for i in range(k)]]
        self.user_link = []
        for i in range(k):
            self.user_link.append(Link.Link(self.UserDiscList[i], self.CPU))

        self.CPU.add_links(self.cpu_links)
        self.SysDisc1.add_links(self.sys1_links)
        self.SysDisc2.add_links(self.sys2_links)
        print(len(self.UserDiscList))
        for ud in self.UserDiscList:
            ud.add_links([Link.Link(ud, self.CPU)])

        #loading jobs
        for i in range(self.n):
            self.jobList = [Resources.Job() for _ in range(self.n)]
        for j in self.jobList:
            self.CPU.accept_job(j)
        print('Initilization done')

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

