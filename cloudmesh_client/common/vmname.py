import getpass
from cloudmesh_client.cloud.default import Default

class VMName(object):

    @staticmethod
    def get(prefix=None, idx=None, user=None):
        """Return a vm name to use next time. prefix or index can be
        given to update a vm name (optional)

        Args:
            prefix (str, optional): the name of prefix
            idx (int, str, optional): the index to increment. This can be a
            digit or arithmetic e.g. +5 or -3 can be used

        """
        user = user or getpass.getuser()
        prefix = prefix or user
        if type(idx) is not int:
            idx = int(idx)
        Default.set('index', idx)
        return "%{:}_%{:}".format()

    @staticmethod
    def next():
        return VMName.vmname(idx="+1")
