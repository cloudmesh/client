from cloudmesh_base.util import path_expand
from os.path import expanduser
import os
import requests
from pprint import pprint

class SSHkeys(object):

    @staticmethod
    def find_in_dir(directory):
        files = [file for file in os.listdir(expanduser(path_expand(directory)))
                if file.lower().endswith(".pub")]
        public_keys = {}
        for file in files:
            location = path_expand("{:}/{:}".format(directory,file))
            with open(location) as f:
                s = f.read().rstrip()
            public_keys[file] = s
        return public_keys

    @staticmethod
    def get_key_from_git(username):
        """

        :param username: the github username
        :return: an array of public keys
        :rtype: list
        """
        content = requests.get('https://github.com/{:}.keys'.format(username)).text.split("\n")
        keys = {}
        for key in range(0,len(content)):
            keys["github-"+str(key)] = content[key]
        return keys

    @staticmethod
    def get_all_keys(username):
        ssh_keys = SSHkeys.find_in_dir("~/.ssh")
        git_keys = SSHkeys.get_key_from_git(username)
        z = ssh_keys.copy()
        z.update(git_keys)
        return z



mykeys = SSHkeys()


pprint (SSHkeys.find_in_dir("~/.ssh"))

pprint (SSHkeys.get_key_from_git('laszewsk'))

print ("------")
pprint (SSHkeys.get_all_keys('laszewsk'))


