from __future__ import print_function

from os.path import expanduser
import os

from cloudmesh_client.common.ConfigDict import Config
import requests
from cloudmesh_base.menu import menu_return_num
from cloudmesh_client.keys.SSHkey import SSHkey
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.shell.console import Console


class SSHKeyManager(object):
    def __init__(self):
        self.__keys__ = {}

    def add_from_file(self, file_path, keyname=None):
        sshkey = SSHkey(file_path, keyname)
        self.add_from_object(sshkey)

    def add_from_object(self, sshkey_obj):
        i = sshkey_obj.__key__['name']
        self.__keys__[i] = sshkey_obj.__key__

    @property
    def table(self):
        d = dict(self.__keys__)
        return (dict_printer(d,
                             order=["comment",
                                    "uri",
                                    "fingerprint"],
                             output="table",
                             sort_keys=True))

    def __delitem__(self, key):
        del self.__keys__[key]

    def __repr__(self):
        return self.__keys__

    def __str__(self):
        return str(self.__keys__)

    def keys(self):
        return self.__keys__.keys()

    def __getitem__(self, item):
        return self.__keys__[item]

    def __len__(self):
        return len(self.keys())

    def select(self):
        options = []
        for i in self.__keys__:
            print('i:', i)
            line = '{}: {}'.format(self.__keys__[i]['comment'], self.__keys__[i]['fingerprint'])
            options.append(line)
        return menu_return_num('KEYS', options)

    # noinspection PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember,PyProtectedMember
    def get_from_yaml(self, filename=None, load_order=None):
        """
        :param filename: name of the yaml file
        :return: a SSHKeyManager (dict of keys)
        """
        if filename is None:
            # default = Config.path_expand(os.path.join("~", ".cloudmesh", "cloudmesh.yaml"))
            # config = ConfigDict("cloudmesh.yaml")
            filename = "cloudmesh.yaml"
            config = ConfigDict(filename)
        elif load_order:
            config = ConfigDict(filename, load_order)
        else:
            Console.error("Wrong arguments")
        config_keys = config["cloudmesh"]["keys"]
        default = config_keys["default"]
        keylist = config_keys["keylist"]
        sshmanager = SSHKeyManager()
        for key in keylist.keys():
            keyname = key
            value = keylist[key]
            if os.path.isfile(Config.path_expand(value)):
                path = Config.path_expand(value)
                sshmanager.add_from_file(path, keyname)
            else:
                sshkey = SSHkey()
                uri = Config.path_expand(os.path.join("~", ".cloudmesh", filename))
                sshkey.__key__['uri'] = 'yaml://{}'.format(uri)
                sshkey.__key__['string'] = value
                (sshkey.__key__['type'],
                 sshkey.__key__['key'],
                 sshkey.__key__['comment']) = sshkey._parse(sshkey.__key__['string'])
                sshkey.__key__['fingerprint'] = sshkey._fingerprint(sshkey.__key__['string'])
                sshkey.__key__['name'] = keyname
                sshmanager.add_from_object(sshkey)
        return sshmanager
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

    def get_from_dir(self, directory=None):
        directory = directory or Config.path_expand("~/.ssh")
        files = [file for file in os.listdir(expanduser(Config.path_expand(directory)))
                 if file.lower().endswith(".pub")]
        for file in files:
            location = Config.path_expand("{:}/{:}".format(directory, file))

            sshkey = SSHkey(location)
            i = sshkey.comment
            self.__keys__[i] = sshkey.__key__

    # noinspection PyProtectedMember
    def get_from_git(self, username):
        """

        :param username: the github username
        :return: an array of public keys
        :rtype: list
        """
        uri = 'https://github.com/{:}.keys'.format(username)
        content = requests.get(uri).text.split("\n")

        for key in range(0, len(content)):
            value = content[key]
            sshkey = SSHkey(None)
            sshkey.__key__ = {
                'uri': uri,
                'string': value
            }
            (sshkey.__key__['type'],
             sshkey.__key__['key'],
             sshkey.__key__['comment']) = sshkey._parse(sshkey.__key__['string'])
            sshkey.__key__['fingerprint'] = sshkey._fingerprint(sshkey.__key__['string'])
            name = "github-" + str(key)
            sshkey.__key__['comment'] = name
            sshkey.__key__['Id'] = name
            self.__keys__[name] = sshkey.__key__

    def get_all(self, username):
        self.get_from_dir("~/.ssh")
        self.get_from_git(username)


if __name__ == "__main__":
    print ("HALLO")
    from cloudmesh_base.util import banner

    mykeys = SSHKeyManager()
    mykeys.get_all("laszewsk")

    banner("ssh keys")

    print(mykeys)
    print(mykeys.keys())

    print("GIT")
    mykeys = SSHKeyManager()
    mykeys.get_from_git("laszewsk")
    print(mykeys)
    print(mykeys.keys())

    #    print(mykeys['id_rsa.pub'])
#    print (len(mykeys))
