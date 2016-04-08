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
import os
from os.path import expanduser
import requests


# noinspection PyPep8Naming
class Key(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def info(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def get_from_dir(cls, directory=None, store=False):
        directory = directory or Config.path_expand("~/.ssh")
        files = [file for file in os.listdir(expanduser(Config.path_expand(directory)))
                 if file.lower().endswith(".pub")]
        d = []
        for file in files:
            location = Config.path_expand("{:}/{:}".format(directory, file))

            sshkey = SSHkey(location).get()

            i = sshkey["comment"]
            if i is not None:
                i = i.replace("@", "_")
                i = i.replace("-", "_")
                i = i.replace(" ", "_")
                i = i.replace(".", "_")
            else:
                # use base name
                i = file.replace(".pub", "")
            sshkey["kind"] = "key"
            sshkey["source"] = 'file'

            # print("UUUU", sshkey)
            if store:
                cls._add_from_sshkey(
                    dict(sshkey),
                    keyname=sshkey["name"],
                    source=sshkey["source"],
                    uri=sshkey["uri"])
            else:
                d.append(dict(sshkey))
        if not store:
            return d

    @classmethod
    def get_from_git(cls, username, store=True):
        """

        :param username: the github username
        :return: an array of public keys
        :rtype: list
        """
        uri = 'https://github.com/{:}.keys'.format(username)
        content = requests.get(uri).text.strip("\n").split("\n")

        d = []
        print (len(content))
        for key in range(0, len(content)):
            value = content[key]
            thekey = {}

            name = "{}_git_{}".format(username, key)

            thekey = {
                'uri': uri,
                'string': value,
                'fingerprint': SSHkey._fingerprint(value),
                'name': name,
                'comment': name,
                'cm_id': name,
                'source': 'git',
                'kind': 'key'
            }

            thekey["type"], thekey["key"], thekey["comment"] = SSHkey._parse(value)

            if thekey["comment"] is None:
                thekey["comment"] = name
            d.append(thekey)
            if store:
                try:

                    cls.cm.add(thekey)
                except:
                    Console.error("Key already in db", traceflag=False)
        if not store:
            return d
                # noinspection PyProtectedMember,PyUnreachableCode,PyUnusedLocal

    @classmethod
    def get_from_yaml(cls, filename=None, load_order=None, store=True):
        """
        :param filename: name of the yaml file
        :return: a SSHKeyManager (dict of keys)
        """
        config = None
        if filename is None:
            # default = Config.path_expand(os.path.join("~", ".cloudmesh", "cloudmesh.yaml"))
            # config = ConfigDict("cloudmesh.yaml")
            filename = "cloudmesh.yaml"
            config = ConfigDict(filename)
        elif load_order:
            config = ConfigDict(filename, load_order)
        else:
            Console.error("Wrong arguments")
            return
        config_keys = config["cloudmesh"]["keys"]
        default = config_keys["default"]
        keylist = config_keys["keylist"]

        uri = Config.path_expand(os.path.join("~", ".cloudmesh", filename))


        print ("IIIII", keylist)
        d = []
        for key in list(keylist.keys()):
            keyname = key
            value = keylist[key]
            if os.path.isfile(Config.path_expand(value)):
                path = Config.path_expand(value)
                if store:
                    Key.add_from_path(path, keyname)
                else:
                    d.append(Key.add_from_path(path, keyname, store=False))
            else:

                keytype, string, comment = SSHkey._parse(value)
                thekey = {
                    'uri': 'yaml://{}'.format(uri),
                    'string': value,
                    'fingerprint': SSHkey._fingerprint(value),
                    'name': keyname,
                    'comment': comment,
                    'source': 'git',
                    'kind': 'key'
                }

                thekey["type"], thekey["key"], thekey["comment"] = SSHkey._parse(value)

                if thekey["comment"] is None:
                    thekey["comment"] = keyname
                if store:
                    try:
                        cls.cm.add(thekey)
                    except:
                        Console.error("Key already in db", traceflag=False)
                else:
                    d.append(thekey)
        if not store:
            return d



        """
        take a look into original cloudmesh code, its possible to either specify a key or a filename
        the original one is able to figure this out and do the rightthing. We may want to add this
        logic to the SSHkey class, so we can initialize either via filename or key string.
        It would than figure out the right thing

        cloudmesh:
          keys:
            idrsa: ~/.ssh/id_rsa.pub

        cloudmesh:
        ...
          keys:
            default: name of the key
            keylist:
              keyname: ~/.ssh/id_rsa.pub
              keyname: ssh rsa hajfhjldahlfjhdlsak ..... comment
              github-x: github
        """


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

        pprint(sshkey)

        thekey = {
            "kind": "key",
            "name": keyname,
            "uri": sshkey['uri'],
            "source": sshkey['source'],
            "fingerprint": sshkey['fingerprint'],
            "comment": sshkey['comment'],
            "value": sshkey['string'],
            "category": "general",
            "user": user}

        cls.cm.add(thekey)

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
    def delete(cls, name=None, cloud=None):
        if cloud is not None:
            result = CloudProvider(cloud).provider.delete_key_from_cloud(name)
        if name is None:
            cls.cm.delete(kind="key", provider="general")
        else:
            cls.cm.delete(name=name, kind="key", provider="general")

    @classmethod
    def all(cls, output="dict"):
        return cls.cm.find(kind="key", scope="all", output=output)


    @classmethod
    def find(cls, name=None, output="dict"):
        return cls.get(name=name, output=output)

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
    def add_from_path(cls,
                      path,
                      keyname=None,
                      user=None,
                      source=None,
                      uri=None,
                      store=True):
        """
        Adds the key to the database based on the path

        :param keyname: name of the key or path to the key
        :return:
        """

        user = user or cls.cm.user

        sshkey = SSHkey(Config.path_expand(path))

        if store:
            cls._add_from_sshkey(sshkey.__key__,
                             keyname,
                             user,
                             source=source,
                             uri=uri)
        else:
            return sshkey.__key__