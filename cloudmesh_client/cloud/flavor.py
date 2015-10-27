from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.db import model
from cloudmesh_client.common import tables
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.common.authenticate import Authenticate


class Flavor(object):
    cm_db = CloudmeshDatabase()

    table_model = model.FLAVOR

    @classmethod
    def authenticate(cls, cloud):
        cls.nova = Authenticate.get_environ(cloud)
        cls._source = cls.nova.flavors

    @classmethod
    def clear(cls, cloud):
        """
        This method deletes all flavors of the cloud
        :param cloud: the cloud name
        """
        try:
            elements = cls.cm_db.query(cls.table_model).filter(
                cls.table_model.cloud == cloud
            ).all()

            for element in elements:
                cls.cm_db.delete(element)
        except Exception as ex:
            Console.error(ex.message, ex)
        finally:
            cls.cm_db.close()

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
            user = cls.cm_db.user

            # read data from openstack

            for data in cls._source.list():
                dictionary = data._info
                element = cls.table_model(
                    dictionary['name'],
                    dictionary['id'],
                    type="string",
                    cloud=cloud,
                    user=user
                )
                cls.cm_db.add(element)
                cls.cm_db.save()
        except Exception as ex:
            Console.error(ex.message, ex)
            return False
        finally:
            cls.cm_db.close()
        return True

    @classmethod
    def list(cls, cloud, format="table"):
        """
        This method lists all flavors of the cloud
        :param cloud: the cloud name
        """
        # TODO: make a CloudmeshDatabase without requireing the user=
        cm = CloudmeshDatabase(user="gregor")

        try:
            elements = cm.find("flavor", cloud=cloud)

            order=['id', 'uuid', 'name', 'cloud']
            # order = None
            return tables.dict_printer(elements,
                                      order=order,
                                      output=format)
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def details(cls, cloud, id, live=False, format="table"):
        if live:
            # taken live information from openstack
            cls.authenticate(cloud)
            details = cls._source.get(id)._info
            d = {}
            count = 0
            for key in details.keys():
                if key != 'links':
                    if key == 'metadata':
                        for meta_key in details['metadata'].keys():
                            d[count] = {}
                            d[count]["Property"], d[count]["Value"] = \
                                'metadata '+meta_key, details['metadata'][meta_key]
                            count += 1
                    elif key == 'server':
                        d[count] = {}
                        d[count]["Property"], d[count]["Value"] = key, details['server']['id']
                        count += 1
                    else:
                        d[count] = {}
                        d[count]["Property"], d[count]["Value"] = key, details[key]
                        count += 1
            return tables.dict_printer(d, order=['Property',
                                                 'Value'],
                                       output=format)

        else:
            # data taken from local database
            try:
                element = cls.cm_db.query(cls.table_model).filter(
                    cls.table_model.cloud == cloud,
                    cls.table_model.uuid == id
                ).first()

                d = {}
                if element:
                    for i, key in enumerate(element.__dict__.keys()):
                        if not key.startswith("_sa"):
                            d[i] = {}
                            d[i]["Property"], d[i]["Value"] = key, str(element.__dict__[key])
                return tables.dict_printer(d, order=['Property',
                                                     'Value'],
                                           output=format)
            except Exception as ex:
                Console.error(ex.message, ex)
            finally:
                cls.cm_db.close()


if __name__ == "__main__":
    Flavor.details("juno", "58c9552c-8d93-42c0-9dea-5f48d90a3188")
