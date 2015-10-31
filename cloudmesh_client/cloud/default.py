from __future__ import print_function

from cloudmesh_client.db import model
from cloudmesh_client.common import Printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.ListResource import ListResource


class Default(ListResource):
    cm_db = CloudmeshDatabase()
    # Create a static variable so that db is initialized once in a transaction

    @classmethod
    def list(cls,
             format="table",
             order=['user', 'cloud', 'name', 'value'],
             output=format):

        try:
            d = cls.cm_db.all(model.DEFAULT)
            return (Printer.dict_printer(d,
                                        order=order,
                                        output=format))
        finally:
            cls.cm_db.close()

    @classmethod
    def get_objects(cls, cloud, format="table"):
        try:
            elements = cls.cm_db.query(model.DEFAULT).filter(
                model.DEFAULT.cloud == cloud
            )
            d = {}
            for element in elements:
                d[element.id] = {}
                for key in element.__dict__.keys():
                    if not key.startswith("_sa"):
                        d[element.id][key] = str(element.__dict__[key])

            return (Printer.dict_printer(d,
                                        order=['user',
                                               'cloud',
                                               'name',
                                               'value'],
                                        output=format))
        finally:
            cls.cm_db.close()

    #
    # GENERAL SETTER AND GETTER METHOD
    #

    @classmethod
    def set(cls, key, value, cloud=None, user=None):
        try:
            o = Default.get_object(key, cloud)
            me = cls.cm_db.user or user
            if o is None:
                o = model.DEFAULT(key, value, cloud=cloud, user=me)
            else:
                o.value = value
            cls.cm_db.add(o)
        finally:
            cls.cm_db.close()

    @classmethod
    def get_object(cls, key, cloud=None):
        try:
            which_cloud = cloud or "general"
            o = cls.cm_db.query(model.DEFAULT).filter(
                model.DEFAULT.name == key,
                model.DEFAULT.cloud == which_cloud
            ).first()
            return o
        finally:
            cls.cm_db.close()

    @classmethod
    def get(cls, key, cloud=None):
        try:
            o = cls.get_object(key, cloud=cloud)
            if o is None:
                return None
            else:
                return o.value
            if result is None:
                if key == 'cloud':
                    result = 'general'
                elif key == 'group':
                    result = 'default'
        finally:
            cls.cm_db.close()

    @classmethod
    def delete(cls, key, cloud):
        try:
            o = Default.get_object(key, cloud)
            if o is not None:
                cls.cm_db.delete(o)
                return "Deletion. ok."
            else:
                return None
        finally:
            cls.cm_db.close()

    @classmethod
    def clear(cls):
        try:
            d = cls.cm_db.all(model.DEFAULT)
            for item in d:
                name = d[item]["name"]
                kind = model.DEFAULT
                cls.cm_db.delete_by_name(kind, name)
            cls.cm_db.save()
        finally:
            cls.cm_db.close()

    #
    # Set the default cloud
    #
    @classmethod
    def get_cloud(cls):
        o = cls.get("cloud", cloud="general")
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
