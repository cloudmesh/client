from __future__ import print_function

from cloudmesh_client.db import model
from cloudmesh_client.common import Printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.ListResource import ListResource


class Default(ListResource):
    cm = CloudmeshDatabase()
    # Create a static variable so that db is initialized once in a transaction

    @classmethod
    def list(cls,
             format="table",
             order=['user', 'cloud', 'name', 'value'],
             output=format):

        try:
            d = cls.cm.all("default")
            return (Printer.dict_printer(d,
                                         order=order,
                                         output=format))
        finally:
            cls.cm.close()

    @classmethod
    def get_objects(cls,
                    cloud,
                    format="table",
                    order=['user', 'cloud', 'name', 'value']):
        try:
            d = cls.cm.find_and_convert('default', cloud=cloud)
            return (Printer.dict_printer(d,
                                         order=order,
                                         output=format))
        finally:
            cls.cm.close()

    #
    # GENERAL SETTER AND GETTER METHOD
    #

    @classmethod
    def set(cls, key, value, cloud=None, user=None):
        try:
            o = Default.get_object(key, cloud)
            me = cls.cm.user or user
            if o is None:
                o = model.DEFAULT(key, value, cloud=cloud, user=me)
            else:
                o.value = value
            cls.cm.add(o)
        finally:
            cls.cm.close()

    @classmethod
    def get_object(cls, key, cloud=None):
        try:
            which_cloud = cloud or "general"
            kwargs = {'name': key,
                      'cloud': which_cloud}
            o = cls.cm.find('default', output='object', **kwargs).first()
            return o
        finally:
            cls.cm.close()

    @classmethod
    def get(cls, key, cloud=None):
        try:
            result = cls.get_object(key, cloud=cloud)
            if result is None:  # TODO: Verify if this is needed
                if key == 'cloud':
                    return 'general'
                elif key == 'group':
                    return 'default'
                return None
            else:
                return result.value

        finally:
            cls.cm.close()

    @classmethod
    def delete(cls, key, cloud):
        try:
            o = Default.get_object(key, cloud)
            if o is not None:
                cls.cm.delete(o)
                return "Deletion. ok."
            else:
                return None
        finally:
            cls.cm.close()

    @classmethod
    def clear(cls):
        try:
            d = cls.cm.all(model.DEFAULT)
            for item in d:
                name = d[item]["name"]
                kind = model.DEFAULT
                cls.cm.delete_by_name(kind, name)
            cls.cm.save()
        finally:
            cls.cm.close()

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
