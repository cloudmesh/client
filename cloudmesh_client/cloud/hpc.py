from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource


class Hpc(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def refresh(cls, cloud):
        """
        This method would refresh the hpc list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """

        return cls.cm.refresh(kind='hpc', category=cloud)

    @classmethod
    def list(cls, cloud, live=False, format="table"):
        """
        This method lists all hpcs of the cloud
        :param cloud: the cloud name
        """

        try:

            if live:
                cls.refresh(cloud)

            elements = cls.cm.find(kind="hpc", category=cloud)

            # pprint(elements)

            (order, header) = CloudProvider(cloud).get_attributes("hpc")

            return Printer.write(elements,
                                 order=order,
                                 header=header,
                                 output=format)
        except Exception as ex:
            Console.error(ex.message)

    @classmethod
    def details(cls, cloud, id, live=False, format="table"):
        if live:
            cls.refresh(cloud)

        return CloudProvider(cloud).details('hpc', cloud, id, format)
