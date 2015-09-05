""" run with

python setup.py install; nosetests -v --nocapture  tests/test_keys.py:Test_keys.test_001

nosetests -v --nocapture

or

nosetests -v

"""

from pprint import pprint

from cloudmesh_client.keys.SSHKeyManager import SSHKeyManager
from cloudmesh_client.keys.SSHkey import SSHkey
from cloudmesh_client.db.SSHKeyDBManager import SSHKeyDBManager
from cloudmesh_client.common.tables import dict_printer

from cloudmesh_base.util import HEADING
from cloudmesh_base.util import banner


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
        mykeys.get_from_dir("~/.ssh")


        assert len(mykeys) > 0

    def test_002(self):
        """reading the keys from github"""
        HEADING()

        # from cloudmesh_client.common import cloudmesh_yaml
        #config = ConfigDict(filename=cloudmesh_yaml")
        #git_username = config['cloudmesh']['github']['username']
        git_username = 'laszewsk'

        mykeys = SSHKeyManager()

        banner("git hub")
        mykeys.get_from_git(git_username)

        count1 = len(mykeys)

        banner("all")
        mykeys.get_all(git_username)

        count2 = len(mykeys)

        # d = mykeys.dict()
        print (mykeys.table)

        mykeys.__delitem__('github-0')
        print (mykeys.table)

        assert count1 > 0 and count2 >0


    def test_003(self):
        """testing properties in SSHKey"""
        HEADING()


        sshkey = SSHkey("~/.ssh/id_rsa.pub")
        pprint (sshkey.key)
        print ("Fingerprint:", sshkey.fingerprint)
        pprint (sshkey.__key__)
        print ("sshkey", sshkey)
        print ("str", str(sshkey))
        print (sshkey.type)
        assert True

    def test_004(self):
        HEADING()
        sshdb = SSHKeyDBManager()
        sshdb.delete_all()
        sshdb.add("~/.ssh/id_rsa.pub")

        d = sshdb.dict()
        print d
        print dict_printer(d, output="table")

        d = sshdb.find('PauloR@bebop')
        print ('find function: ', d)

        sshdb.delete('PauloR@bebop')

        d = sshdb.object_to_dict(sshdb.find_all())
        print ("DICT", d)

    def test_005(self):
        HEADING()
        sshm = SSHKeyManager()
        print sshm.get_from_yaml()