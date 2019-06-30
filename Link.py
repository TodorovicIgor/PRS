import Resources, Num


class Link:

    def __init__(self, resource_in, resource_out):
        self.input = resource_in
        self.output = resource_out

    def get_id(self):
        self.output.get_id()

    def transfer_job(self, job):
        self.output.accept_job(job)
