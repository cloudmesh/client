from __future__ import print_function

from cloudmesh_client.common import Printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.ListResource import ListResource


# noinspection PyBroadException
class Default(ListResource):
    """
    Cloudmesh contains the concept of defaults. Defaults can have
    categories (we will rename cloud to categories). A category can be a
    cloud name or the name 'general'. The category general is a 'global'
    name space and contains defaults of global value (in future we will
    rename the value to global).

    """

    cm = CloudmeshDatabase()
    """cm is  a static variable so that db is used uniformly."""

    @classmethod
    def list(cls,
             cloud=None,
             format="table",
             order=None,
             output=format):
        """
        lists the default values in the specified format.
        TODO: This method has a bug as it uses format and output,
        only one should be used.

        :param cloud: the category of the default value. If general is used
                      it is a special category that is used for global values.
        :param format: json, table, yaml, dict, csv
        :param order: The order in which the attributes are returned
        :param output: The output format.
        :return:
        """
        if order is None:
            order = ['user', 'cloud', 'name', 'value']
        try:
            if cloud is None:
                d = cls.cm.all("default")
            else:
                d = cls.cm.find('default', cloud=cloud)
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
        """
        sets the default value for a given category
        :param key: the dictionary key of the value to store it at.
        :param value: the value
        :param cloud: the name of the category
        :param user: the username to store this default value at.
        :return:
        """
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
                #cls.cm.update(o)
            cls.cm.save()
        except:
            return None

    @classmethod
    def get_object(cls, key, cloud="general"):
        """
        returns the first object that matches the key in teh Default
        database.

        :param key: The dictionary key
        :param cloud: The category
        :return:
        """
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
        """
        returns the value of the first objects matching the key
        with the given category.

        :param key: The dictionary key
        :param cloud: The category
        :return:
        """
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
        """
        deletes all default values in the database.
        :param key: The dictionary key
        :param cloud: The category
        :return:
        """
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
        """
        returns the cloud in teh category general
        :return:
        """
        o = cls.get("cloud", cloud="general")
        return o

    @classmethod
    def set_cloud(cls, value):
        """
        sets the cloud in the category general
        :param value: the cloud as defined in cloudmesh.yaml
        :return:
        """
        cls.set("cloud", value, cloud="general")

    #
    # Set the default image
    #

    @classmethod
    def set_image(cls, value, cloud):
        """
        sets the default image for a specific cloud.
        :param value: the image uuid or name
        :param cloud: the cloud
        :return:
        """
        cls.set("image", value, cloud)

    @classmethod
    def get_image(cls, cloud):
        """
        returns the image for a particular cloud
        :param cloud: the cloud
        :return:
        """
        return cls.get("image", cloud)

    #
    # Set the default flavor
    #

    @classmethod
    def set_flavor(cls, value, cloud):
        """
        sets the default flavor for a particular cloud
        :param value: teh flavor name or uuid
        :param cloud: the cloud
        :return:
        """
        cls.set("flavor", value, cloud)

    @classmethod
    def get_flavor(cls, cloud):
        """
        gets ths flavor default for a cloud
        :param cloud: the cloud
        :return:
        """
        return cls.get("flavor", cloud)

    #
    # Set the default group
    #

    @classmethod
    def set_group(cls, value):
        """
        sets the default group
        :param value: the group name
        :return:
        """
        cls.set("group", value, "general")



    @classmethod
    def get_group(cls):
        """
        get the default group
        :return:
        """
        return cls.get("group", "general")

    #
    # Set the default key
    #

    @classmethod
    def set_key(cls, value):
        """
        sets the default key
        :param value: the keyname
        :return:
        """
        cls.set("key", value, "general")

    @classmethod
    def get_key(cls):
        """
        get the default keyname
        :return:
        """
        return cls.get("key", "general")

    #
    # Set the default cluster
    #

    @classmethod
    def set_cluster(cls, value):
        """
        sets the default cluster
        :param value: the clustername as defined in the cloudmesh yaml file.
        :return:
        """
        cls.set("cluster", value, "general")

    @classmethod
    def get_cluster(cls):
        """
        gets the default cluster name.

        :return:
        """
        return cls.get("cluster", "general")
    #
    # Set the default key
    #

    @classmethod
    def set_debug(cls, value):
        """
        enables debugging
        :param value: True/False
        :return:
        """
        cls.set("debug", value, "general")

    @classmethod
    def get_debug(cls):
        """
        is dubugging switched on?
        :return:
        """
        return cls.get("debug", "general")

    @classmethod
    def debug(cls):
        """
        :return: returns True if debugging is on
        """
        return cls.get("debug", "general")


    #
    # Set the default key
    #

    @classmethod
    def set_refresh(cls, value):
        """
        sets the default for all clouds to refresh
        :param value:
        :return:
        """
        cls.set("refresh", value, "general")

    @classmethod
    def get_refresh(cls):
        """
        is refresh switched on?
        :return:
        """
        return cls.get("refresh", "general")

    @classmethod
    def refresh(cls):
        """
        :return: "on" if refresh is True, "off" otherwise
        """
        try:
            value = cls.get_refresh()
        except:
            cls.set_refresh("off")
            value = "off"
        return value == "on"
