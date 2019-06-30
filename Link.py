class Link:

    def __init__(self, resource_in, resource_out):
        self.input = resource_in
        self.output = resource_out

    def getx(self):
        self.output.getx()

    def transfer_job(self, job):
        self.output.accept_job(job)
