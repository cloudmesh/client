from cloudmesh_base.hostlist import Parameter


class IP(object):

    def create(self):
        ip = None
        return ip
        pass

    def assign(self, ip, vm):
        pass

    def release(self, ip):
        pass


class compute(object):

    dryrun = False

    def __init__(self, dryrun=False):
        self.dryrun = dryrun

    def delete_by_name(name):
        if dryrun:
            print ("delete " + name)
        else:
            print ("not implemented")

    def delete(self, names):
        result = Parameter.expand(names)
        for name in result:
            self.delete_by_name(name)

    def boot(self):
        print ("not implemented")
        pass


    def list(self, clouds):
        print ("not implemented")
        pass


    def login(self, vm):
        print ("not implemented")
        pass