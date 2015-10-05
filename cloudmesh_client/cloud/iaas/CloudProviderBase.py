from abc import ABCMeta, abstractmethod, abstractproperty

from cloudmesh_base.hostlist import Parameter
#
# Abstarct class to tell us what we have to define
#


class CloudmeshProviderBase(object):
    __metaclass__ = ABCMeta

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
    def list(self):
        """
        Listing of vm instances
        :return:
        """
        return None

    @abstractmethod
    def boot(self, cloud, user, name, image, flavor, key, secgroup, meta):
        """
        Boots a new vm instance on the target cloud.
        :param cloud:
        :param user:
        :param name:
        :param image:
        :param flavor:
        :param key:
        :param secgroup:
        :param meta:
        :return:
        """
        return None

    @abstractmethod
    def delete(self, name, group=None, force=None):
        """
        Deletes the vm indicated by name_or_id on target cloud.
        :param name_or_id:
        :param group:
        :param force:
        :return:
        """

    @abstractmethod
    def get_ips(self, name, group=None, force=None):
        """
        Returns the ip addresses of the instance indicated by name_or_id
        :param name_or_id:
        :param group:
        :param force:
        :return:
        """

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

    # TODO: define this
    @classmethod
    def refresh(cls, cloud, kind, **kwargs):
        """
        refreshes the information from the cloud into the db

        refresh ("india,aws", "vm,images")

        uses parametrized arguments defined by Parameter in cloudmesh.base

        TODO: details TBD
        """
        return None





