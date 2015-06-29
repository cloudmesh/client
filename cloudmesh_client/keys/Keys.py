from cloudmesh_base.util import path_expand
from os.path import expanduser
import os
import requests
from pprint import pprint
from cloudmesh_client.keys.util import SSHkey
from prettytable import PrettyTable

class SSHkeys(object):

    def __init__(self):
        self.__keys__ = {}

    def add_from_file(self, filename):
        sshkey = SSHkey(filename)
        i = sshkey.comment
        self.__keys__[i] = sshkey

    def dict(self):
        r = {}
        for i in self.__keys__:
            k = self.__keys__[i].__key__['string']
            r[i] = k
        return r

    def print_dict(self, dict):
        x = PrettyTable(["Name", "Key"])
        x.align["Name"] = "l" # Left align city names
        x.padding_width = 1 # One space between column edges and contents (default)
        for i in dict:
            x.add_row([i,dict[i]])
        print x

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

            sshkey = SSHkey(location)
            i = sshkey.comment
            self.__keys__[i] = sshkey

            """
            with open(location) as f:
                s = f.read().rstrip()
            self.__keys__[file] = s
            """

    def get_from_git(self, username):
        """

        :param username: the github username
        :return: an array of public keys
        :rtype: list
        """
        content = requests.get('https://github.com/{:}.keys'.format(username)).text.split("\n")

        for key in range(0,len(content)):
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

            self.__keys__["github-"+str(key)] = sshkey


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




