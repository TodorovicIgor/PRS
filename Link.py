class Link:

    def __init__(self, res_in, res_out):
        self.input = res_in
        self.output = res_out

    def getx(self):
        self.output.getx()

    def print(self):
        print(self.input, self.output)

    def transfer_job(self, job):
        self.output.accept_job(job)
