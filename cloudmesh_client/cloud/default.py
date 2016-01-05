from __future__ import print_function

from cloudmesh_client.common import Printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.ListResource import ListResource


# noinspection PyBroadException
class Default(ListResource):
    cm = CloudmeshDatabase()
    # Create a static variable so that db is initialized once in a transaction

    @classmethod
    def list(cls,
             cloud=None,
             format="table",
             order=None,
             output=format):
        if order is None:
            order = ['user', 'cloud', 'name', 'value']
        try:
            if cloud is None:
                d = cls.cm.all("default")
            else:
                d = cls.cm.find('default', cloud=cloud)
            from pprint import pprint
            pprint (d)
            return (Printer.dict_printer(d,
                                         order=order,
                                         output=format))
        except:
            return None

    #
    # GENERAL SETTER AND GETTER METHOD
    #

    @classmethod
    def set(cls, key, value, cloud=None, user=None):
        try:
            o = Default.get_object(key, cloud)

            me = cls.cm.user or user
            if o is None:
                o = cls.cm.db_obj_dict('default',
                                       name=key,
                                       value=value,
                                       cloud=cloud,
                                       user=me)
                cls.cm.add_obj(o)
            else:
                o.value = value
                cls.cm.add(o)
            cls.cm.save()
        except:
            return None

    @classmethod
    def get_object(cls, key, cloud="general"):
        try:
            arguments = {'name': key,
                         'cloud': cloud}
            o = cls.cm.find('default',
                            output='object',
                            **arguments).first()
            return o
        except Exception, e:
            return None

    @classmethod
    def get(cls, key, cloud="general"):
        arguments = {'name': key,
                     'cloud': cloud}
        o = cls.cm.find('default',
                        output='dict',
                        scope='first',
                        **arguments)
        if o is not None:
            return o['value']
        else:
            return None

    @classmethod
    def delete(cls, key, cloud):
        #
        # TODO: this is wrong implemented,
        #
        try:
            o = Default.get_object(key, cloud)
            if o is not None:
                cls.cm.delete(o)
                return "Deletion. ok."
            else:
                return None
        except:
            return None

    @classmethod
    def clear(cls):
        try:
            d = cls.cm.all('default')
            for item in d:
                name = d[item]["name"]
                cls.cm.delete_by_name('default', name)
            cls.cm.save()
        except:
            return None

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

    #
    # Set the default cluster
    #

    @classmethod
    def set_cluster(cls, value):
        cls.set("cluster", value, "general")

    @classmethod
    def get_cluster(cls):
        return cls.get("cluster", "general")
