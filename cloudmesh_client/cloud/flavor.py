from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.db import model
from cloudmesh_client.common.Printer  import dict_printer
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.cloud.list import List

class Flavor(ListResource):
    db = CloudmeshDatabase()

    table_model = model.FLAVOR

    @classmethod
    def authenticate(cls, cloud):
        cls.provider = CloudProvider.set(cloud)
        cls._source = cls.provider.flavors

    @classmethod
    def clear(cls, cloud):
        """
        This method deletes all flavors of the cloud
        :param cloud: the cloud name
        """
        try:
            elements = cls.db.query(cls.table_model).filter(
                cls.table_model.cloud == cloud
            ).all()

            for element in elements:
                cls.db.delete(element)
        except Exception as ex:
            Console.error(ex.message, ex)
        finally:
            cls.db.close()

    @classmethod
    def refresh(cls, cloud):
        """
        This method would refresh the flavor list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """
        # set the environment
        cls.authenticate(cloud)
        # delete previous data

        try:
            cls.clear(cloud)
            # get the user
            user = cls.db.user

            # read data from openstack

            for data in cls._source.list():
                dictionary = data._info
                # print (data._info.keys())
                element = cls.table_model(
                    dictionary['name'],
                    dictionary['id'],
                    type="string",
                    cloud=cloud,
                    user=user
                )
                cls.db.add(element)
                cls.db.save()
        except Exception as ex:
            Console.error(ex.message, ex)
            return False
        finally:
            cls.db.close()
        return True

    @classmethod
    def list(cls, cloud, format="table"):
        """
        This method lists all flavors of the cloud
        :param cloud: the cloud name
        """
        # TODO: make a CloudmeshDatabase without requiring the user=

        user = "gregor"
        tenant = None
        cm = CloudmeshDatabase(user=user)

        try:
            elements = cm.find("flavor", cloud=cloud)

            provider = CloudProvider.set(cloud)
            order, header = provider.attributes("flavor")


            return List.list("flavor",
                 cloud,
                 user=user,
                 tenant=None,
                 order=order,
                 header=header,
                 output=format)

            return dict_printer(elements,
                                       order=order,
                                       output=format)
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def details(cls, cloud, id, live=False, format="table"):
        if live:
            cls.refresh(cloud)

        try:
            cm = CloudmeshDatabase(user="gregor")

            elements = cm.find("flavor", cloud=cloud, uuid=id)
            if format == "table":
                element = elements.values()[0]
                return tables.attribute_printer(element)
            else:
                return dict_printer(elements,
                                           output=format)
        except Exception as ex:
            Console.error(ex.message, ex)


if __name__ == "__main__":
    Flavor.details("juno", "58c9552c-8d93-42c0-9dea-5f48d90a3188")
