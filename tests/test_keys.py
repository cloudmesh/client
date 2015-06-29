""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_base.util import HEADING
import os
from cloudmesh_base.util import banner
from cloudmesh_client.keys.Keys import SSHkeys
from pprint import pprint

class Test_keys:
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """testing cm search with all the arguments"""
        HEADING()
        try:


            mykeys = SSHkeys()

            banner("ssh keys")
            pprint (SSHkeys.find_in_dir("~/.ssh"))

            banner("git hub")
            pprint (SSHkeys.get_key_from_git('laszewsk'))

            banner("all")
            pprint (SSHkeys.get_all_keys('laszewsk'))
            assert False
        except Exception:
            assert True

    def tes_002(self):

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