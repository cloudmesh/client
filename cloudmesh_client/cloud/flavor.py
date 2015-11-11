from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.db import model
from cloudmesh_client.common.Printer import dict_printer, attribute_printer, \
    list_printer
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.cloud.list import List
from pprint import pprint


class Flavor(ListResource):
    db = CloudmeshDatabase()

    @classmethod
    def clear(cls, cloud):
        """
        This method deletes all flavors of the cloud
        :param cloud: the cloud name
        """
        try:
            elements = cls.db.find("flavor", scope="all", cloud=cloud)

            for element in elements:
                cls.db.delete(element)
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def refresh(cls, cloud):
        """
        This method would refresh the flavor list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """
        return cls.db.refresh('flavor', cloud)

    @classmethod
    def list(cls, cloud, live=False, format="table"):
        """
        This method lists all flavors of the cloud
        :param cloud: the cloud name
        """
        cm = CloudmeshDatabase()

        try:

            if live:
                cls.refresh(cloud)
            elements = cm.find("flavor", cloud=cloud)

            pprint(elements)

            (order, header) = CloudProvider(cloud).get_attributes("flavor")
            return dict_printer(elements,
                                order=order,
                                output=format)
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def details(cls, cloud, id, live=False, format="table"):

        try:

            if live:
                cls.refresh(cloud)

            provider = CloudProvider(cloud).provider

            if id.isdigit():
                args = {'id': id}
            else:
                args = {'name': id}

            flavor = provider.get_flavor(**args)

            if format == "table":
                # return attribute_printer(flavor)

                return dict_printer({"0": flavor})

            else:
                return dict_printer(flavor,
                                    output=format)

        except Exception as ex:
            Console.error(ex.message, ex)


if __name__ == "__main__":
    Flavor.details("juno", "58c9552c-8d93-42c0-9dea-5f48d90a3188")
