"""
This module defines the main API for operating with cloudmesh.
"""

from abc import ABCMeta, abstractmethod, abstractproperty

from cloudmesh_client.common.ConfigDict import ConfigDict

from cloudmesh_client import CloudmeshDatabase


class Config(object):
    """
    The Cloudmesh configuration
    """

    __metaclass__ =  ABCMeta

    pass


class Resource(object):


    __metaclass__ = ABCMeta
    db = CloudmeshDatabase()

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def refresh(self):
        pass


class Provider(object):
    """
    A Provider is a collection of :class:`Resource`\ s
    that may be operated upon.
    """

    __metaclass__ = ABCMeta
    db = CloudmeshDatabase()
    cfg = ConfigDict("~/.cloudmesh/cloudmesh.yaml")

    _resources = list()

    def _add_resource(self, resource):
        """Adds a resources. To be used by subclasses"""
        self._resources.append(resource)

    def resources(self):
        return self._resources.copy()

    ###################################################################

    def __init__(self, cloud):
        self._cloud = cloud

    @property
    def cloud(self):
        return self._cloud

    @classmethod
    def from_cloud(cls, cloud_name):
        """

        :param str cloud_name: name of the cloud as found in cloudmesh.yaml
        """

        provider_name = cls.cfg['cloudmesh']['clouds'][cloud_name]['cm_type']

        if provider_name == 'openstack':
            from cloudmesh_client.api.impl.openstack import OpenstackProvider
            return OpenstackProvider(cloud=cloud_name)
        else:
            raise NotImplemented('Provider %s' % provider_name)

    @abstractmethod
    def node(self):
        """Factory method to create an instance of the
        appropriate subclass of :class:`Node`"""
        pass

    @abstractmethod
    def boot(self):
        """Boots a single VM"""
        pass

    @abstractmethod
    def delete(self, node):
        """Deletes a running :class:`Node`"""
        pass

    @abstractmethod
    def create_ip(self, node):
        """
        Creates and associeates a public ip with given node

        :param Node node:
        :return:
        """
        pass




class Node(object):
    """
    A Node is machine running on some :class:`Provider`
    """

    __metaclass__ = ABCMeta
    db = CloudmeshDatabase()

    @abstractproperty
    def name(self):
        "The name of this machine"
        pass

    @abstractproperty
    def username(self):
        "The login username for this machine. None if unknown"
        pass

    @abstractproperty
    def private_ip(self):
        "The private ip address of this node"
        pass

    @abstractproperty
    def public_ip(self):
        "The public ip address of this node"
        pass

    @abstractmethod
    def start(selfs):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def create_ip(self):
        pass

    @abstractmethod
    def ssh(self, cmd=None, user=None):
        """ssh into and optionally run a command on this node

        :param list(str) cmd: the command to run
        :param str user: the user to login as (defaults to self.name
        """
        pass


class Cluster(object):
    """
    A Cluster is a collection of :class:`Node`\'s that need to interact
    """

    __metaclass__ = ABCMeta
    db = CloudmeshDatabase()


class Stack(object):

    __metaclass__ = ABCMeta
    db = CloudmeshDatabase()

class Layer(object):

    __metaclass__ = ABCMeta
    db = CloudmeshDatabase()