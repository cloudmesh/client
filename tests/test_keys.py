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

def run3():
    sshkey = SSHkey("~/.ssh/id_rsa.pub")
    pprint (sshkey.key)
    print ("Fingerprint:", sshkey.fingerprint)
    pprint (sshkey.__key__)
    print ("sshkey", sshkey)
    print ("str", str(sshkey))
    print (sshkey.type)
    return "ok"

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
        result = mykeys.get_from_dir("~/.ssh")
        assert "ok" in result

    def test_002(self):
        """reading the keys from github"""
        HEADING()

        #config = ConfigDict(filename="~/.cloudmesh/cloudmesh.yaml")
        #git_username = config['cloudmesh']['github']['username']
        git_username = 'laszewsk'

        mykeys = SSHKeyManager()

        banner("git hub")
        result1 = mykeys.get_from_git(git_username)

        banner("all")
        result2 = mykeys.get_all(git_username)

        d = mykeys.dict()
        mykeys.print_dict(d)

        assert 'ok' in (result1,result2)


    def test_003(self):
        """testing properties in SSHKey"""
        HEADING()

        result = run3()
        assert 'ok' in result
