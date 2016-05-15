from __future__ import print_function

from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db import CloudmeshDatabase


# noinspection PyPep8Naming,PyPep8Naming
class List(object):
    cm = CloudmeshDatabase()

    @classmethod
    def list(cls, kind, cloud, user=None,
             tenant=None, order=None, header=None, output="table"):
        """
        Method lists the data in the db for
        given cloud and of given kind
        :param kind:
        :param cloud:
        :param tenant:
        :param user:
        :param order:
        :param header:
        :param output:
        :return:
        """
        try:

            # get the model object
            table = cls.cm.get_table(kind)

            filter = {}
            if cloud is not None:
                filter["category"] = cloud
            if user is not None:
                filter["user"] = user
            if tenant is not None:
                filter["tenant"] = tenant

            elements = cls.cm.find(table, **filter)

            if elements is not None or elements is not {}:
                # convert the output to a dict
                return (Printer.write(elements,
                                      order=order,
                                      header=header,
                                      output=output))
            else:
                return None

        except Exception as ex:
            Console.error(ex.message)

    #
    # TODO: don't we have not already a conversion method
    #
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
                for key in list(element.__dict__.keys()):
                    if not key.startswith("_sa"):
                        d[element.id][key] = str(element.__dict__[key])
        # Form dict without iterating
        else:
            d[item.id] = {}
            for key in list(item.__dict__.keys()):
                if not key.startswith("_sa"):
                    d[item.id][key] = str(item.__dict__[key])

        # return the dict
        return d
