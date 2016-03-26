""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_secgroup.py:Test_secgroup.test_001

nosetests -v --nocapture tests/test_secgroup.py

or

nosetests -v tests/test_secgroup.py

"""

from cloudmesh_client.util import banner
from cloudmesh_client.util import HEADING

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.default import Default


# noinspection PyPep8Naming
class Test_secgroup:
    data = dotdict({
        "cloud": Default.get_cloud(),
        "group": "test_group",
        "wrong_cloud": "no_cloud",
        "rule-80": "80 80 tcp  0.0.0.0/0",
        "rule-443": "443 443 tcp  0.0.0.0/0",
    })
    data.tenant = ConfigDict("cloudmesh.yaml")["cloudmesh.clouds"][data.cloud]["credentials"]["OS_TENANT_NAME"]

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c="-")
        print(command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return str(result)

    def setup(self):
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_001(self):
        HEADING("testing cm secgroup create --cloud=india test-group")
        result = self.run("cm secgroup create --cloud={cloud} {group}")
        assert "Created a new security group" in result
        assert self.data.group in result
        return

    def test_002(self):
        HEADING("testing cm secgroup refresh")
        result = self.run("cm secgroup refresh")
        assert "ok" in result
        return

    def test_003(self):
        HEADING("testing cm secgroup list --cloud=india")
        result = self.run("cm secgroup list --cloud={cloud}")
        assert self.data.group in result
        return

    def test_004(self):
        HEADING("testing cm secgroup rules-add --cloud=india test-group 80 80 tcp  0.0.0.0/0")
        result = self.run("cm secgroup rules-add --cloud={cloud} {group} {rule-80}")
        assert "Added rule" in result
        return

    def test_005(self):
        HEADING("testing cm secgroup rules-add --cloud=india test-group 443 443 udp  0.0.0.0/0")
        result = self.run("cm secgroup rules-add --cloud={cloud} {group} {rule-443}")
        assert "Added rule" in result
        return

    def test_006(self):
        HEADING("cm secgroup rules-list --cloud=india test-group")
        result = self.run("cm secgroup rules-list --cloud={cloud} {group}")
        assert "0.0.0.0/0" in result
        return

    def test_007(self):
        HEADING("cm secgroup rules-delete --cloud=india test-group 80 80 tcp  0.0.0.0/0")
        result = self.run("cm secgroup rules-delete --cloud={cloud} {group} {rule-80}")
        assert "Rule [80 | 80 | tcp | 0.0.0.0/0] deleted" in result
        return

    def test_008(self):
        HEADING("cm secgroup rules-delete --cloud=india test-group --all")
        result = self.run("cm secgroup rules-delete --cloud={cloud} {group} --all")
        assert "Rule [443 | 443 | tcp | 0.0.0.0/0] deleted" in result
        return

    def test_009(self):
        HEADING("cm secgroup delete --cloud=india test-group")
        result = self.run("cm secgroup delete --cloud={cloud} {group}")
        assert "deleted" in result
        return
