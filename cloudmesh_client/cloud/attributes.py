from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource


# noinspection PyIncorrectDocstring
class Attributes(ListResource):
    # cm = CloudmeshDatabase()

    @classmethod
    def refresh(cls, cloud):
        """This method has no effect for attributes
        :param cloud: The name of the cloud
        """
        return None

    @classmethod
    def list(cls, cloud, kind):
        """
        This method lists all flavors of the cloud
        :param cloud: the cloud name
        :param kind: the kind of the attribute
        """
        try:
            (order, header) = CloudProvider(cloud).get_attributes(kind)
            return order, header
        except Exception as ex:
            Console.error(ex.message)
