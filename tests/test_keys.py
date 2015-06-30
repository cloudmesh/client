""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_base.util import HEADING
import os
from cloudmesh_base.util import banner
from cloudmesh_client.keys.SSHKeyManager import SSHKeyManager
from cloudmesh_client.keys.SSHkey import SSHkey
from pprint import pprint
from cloudmesh_client.db.models import dict_printer

class Test_keys:
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """reading the keys from ~/.ssh"""
        HEADING()

        mykeys = SSHKeyManager()

        banner("ssh keys")
        pprint (SSHKeyManager.find_in_dir("~/.ssh"))

        assert True

    def test_002(self):
        """reading the keys from github"""
        HEADING()

        #config = ConfigDict(filename="~/.cloudmesh/cloudmesh.yaml")
        #git_username = config['cloudmesh']['github']['username']
        git_username = 'laszewsk'

        mykeys = SSHKeyManager()

        banner("git hub")
        pprint (SSHKeyManager.get_key_from_git(git_username))

        banner("all")
        pprint (SSHKeyManager.get_all_keys(git_username))

        assert True


    def test_003(self):
        """testing properties in SSHKey"""
        HEADING()

        try:
            sshkey = SSHkey("~/.ssh/id_rsa.pub")
            pprint (sshkey.key)
            print ("Fingerprint:", sshkey.fingerprint)
            pprint (sshkey.__key__)
            print ("sshkey", sshkey)
            print ("str", str(sshkey))
            print (sshkey.type)
            assert False
        except Exception:
            assert True

    def test_003(self):

        HEADING()
        mykeys = SSHKeyManager()
        #mykeys.get_from_dir("~/.ssh")
        git_username = 'laszewsk'
        mykeys.get_all(git_username)
        d = mykeys.dict()
        mykeys.print_dict(d)