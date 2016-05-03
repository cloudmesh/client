from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource


class Workflow(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def refresh(cls, cloud):
        """
        This method would refresh the workflow list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """

        Console.error("workflow does not implement yet a refresh method")
        return

        # return cls.cm.refresh('workflow', cloud)

    @classmethod
    def delete(cls, name):
        pass


    @classmethod
    def list(cls, name, format="table"):
        """
        This method lists all workflows of the cloud
        :param cloud: the cloud name
        """

        try:

            elements = cls.cm.find(kind="workflow", category='general')

            # pprint(elements)

            # (order, header) = CloudProvider(cloud).get_attributes("workflow")
            order = None
            header= None
            return Printer.write(elements,
                                 order=order,
                                 header=header,
                                 output=format)
        except Exception as ex:
            Console.error(ex.message)

    @classmethod
    def details(cls, cloud, id, live=False, format="table"):

        Console.TODO("this method is not yet implemented")
        return None


