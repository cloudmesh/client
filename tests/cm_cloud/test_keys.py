""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_keys.py:Test_keys.test_001

nosetests -v --nocapture

or

nosetests -v

"""
from __future__ import print_function

from pprint import pprint

import yaml
from cloudmesh_client.cloud.key import Key

from cloudmesh_client.cloud.iaas.provider.openstack.CloudProviderOpenstackAPI import CloudProviderOpenstackAPI
from cloudmesh_client import CloudmeshDatabase
from cloudmesh_client import ConfigDict
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.SSHkey import SSHkey
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default


# noinspection PyMethodMayBeStatic,PyMethodMayBeStatic,PyPep8Naming
class Test_keys:

    cm = CloudmeshDatabase()

    # noinspection PyTypeChecker
    data = dotdict({
        "cloud": Default.cloud,
        "username": ConfigDict("cloudmesh.yaml")["cloudmesh"]["github"]["username"]}
    )

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c="-")
        print(command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return result

    def setup(self):
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def clean_db(self):
        """create new db"""
        print ("clean db")
        self.cm.clean()
        result = self.run("cm default cloud={cloud}")
        result = self.run("cm default cloud")
        assert self.data.cloud in result

    def test_001(self):
        HEADING("reading the keys from ~/.ssh")

        banner("ssh keys")
        Key.get_from_dir("~/.ssh")
        mykeys = Key.all(output="dict")

        assert len(mykeys) > 0

    def test_002(self):
        HEADING("reading the keys from github")

        self.cm.clean()

        config = ConfigDict("cloudmesh.yaml")
        git_username = config['cloudmesh']['github']['username']

        banner("git hub")
        Key.get_from_git(git_username)

        mykeys = Key.all(output="dict")
        count1 = len(mykeys)

        banner("all")
        key= Key.get(git_username, output="dict")
        print (key)

        mykeys = Key.all(output="dict")
        count2 = len(mykeys)

        print(mykeys)

        Key.delete(name='github-0')


        mykeys = Key.all(output="table")

        print(mykeys)

        assert count1 > 0 and count2 > 0

    def test_003(self):
        HEADING("testing properties in SSHKey")

        sshkey = SSHkey("~/.ssh/id_rsa.pub")
        pprint(sshkey.key)
        print("Fingerprint:", sshkey.fingerprint)
        pprint(sshkey.__key__)
        print("sshkey", sshkey)
        print("str", str(sshkey))
        print(sshkey.type)
        assert True

    def test_004(self):
        HEADING()

        Key.delete()
        Key.add_from_path("~/.ssh/id_rsa.pub")

        d = Key.all(output="dict")
        print(d)

        print(Printer.write(d, output="table"))
        assert 'id_rsa.pub' in str(d)

        d = Key.find(name='rsa')
        print('find function: ', d)

        Key.delete(name='rsa')

        d = Key.all(output="dict")

        assert d is None

    def test_005(self):
        HEADING()
        print(Key.get_from_yaml())

    def test_101(self):
        """
        cm key add --name=testkey ~/.ssh/id_rsa.pub
        """
        HEADING()
        self.clean_db()
        result = self.run("cm key add testkey --source=~/.ssh/id_rsa.pub")
        result = self.run("cm key list")

        assert "OK." in result
        assert "testkey" in result
        assert "file:" in result

    def test_102(self):
        """
        cm key add --git --name=testkey ~/.ssh/id_rsa.pub
        """
        HEADING()
        self.clean_db()

        result = self.run("cm key add --git ")
        result = self.run("cm key list")

        username = "{username}_git".format(**self.data)

        assert username in result

    def test_103(self):
        """
        key add --ssh --name=testkey
        """
        HEADING()
        self.clean_db()
        result = self.run("cm key add testkey --ssh")
        result = self.run("cm key list")
        assert "OK." in result
        assert "testkey" in result
        assert "ssh" in result

    def test_105(self):
        """
        cm key list --source=db
        """

        HEADING()
        self.clean_db()
        result = self.run("cm key add testkey --ssh")
        result = self.run("cm key list --source=db")

        assert "testkey" in result
        assert "ssh" in result
        assert "OK." in result

    def test_106(self):
        """
        cm key list --source=db --format=json
        """

        HEADING()
        result = self.run("cm key list --source=db --format=json")
        print(result)
        assert "OK." in result
        assert "{" in result
        assert "testkey" in result

    def test_107(self):
        """
        cm key list --source=db --format=yaml
        """

        HEADING()
        result = self.run("cm key list --source=db --format=yaml")
        d = yaml.load(result.split("\n\n")[0])

        assert "OK." in result
        assert "testkey" in result

    def test_109(self):
        """
        cm key list --source=git
        """

        HEADING()
        result = self.run("cm key list --source=git")
        print(result)
        assert "github-" in result
        assert "OK." in result

    def test_110(self):
        """
        cm key list --source=cloudmesh
        """

        HEADING()
        result = self.run("cm key list --source=yaml")
        print(result)
        assert "OK." in result

    def test_111(self):
        """
        cm key list --source=ssh
        """

        HEADING()
        result = self.run("cm key list --source=ssh")
        assert "rsa" in result
        assert "OK." in result

    def test_112(self):
        """
        cm key list --source=cloudmesh
        """
        HEADING()
        result = self.run("cm key list --source=yaml")
        assert "ssh" in result
        assert "fingerprint" in result
        assert "OK." in result

    def test_113(self):
        """
        cm key get testkey
        """

        HEADING()
        result = self.run("cm key get testkey")
        assert "testkey" in result
        assert "OK." in result

    def test_114(self):
        """
        cm key default testkey
        """

        HEADING()
        result = self.run("cm default key=testkey")
        assert "ok." in result

        result = self.run("cm default key")
        assert "testkey" in result

    def test_115(self):
        """
        cm key delete testkey
        """

        HEADING()
        self.clean_db()
        result = self.run("cm key add testkey --ssh")
        result = self.run("cm key delete testkey")
        assert "testkey" in result
        assert "OK." in result

        result = self.run("cm key list")

        assert "No keys" in result
        assert "testkey" not in result

    def test_116(self):
        """
        cm key delete --all
        """

        HEADING()
        result = self.run("cm key add testkey --ssh")
        result = self.run("cm key delete --all --force")
        assert "OK." in result

    def test_117(self):
        HEADING()
        self.clean_db()
        result = self.run("cm key add testkey --ssh")
        result = self.run("cm key upload testkey")

        cloudname = self.data.cloud
        d = ConfigDict("cloudmesh.yaml")
        cloud_details = d["cloudmesh"]["clouds"][cloudname]

        cloud = CloudProviderOpenstackAPI(cloudname, cloud_details)


        d = cloud.list_key(cloudname)
        pprint(d)

        assert len(d) > 0
        result = self.run("cm key delete testkey --cloud={cloud}")
        assert 'OK' in result
