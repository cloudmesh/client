from __future__ import print_function

import importlib
from sqlalchemy import and_
from cloudmesh_client.db import model
from cloudmesh_client.common.Printer  import dict_printer
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase


class List(object):
    cm_db = CloudmeshDatabase()
    # Instance to communicate with the cloudmesh database

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
            print (kind)
            model_kind =cls.cm_db.get_table_from_name(kind)
            print
            filter_obj = cls.cm_db.query(model_kind).filter(
                model_kind.cloud == cloud
            )

            # If user is supplied, add to filter
            if user:
                filter_obj = filter_obj.filter(
                    model_kind.user == user
                )

            # If tenant is supplied, add to filter
            if tenant:
                filter_obj = filter_obj.filter(
                    model_kind.project == tenant
                )

            # get the elements from the db
            elements = filter_obj.all()

            if elements:
                # convert the output to a dict
                d = cls.toDict(elements)
                return (dict_printer(d,
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

        print ("M", module)
        print ("K", kind)
        obj = getattr(module, kind)
        #obj = getattr(module, "FLAVOR")
        #obj = cls.cm_db.get_table(kind)
        print (obj)
        return obj

    #
    # TODO: dont we have not already a conversion method
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

    #
    # TODO: i do not see why this method is here its also hardcoded and
    # wrong as india does not exist. if a name is based on openstack,
    # the kluod need to be checked if its openstack and than the user is
    # returned. Than you also want o move this to cloud provider
    #
    @classmethod
    def getUser(cls, cloudname):
        try:
            # currently support India cloud
            if cloudname == "india":
                d = ConfigDict("cloudmesh.yaml")
                credentials = d["cloudmesh"]["clouds"][cloudname][
                    "credentials"]
                for key, value in credentials.iteritems():
                    if key == "OS_USERNAME":
                        return value
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)
