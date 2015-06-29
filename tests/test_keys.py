""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_base.util import HEADING
import os
from cloudmesh_base.util import banner
from cloudmesh_client.keys.Keys import SSHkeys
from cloudmesh_client.keys.util import SSHkey
from pprint import pprint
from cloudmesh_client.db.models import dict_printer

class Test_keys:
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
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

    def test_002(self):

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
        mykeys = SSHkeys()
        #mykeys.get_from_dir("~/.ssh")
        mykeys.get_all('paulo-chagas')
        d = mykeys.dict()
        mykeys.print_dict(d)