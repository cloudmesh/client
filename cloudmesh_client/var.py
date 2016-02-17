from __future__ import print_function

from cloudmesh_client.common import Printer
# from cloudmesh_client.db.SSHKeyDBManager import SSHKeyDBManager
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.ConfigDict import ConfigDict


# noinspection PyBroadException
class Var(ListResource):
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
             format="table",
             order=None,
             output=format):
        """
        lists the default values in the specified format.
        TODO: This method has a bug as it uses format and output,
        only one should be used.

        :param category: the category of the default value. If general is used
                      it is a special category that is used for global values.
        :param format: json, table, yaml, dict, csv
        :param order: The order in which the attributes are returned
        :param output: The output format.
        :return:
        """
        if order is None:
            order = ['name', 'value', 'user']
        try:
            d = cls.cm.all("var")
            return (Printer.dict_printer(d,
                                         order=order,
                                         output=format))
        except:
            return None

    #
    # GENERAL SETTER AND GETTER METHOD
    #

    @classmethod
    def set(cls, key, value, user=None):
        """
        sets the default value for a given category
        :param key: the dictionary key of the value to store it at.
        :param value: the value
        :param user: the username to store this default value at.
        :return:
        """
        try:
            o = cls.get_object(key)

            me = cls.cm.user or user
            if o is None:
                o = cls.cm.db_obj_dict('var',
                                       name=key,
                                       value=value,
                                       category="var",
                                       user=me)
                cls.cm.add_obj(o)
            else:
                o.value = value
                cls.cm.add(o)
                # cls.cm.update(o)
            cls.cm.save()
        except:
            return None

    @classmethod
    def get_object(cls, key):
        """
        returns the first object that matches the key in teh Default
        database.

        :param key: The dictionary key
        :param category: The category
        :return:
        """
        try:
            arguments = {'name': key}
            o = cls.cm.find('var',
                            output='object',
                            **arguments).first()
            return o
        except Exception:
            return None

    @classmethod
    def get(cls, key):
        """
        returns the value of the first objects matching the key
        with the given category.

        :param key: The dictionary key
        :param category: The category
        :return:
        """
        arguments = {'name': key}
        o = cls.cm.find('var',
                        output='dict',
                        scope='first',
                        **arguments)
        if o is not None:
            return o['value']
        else:
            return None

    @classmethod
    def delete(cls, key):
        try:
            o = Var.get_object(key)
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
        :return:
        """
        try:
            d = cls.cm.all('var')
            for item in d:
                name = d[item]["name"]
                cls.cm.delete_by_name('var', name)
            cls.cm.save()
        except:
            return None

