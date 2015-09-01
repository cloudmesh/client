from __future__ import print_function
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.db.model import DEFAULT
from cloudmesh_client.common.tables import dict_printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from pprint import pprint


class Default(object):

    @classmethod
    def list(cls, format="table"):
        cm = CloudmeshDatabase()
        d = cm.all(DEFAULT)
        return(dict_printer(d, order=['cm_user',
                                      'cm_cloud',
                                      'name',
                                      'value'], output=format))

    #
    # GENERAL SETER AND GETER METHOD
    #

    @classmethod
    def set(cls, key, value, cloud):
        cm = CloudmeshDatabase()
        d = cm.dict(DEFAULT)
        cm.set_default(key, value, cloud)

    @classmethod
    def get(cls, key, cloud):
        cm = CloudmeshDatabase()
        return(cm.get_default(key, cloud))

    @classmethod
    def delete(cls, key, cloud):
        cm = CloudmeshDatabase()
        _id = cm.getID("default", key, cloud)
        e = cm.find(DEFAULT, cm_id=_id).first()
        if e is not None:
            cm.delete(e)

    @classmethod
    def clear(cls):
        cm = CloudmeshDatabase()
        d = cm.all(DEFAULT)
        for item in d:
            name = d[item]["name"]
            kind = DEFAULT
            cm.delete_by_name(kind, name)

    #
    # Set the default cloud
    #
    @classmethod
    def get_cloud(cls):
        return(cls.get("cloud", "general"))

    @classmethod
    def set_cloud(cls, value):
        cls.set("cloud", value, "general")


    #
    # Set the default image
    #

    @classmethod
    def set_image(cls, value, cloud):
        cls.set("image", value, cloud)

    @classmethod
    def get_image(cls, cloud):
        return(cls.get("image", cloud))

    #
    # Set the default flavor
    #

    @classmethod
    def set_flavor(cls, value, cloud):
        cls.set("flavor", value, cloud)

    @classmethod
    def get_flavor(cls, cloud):
        return(cls.get("flavor", cloud))

    #
    # Set the default group
    #

    @classmethod
    def set_group(cls, value):
        cls.set("group", value, "general")

    @classmethod
    def get_group(cls):
        return(cls.get("group", "general"))

    #
    # Set the default key
    #

    @classmethod
    def set_key(cls, value):
        cls.set("key", value, "general")

    @classmethod
    def get_key(cls):
        return(cls.get("key", "general"))
