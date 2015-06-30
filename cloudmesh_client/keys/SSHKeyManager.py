from __future__ import print_function
from cloudmesh_base.util import path_expand
from os.path import expanduser
import os
import requests
from pprint import pprint
from cloudmesh_client.keys.SSHkey import SSHkey
from prettytable import PrettyTable
from cloudmesh_client.common.tables import dict_printer

class SSHKeyManager(object):
    def __init__(self):
        self.__keys__ = {}

    def add_from_file(self, filename):
        sshkey = SSHkey(filename)
        i = sshkey.comment
        self.__keys__[i] = sshkey.__key__
        print(self.__keys__)


    @property
    def table(self):
        d = dict(self.__keys__)
        return (dict_printer(d,
                            order=["comment", "fingerprint"],
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

    def get_from_yaml(self, filename):
        # TODO
        print("not implemented")
        config = ConfigDict("~/.cloudmesh/cloudmesh.yaml")
        clouds = config["cloudmesh"]["clouds"]
        for key in clouds.keys():
            Console.ok("  " + key)
        """
        take a look into original cloudmesh code, its possible to either specify a key or a filename
        the original one is able to figure this out and do the rightthing. We may want to add this
        logic to the SSHkey class, so we can initialize either via filename or key string.
        It would than figure out the right thing

        cloudmesh:
          keys:
            idrsa: ~/.ssh/id_rsa.pub
        """

    def get_from_dir(self, directory):
        files = [file for file in os.listdir(expanduser(path_expand(directory)))
                 if file.lower().endswith(".pub")]
        for file in files:
            location = path_expand("{:}/{:}".format(directory, file))

            sshkey = SSHkey(location)
            i = sshkey.comment
            self.__keys__[i] = sshkey.__key__

    def get_from_git(self, username):
        """

        :param username: the github username
        :return: an array of public keys
        :rtype: list
        """
        content = requests.get('https://github.com/{:}.keys'.format(username)).text.split("\n")

        for key in range(0, len(content)):
            value = content[key]
            sshkey = SSHkey(None)
            sshkey.filename = None
            sshkey.__key__ = {}
            sshkey.__key__['filename'] = None
            sshkey.__key__['string'] = value
            (sshkey.__key__['type'],
             sshkey.__key__['key'],
             sshkey.__key__['comment']) = sshkey._parse(sshkey.__key__['string'])
            sshkey.__key__['fingerprint'] = sshkey._fingerprint(sshkey.__key__['string'])
            name = "github-" + str(key)
            self.__keys__[name] = sshkey.__key__
            sshkey.__key__['comment'] = name
            sshkey.__key__['Id'] = name

    def get_all(self, username):
        self.get_from_dir("~/.ssh")
        self.get_from_git(username)


if __name__ == "__main__":
    from cloudmesh_base.util import banner

    mykeys = SSHKeyManager()
    mykeys.get_all("laszewsk")

    banner("ssh keys")

    print(mykeys)
    print(mykeys.keys())

    print(mykeys['id_rsa.pub'])
    print (len(mykeys))
