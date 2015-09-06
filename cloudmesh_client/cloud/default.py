from __future__ import print_function

from cloudmesh_client.db import model
from cloudmesh_client.common import tables
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase


class Default(object):

    @classmethod
    def list(cls, format="table"):
        cm = CloudmeshDatabase()
        d = cm.all(model.DEFAULT)
        return (tables.dict_printer(d,
                             order=['user',
                                    'cloud',
                                    'name',
                                    'value'],
                             output=format))

    #
    # GENERAL SETER AND GETER METHOD
    #

    @classmethod
    def set(cls, key, value, cloud=None):
        print ("KKK", key, value, cloud)
        cm = CloudmeshDatabase()
        # d = cm.dict(DEFAULT)
        o = Default.get_object(key, cloud)
        print ("OOO object", key, cloud)
        if o is None:
            print ("create new o", key, value, cloud)
            o = model.DEFAULT(key, value, cloud=cloud)
            print (o.__dict__)
            cm.add(o)
        else:
            o.value = value
        print ("PPPP", o.name, o.value, o.cloud)
        cm.save()

    @classmethod
    def get_object(cls, key, cloud=None):
        print("get object:", key, cloud)
        cm = CloudmeshDatabase()
        which_cloud = cloud or "general"
        print ("W", which_cloud)
        o = cm.query(model.DEFAULT).filter(model.DEFAULT.name==key).first()
                                           # model.DEFAULT.cloud==which_cloud).first()
        print ("OOOO", o)
        return o

    @classmethod
    def get(cls, key, cloud=None):
        o = cls.get_object(key, cloud=cloud)
        if o is None:
            return None
        else:
            return o.value

    @classmethod
    def delete(cls, key, cloud):
        cm = CloudmeshDatabase()
        o = Default.get(key, cloud)
        if o is not None:
            cm.delete(o)
        cm.save()

    @classmethod
    def clear(cls):
        cm = CloudmeshDatabase()
        d = cm.all(model.DEFAULT)
        for item in d:
            name = d[item]["name"]
            kind = model.DEFAULT
            cm.delete_by_name(kind, name)
        cm.save()
    #
    # Set the default cloud
    #
    @classmethod
    def get_cloud(cls):
        o = cls.get("cloud", cloud="general")
        print ("LLL", o)
        return o

    @classmethod
    def set_cloud(cls, value):
        cls.set("cloud", value, cloud="general")

    #
    # Set the default image
    #

    @classmethod
    def set_image(cls, value, cloud):
        cls.set("image", value, cloud)

    @classmethod
    def get_image(cls, cloud):
        return cls.get("image", cloud)

    #
    # Set the default flavor
    #

    @classmethod
    def set_flavor(cls, value, cloud):
        cls.set("flavor", value, cloud)

    @classmethod
    def get_flavor(cls, cloud):
        return cls.get("flavor", cloud)

    #
    # Set the default group
    #

    @classmethod
    def set_group(cls, value):
        cls.set("group", value, "general")

    @classmethod
    def get_group(cls):
        return cls.get("group", "general")

    #
    # Set the default key
    #

    @classmethod
    def set_key(cls, value):
        cls.set("key", value, "general")

    @classmethod
    def get_key(cls):
        return cls.get("key", "general")
