from __future__ import print_function
from cloudmesh_client.common.ConfigDict import ConfigDict

from cloudmesh_client.common.todo import TODO
# add imports for other cloud providers in future
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.Error import Error
from uuid import UUID
from cloudmesh_client.common.dotdict import dotdict
from builtins import input
from pprint import pprint


# noinspection PyPep8Naming
class Key(ListResource):
    @classmethod
    def info(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def list(cls, cloud, live=False, format="table"):
        """
        This method lists all flavors of the cloud
        :param cloud: the cloud name
        """
        try:

            keys = CloudProvider(cloud).provider.list_key(cloud)

            (order, header) = CloudProvider(cloud).get_attributes("key")

            return Printer.write(keys,
                                 order=order,
                                 header=header,
                                 output=format)
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def clear(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def refresh(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def delete(self, name, cloud=None):

        result = CloudProvider(cloud).provider.delete_key_from_cloud(name)
