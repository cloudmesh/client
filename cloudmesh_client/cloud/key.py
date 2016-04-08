from __future__ import print_function
from cloudmesh_client.common.ConfigDict import ConfigDict

from cloudmesh_client.common.todo import TODO
# add imports for other cloud providers in future
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.Error import Error
from uuid import UUID
from cloudmesh_client.common.dotdict import dotdict
from builtins import input
from pprint import pprint
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.default import Default
from cloudmesh_client.common.menu import menu_return_num
from cloudmesh_client.common.SSHkey import SSHkey

# noinspection PyPep8Naming
class Key(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def info(cls, **kwargs):
        raise NotImplementedError()


    @classmethod
    def list(cls, category=None, live=False, format="table"):

        (order, header) = CloudProvider(cloud).get_attributes("key")

        return Printer.write(keys,
                             order=order,
                             header=header,
                             output=format)



    @classmethod
    def list_on_cloud(cls, cloud, live=False, format="table"):
        """
        This method lists all flavors of the cloud
        :param cloud: the cloud name
        """
        try:
            print("FKHJGCFKYTRCK")
            keys = CloudProvider(cloud).provider.list_key(cloud)
            print("KKKKK", keys)
            if keys is None or keys is []:
                return None

            (order, header) = CloudProvider(cloud).get_attributes("key")

            return Printer.write(keys,
                                 order=order,
                                 header=header,
                                 output=format)
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def clear(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def refresh(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def delete(cls, name, cloud=None):
        if cloud is not None:
            result = CloudProvider(cloud).provider.delete_key_from_cloud(name)

    @classmethod
    def all(cls, output="dict"):
        return cls.cm.get(kind="key")

    @classmethod
    def get(cls, name=None, output="dict"):
        """
        Finds the key on the database by name

        :param name: name of the key to be found
        :return: Query object of the search
        """
        if name is None:
            return cls.cm.find(kind="key", output=output)
        else:
            return cls.cm.find(kind="key", name=name, output=output, scope="first")

    @classmethod
    def set_default(cls, name):
       Default.set_key(name)

    # deprecated use Default.key
    @classmethod
    def get_default(cls):
        return Default.key

    @classmethod
    def delete_from_cloud(cls, name, cloud=None):
        pass


    @classmethod
    def _delete_from_db(cls, name=None):
        if name is None:
            cls.cm.delete(kind='key')
        else:
            cls.cm.delete(kind='key', name=name)

    @classmethod
    def select(cls):
        options = []
        d = cls.get(output='dict')
        for i in d:
            line = '{}: {}'.format(d[i]['name'], d[i]['fingerprint'])
            options.append(line)
        num = menu_return_num('KEYS', options)
        if num != 'q':
            return options[num]
        return num

    #
    # ADD
    #
    @classmethod
    def _add_from_path(cls,
                       path,
                       keyname=None,
                       user=None,
                       source=None,
                       uri=None):
        """
        Adds the key to the database based on the path

        :param keyname: name of the key or path to the key
        :return:
        """

        user = user or cls.cm.user

        sshkey = SSHkey(Config.path_expand(path))

        cls._add_from_sshkey(sshkey.__key__,
                             keyname,
                             user,
                             source=source,
                             uri=uri)

    @classmethod
    def _add_from_sshkey(cls,
                         sshkey,
                         keyname=None,
                         user=None,
                         source=None,
                         uri=None):


        user = user or cls.cm.user

        if keyname is None:
            try:
                keyname = sshkey['name']
            except:
                pass
        if keyname is None:
            print("ERROR: keyname is None")

        print("YYYYY", sshkey)

        thekey = {
            "name": keyname,
            "uri": sshkey['uri'],
            "source": sshkey['source'],
            "fingerprint": sshkey['fingerprint'],
            "comment": sshkey['comment'],
            "value": sshkey['string'],
            "category": "general",
            "user": user}

        key_obj = cls.cm.add(key)

        # pprint(key_obj.__dict__)
        cls._add(key_obj)
