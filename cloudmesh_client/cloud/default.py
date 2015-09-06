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
    def set(cls, key, value, cloud=None, user=None):
        cm = CloudmeshDatabase(user=user)
        # d = cm.dict(DEFAULT)
        o = Default.get_object(key, cloud)
        me = cm.user or user
        if o is None:
            o = model.DEFAULT(key, value, cloud=cloud, user=me)
            cm.add(o)
        else:
            o.value = value
        cm.save()

    @classmethod
    def get_object(cls, key, cloud=None):
        cm = CloudmeshDatabase()
        which_cloud = cloud or "general"
        o = cm.query(model.DEFAULT).filter(
            model.DEFAULT.name==key,
            model.DEFAULT.cloud==which_cloud
        ).first()
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
