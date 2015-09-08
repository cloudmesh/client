from cloudmesh_client.cloud.iaas.ClassProviderBase import CloudProviderBase
from cloudmesh_base.hostlist import Parameter

class CloudProviderOpenstack(ClassProviderBase):


    def initialize(self, cloudname, user=None):
        self.nodes = None
        self.flavors = None
        self.data = None
        self.images = None
        self.cloudname = cloudname
        self.keys = None
        self.user = user
        self.secgroup = None
        self.credential = None
        self.driver = None

    @abstractmethod
    def mode(self, source):
        """
        Sets the source for the information to be returned. "db" and "cloud"
        :param source: the database can be queried in mode "db",
        the database can be bypassed in mode "cloud"
        """
    @abstractmethod
    def list(self, kind, output="table"):
        """

        :param kind: exactly on of  "vm", "flavor", "image",
                     "default", "group", "key"
        :param output: the format: table, dict, csv, json, yaml
        :return: list in given format
        """
        return None

    @abstractmethod
    def boot(self, cloud, user, name, image, flavor, key, secgroup, meta):
        return None

    # TODO: define this
    @classmethod
    def get_image(cls, **kwargs):
        """
        finds the image based on a query
        TODO: details TBD
        """
        return None

    # TODO: define this
    @classmethod
    def get_flavor(cls, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        return None

 # TODO: define this
    @classmethod
    def get_vm(cls, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        return None




