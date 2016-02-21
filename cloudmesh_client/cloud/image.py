from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider

from cloudmesh_client.cloud.ListResource import ListResource


class Image(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def refresh(cls, cloud):
        """
        This method would refresh the image list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """
        # Newly implemented refresh
        result = cls.cm.refresh("image", cloud)
        return result

    @classmethod
    def list(cls, cloud, format="table"):
        """
        This method lists all images of the cloud
        :param cloud: the cloud name
        """
        # TODO: make a CloudmeshDatabase without requiring the user=
        # cm = CloudmeshDatabase()

        try:
            elements = cls.cm.find("image", category=cloud)

            (order, header) = CloudProvider(cloud).get_attributes("image")

            return dict_printer(elements,
                                order=order,
                                header=header,
                                output=format)

        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def details(cls, cloud, id, live=False, format="table"):
        if live:
            cls.refresh(cloud)

        return CloudProvider(cloud).details('image', cloud, id, format)

