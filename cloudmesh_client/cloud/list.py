from __future__ import print_function

import importlib
from cloudmesh_client.db import model
from cloudmesh_client.common import tables
from cloudmesh_client.shell.console import Console
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase

class List(object):

    cm_db = CloudmeshDatabase() # Instance to communicate with the cloudmesh database

    @classmethod
    def get_list(cls, kind, cloud, order=None,
                 header=None, output="table"):
        """
        Method lists the data in the db for
        given cloud and of given kind
        :param kind:
        :param cloud:
        :return:
        """
        try:
            # get the model object
            model_kind = cls.get_classobj(kind)

            # get the elements from the db
            elements = cls.cm_db.query(model_kind).filter(
                model_kind.cloud == cloud
            ).all()

            if elements:
                # convert the output to a dict
                d = cls.toDict(elements)
                return (tables.dict_printer(d,
                                    order=order,
                                    header=header,
                                    output=output))
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

    @classmethod
    def get_classobj(cls, kind):
        """
        Method returns an object from model.py
        corresponding to the given kind type
        :param kind:
        :return:
        """
        # get the module reference
        module = importlib.import_module(model.__name__)
        # get tbe class obj reference
        obj = getattr(module, kind)

        return obj

    @classmethod
    def toDict(cls, item):
        """
        Method converts the item to a dict
        :param item:
        :return:
        """
        # Convert to dict & print table
        d = {}
        # If list, iterate to form dict
        if isinstance(item, list):
            for element in item:
                d[element.id] = {}
                for key in element.__dict__.keys():
                    if not key.startswith("_sa"):
                        d[element.id][key] = str(element.__dict__[key])
        # Form dict without iterating
        else:
            d[item.id] = {}
            for key in item.__dict__.keys():
                if not key.startswith("_sa"):
                    d[item.id][key] = str(item.__dict__[key])

        # return the dict
        return d