""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_keys.py:Test_keys.test_001

nosetests -v --nocapture

or

nosetests -v

"""
from __future__ import print_function

from pprint import pprint

# from cloudmesh_client.keys.SSHKeyManager import SSHKeyManager
# from cloudmesh_client.keys.SSHkey import SSHkey
# from cloudmesh_client.db.SSHKeyDBManager import SSHKeyDBManager
# from cloudmesh_client.common.Printer import dict_printer

from cloudmesh_client.cloud.iaas.provider.openstack.CloudProviderOpenstackAPI import CloudProviderOpenstackAPI
from cloudmesh_client.util import HEADING
from cloudmesh_client.common.Shell import Shell
import os
from cloudmesh_client.util import banner
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.dotdict import dotdict

class Test_keys:

    data = dotdict({
        "cloud": "kilo",
        "username": ConfigDict("cloudmesh.yaml")["cloudmesh"]["github"]["username"]}
    )

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c ="-")
        print (command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return result


    def setup(self):
        pass

    def tearDown(self):
        pass


    def test_000(self):
        "create new db"
        command = "make db"
        result = self.run(command)
        assert "kilo" in result

    """
    def test_001(self):
        reading the keys from ~/.ssh
        HEADING()

        mykeys = SSHKeyManager()

        banner("ssh keys")
        mykeys.get_from_dir("~/.ssh")


        assert len(mykeys) > 0

    def test_002(self):
        reading the keys from github
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
        testing properties in SSHKey
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
    """

    '''
    def test_001(self):
        """
        cm key add --name=testkey ~/.ssh/id_rsa.pub
        """
        HEADING()
        os.system("make db")
        result = self.run("cm key add testkey --source=~/.ssh/id_rsa.pub")
        result = self.run("cm key list")


        assert "OK." in result
        assert "testkey" in result
        assert "file:" in result

    '''

    # #################################

    '''
    def test_002(self):
        """
        cm key add --git --name=testkey ~/.ssh/id_rsa.pub
        """
        HEADING()
        os.system("make db")
        result = self.run("cm key add --git ")
        result = self.run("cm key list")


        username = "{username}_github".format(**self.data)

        assert username in result



    def test_003(self):
        """
        key add --ssh --name=testkey
        """
        HEADING()
        os.system("make db")
        result = self.run("cm key add testkey --ssh")
        result = self.run("cm key list")
        assert "OK." in result
        assert "testkey" in result
        assert "ssh" in result


    '''



    def test_005(self):
        """
        cm key list --source=db
        """

        HEADING()
        result = self.run("cm key list --source=db")

        assert "testkey" in result
        assert "ssh" in result
        assert "OK." in result

    '''

    def test_006(self):
        """
        cm key list --source=db --format=json
        """

        HEADING()
        result = self.run("cm key list --source=db --format=json")
        print (result)
        assert "OK." in result

    def test_007(self):
        """
        cm key list --source=db --format=yaml
        """

        HEADING()
        result = self.run("cm key list --source=db --format=yaml")
        print (result)
        assert "OK." in result

    def test_008(self):
        """
        cm key list --source=db --format=yaml
        """

        HEADING()
        result = self.run("cm key list --source=db --format=yaml")
        print (result)
        assert "OK." in result

    def test_009(self):
        """
        cm key list --source=git
        """

        HEADING()
        result = self.run("cm key list --source=git")
        print (result)
        assert "OK." in result

    def test_010(self):
        """
        cm key list --source=cloudmesh
        """

        HEADING()
        result = self.run("cm key list --source=cloudmesh")
        print (result)
        assert "OK." in result

    def test_011(self):
        """
        cm key list --source=ssh
        """

        HEADING()
        result = self.run("cm key list --source=ssh")
        print (result)
        assert "OK." in result

    def test_012(self):
        """
        cm key list --source=cloudmesh
        """

        HEADING()
        result = self.run("cm key list --source=cloudmesh")
        print (result)
        assert "OK." in result

    def test_013(self):
        """
        cm key get testkey
        """

        HEADING()
        result = self.run("cm key get testkey")
        print (result)
        assert "OK." in result

    def test_014(self):
        """
        cm key default testkey
        """

        HEADING()
        result = self.run("cm key default testkey")
        print (result)
        assert "OK." in result

    def test_015(self):
        """
        cm key delete testkey
        """

        HEADING()
        result = self.run("cm key delete testkey")
        print (result)
        assert "OK." in result

    def test_016(self):
        """
        cm key delete --all
        """

        HEADING()
        result = self.run("cm key add --name=testkey ~/.ssh/id_rsa.pub")
        result = self.run("cm key delete --all --force")
        print (result)
        assert "OK." in result
    '''

    '''
    def test_17(self):
        cloudname = 'kilo'
        d = ConfigDict("cloudmesh.yaml")
        cloud_details = d["cloudmesh"]["clouds"][cloudname]

        cloud = CloudProviderOpenstackAPI(cloudname, cloud_details)

        d = cloud.list_key(cloudname)
        pprint (d)

        assert len(d) > 0
    '''