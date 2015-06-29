from cloudmesh_base.util import path_expand
from os.path import expanduser
import os
import requests
from pprint import pprint

class SSHkeys(object):

    def __init__(self):
        self.__keys__ = {}

    def __add__(self, other):
        if type(other) != SSHkey:
            raise Exception("type must be SSHkey")
        else:
            print ("TODO")

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

    def get_from_dir(self, directory):
        files = [file for file in os.listdir(expanduser(path_expand(directory)))
                if file.lower().endswith(".pub")]
        public_keys = {}
        for file in files:
            location = path_expand("{:}/{:}".format(directory,file))
            with open(location) as f:
                s = f.read().rstrip()
            self.__keys__[file] = s

    def get_from_git(self, username):
        """

        :param username: the github username
        :return: an array of public keys
        :rtype: list
        """
        content = requests.get('https://github.com/{:}.keys'.format(username)).text.split("\n")
        keys = {}
        for key in range(0,len(content)):
            self.__keys__["github-"+str(key)] = content[key]


    def get_all(self, username):
        self.get_from_dir("~/.ssh")
        self.get_from_git(username)

if __name__ == "__main__":

    from cloudmesh_base.util import banner

    mykeys = SSHkeys()
    mykeys.get_all("laszewsk")

    banner("ssh keys")

    print(mykeys)
    print(mykeys.keys())

    print(mykeys['id_rsa.pub'])
    print (len(mykeys))




