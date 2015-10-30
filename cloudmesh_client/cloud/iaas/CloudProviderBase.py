from abc import ABCMeta, abstractmethod, abstractproperty

from cloudmesh_base.hostlist import Parameter
#
# Abstarct class to tell us what we have to define
#


class CloudmeshProviderBase(object):

    @classmethod
    def initialize(cls, cloudname, user=None):
        cls.nodes = None
        cls.flavors = None
        cls.data = None
        cls.images = None
        cls.cloudname = cloudname
        cls.keys = None
        cls.user = user
        cls.secgroup = None
        cls.credential = None
        cls.driver = None

    @classmethod
    def mode(cls, source):
        """
        Sets the source for the information to be returned. "db" and "cloud"
        :param source: the database can be queried in mode "db",
        the database can be bypassed in mode "cloud"
        """
        raise NotImplemented("Not implemented yet.")
        return None

    @classmethod
    def list(cls):
        """
        Listing of vm instances
        :return:
        """
        raise NotImplemented("Not implemented yet.")
        return None

    @classmethod
    def boot(cls, cloud, user, name, image, flavor, key, secgroup, meta):
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
        raise NotImplemented("Not implemented yet.")
        return None

    @classmethod
    def delete(cls, name, group=None, force=None):
        """
        Deletes the vm indicated by name_or_id on target cloud.
        :param name_or_id:
        :param group:
        :param force:
        :return:
        """
        raise NotImplemented("Not implemented yet.")
        return

    @classmethod
    def get_ips(cls, name, group=None, force=None):
        """
        Returns the ip addresses of the instance indicated by name_or_id
        :param name_or_id:
        :param group:
        :param force:
        :return:
        """
        raise NotImplemented("Not implemented yet.")
        return

    @classmethod
    def get_image(cls, **kwargs):
        """
        finds the image based on a query
        TODO: details TBD
        """
        return None

    @classmethod
    def get_flavor(cls, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        raise NotImplemented("Not implemented yet.")
        return

    @classmethod
    def get_vm(cls, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        raise NotImplemented("Not implemented yet.")
        return

    @classmethod
    def refresh(cls, cloud, kind, **kwargs):
        """
        refreshes the information from the cloud into the db

        refresh ("india,aws", "vm,images")

        uses parametrized arguments defined by Parameter in cloudmesh.base

        TODO: details TBD
        """
        raise NotImplemented("Not implemented yet.")
        return





