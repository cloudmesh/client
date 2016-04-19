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
        "username": ConfigDict("cloudmesh.yaml")["cloudmesh"]["github"]["username"],
        "key": Default.user
    }
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
        print("clean db")
        self.cm.clean()
        result = self.run("cm default cloud={cloud}")
        result = self.run("cm default cloud")
        assert self.data.cloud in result

    def test_001(self):
        HEADING("clen")
        self.cm.clean()

    def test_002(self):
        HEADING("reading the keys from ~/.ssh")

        banner("ssh keys")
        Key.get_from_dir("~/.ssh")
        mykeys = Key.all(output="dict")

        assert len(mykeys) > 0

    def test_003(self):
        HEADING("reading the keys from github")

        self.cm.clean()

        config = ConfigDict("cloudmesh.yaml")
        git_username = config['cloudmesh']['github']['username']

        banner("git hub")
        Key.get_from_git(git_username)

        mykeys = Key.all(output="dict")
        count1 = len(mykeys)

        banner("all")
        key = Key.get(git_username, output="dict")
        print(key)

        mykeys = Key.all(output="dict")
        count2 = len(mykeys)

        print(mykeys)

        Key.delete(name='github-0')

        mykeys = Key.all(output="table")

        print(mykeys)

        assert count1 > 0 and count2 > 0

    def test_004(self):
        HEADING("testing properties in SSHKey")

        sshkey = SSHkey("~/.ssh/id_rsa.pub")
        pprint(sshkey.key)
        print("Fingerprint:", sshkey.fingerprint)
        pprint(sshkey.__key__)
        print("sshkey", sshkey)
        print("str", str(sshkey))
        print(sshkey.type)
        assert True

    def test_005(self):
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

    def test_006(self):
        """
        cm key add testkey ~/.ssh/id_rsa.pub
        """
        HEADING()
        self.clean_db()
        result = self.run("cm key add {key} --source=~/.ssh/id_rsa.pub")
        result = self.run("cm key list")

        assert "{key}".format(**self.data) in result
        assert "file:" in result

    def test_007(self):
        """
        cm key add --git --name=testkey ~/.ssh/id_rsa.pub
        """
        HEADING()
        self.clean_db()

        result = self.run("cm key add --git ")
        result = self.run("cm key list")

        username = "{username}_git".format(**self.data)

        assert username in result

    def test_008(self):
        """
        key add --ssh --name=testkey
        """
        HEADING()
        self.clean_db()
        result = self.run("cm key add {key} --ssh")
        result = self.run("cm key list")
        assert "{key}".format(**self.data) in result
        assert "ssh" in result

    def test_009(self):
        """
        cm key list --source=db
        """

        HEADING()
        self.clean_db()
        result = self.run("cm key add {key} --ssh")
        result = self.run("cm key list --source=db")

        assert "{key}".format(**self.data) in result
        assert "ssh" in result

    def test_010(self):
        """
        cm key list --source=db --format=json
        """

        HEADING()
        result = self.run("cm key list --source=db --format=json")
        print(result)

        assert "{" in result
        assert "{key}".format(**self.data) in result

    def test_011(self):
        """
        cm key list --source=db --format=yaml
        """

        HEADING()
        result = self.run("cm key list --source=db --format=yaml")

        print("--------")
        print(result)
        print("--------")

        # d = yaml.load(str(result))


        # assert "testkey" in result
        assert ":" in str(result)

    def test_012(self):
        """
        cm key list --source=git
        """

        HEADING()
        result = self.run("cm key list --source=git")
        assert "_git_" in result

    def test_013(self):
        """
        cm key list --source=cloudmesh
        """

        HEADING()
        result = self.run("cm key list --source=yaml")
        print(result)
        assert ":" in result

    def test_014(self):
        """
        cm key list --source=ssh
        """

        HEADING()
        result = self.run("cm key list --source=ssh")
        assert "rsa" in result

    def test_015(self):
        """
        cm key get testkey
        """

        HEADING()
        result = self.run("cm key get {key}")
        assert "{key}".format(**self.data) in result

    def test_016(self):
        """
        cm key default testkey
        """

        HEADING()
        result = self.run("cm default key={key}")
        assert "ok." in result

        result = self.run("cm default key")
        assert "{key}".format(**self.data) in result

    def test_017(self):
        """
        cm key delete testkey
        """

        HEADING()
        self.clean_db()
        result = self.run("cm key add {key} --ssh")
        result = self.run("cm key delete {key}")
        assert "{key}".format(**self.data) in result
        assert "OK." in result

        result = self.run("cm key list")

        assert "None" in str(result)

    def test_018(self):
        """
        cm key delete --all
        """

        HEADING()
        result = self.run("cm key add {key} --ssh")
        result = self.run("cm key delete --all")
        assert "OK." in result

    def test_019(self):
        HEADING()
        self.clean_db()
        result = self.run("cm key add {key} --ssh")
        result = self.run("cm key upload {key}")

        cloudname = self.data.cloud
        d = ConfigDict("cloudmesh.yaml")
        cloud_details = d["cloudmesh"]["clouds"][cloudname]

        cloud = CloudProviderOpenstackAPI(cloudname, cloud_details)

        d = cloud.list_key(cloudname)
        pprint(d)

        assert len(d) > 0
        result = self.run("cm key delete {key} --cloud={cloud}")
        assert 'OK' in result

    def test_020(self):
        HEADING("set key to user defaults")

        result = self.run("cm key add {} --ssh".format(Default.user))
        result = self.run("cm default key={}".format(Default.user))



    # def test_021(self):
    #    HEADING()
    #    print(Key.get_from_yaml())

    # def test_022(self):
    #    """
    #    cm key list --source=cloudmesh
    #    """
    #    HEADING()
    #    result = self.run("cm key list --source=yaml")
    #    assert "ssh" in result
    #    assert "fingerprint" in result
