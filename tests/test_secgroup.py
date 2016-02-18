""" run with

python setup.py install; nosetests -v --nocapture  tests/test_secgroup.py:Test_secgroup.test_001

nosetests -v --nocapture tests/test_secgroup.py

or

nosetests -v tests/test_secgroup.py

"""
import os

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING
from cloudmesh_client.util import banner
from cloudmesh_client.cloud.secgroup import SecGroup
from cloudmesh_client.common.ConfigDict import ConfigDict

def run(command):
    banner(command, c='-')
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    print(result)
    return result

class Test_secgroup:

    def setup(self):

        config = ConfigDict("cloudmesh.yaml")

        self.data = {
            "cloud": "kilo",
        }

        self.data["tenant"] = config["cloudmesh.clouds"][self.data["cloud"]][
            "credentials"]["OS_TENANT_NAME"]
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """testing cm secgroup create --cloud=india --tenant=fg... test-group"""
        HEADING()
        command = "cm secgroup create --cloud={cloud} --tenant={tenant} " \
                  "test-group"
        result = run(command.format(**self.data))
        assert "ok" in result
        assert "test-group" in result
        return

    def test_002(self):
        """testing cm secgroup list --cloud=india --tenant=fg..."""
        HEADING()
        command = "cm secgroup list --cloud={cloud} --tenant={tenant}"
        result = run(command.format(**self.data))
        assert "ok" in result

        return

    def test_003(self):
        """testing cm secgroup rules-add --cloud=india --tenant=fg... test-group 80 80 tcp  0.0.0.0/0"""
        HEADING()
        command = "cm secgroup rules-add --cloud={cloud} --tenant={tenant} " \
                  "test-group 80 80 tcp  0.0.0.0/0"

        result = run(command.format(**self.data))
        assert "Added rule" in result

    def test_004(self):
        """testing cm secgroup rules-add --cloud=india --tenant=fg... test-group 443 443 udp  0.0.0.0/0"""
        HEADING()

        command = "cm secgroup rules-add --cloud={cloud} --tenant={tenant} " \
                  "test-group 443 443 tcp  0.0.0.0/0"

        result = run(command.format(**self.data))
        assert "Added rule" in result

        return

    def test_005(self):
        """cm secgroup rules-list --cloud=india --tenant=fg... test-group"""
        HEADING()
        command = "cm secgroup rules-list --cloud={cloud} --tenant={tenant} " \
                  "test-group"
        result = run(command.format(**self.data))
        assert "test-group | 80" in result

        return

    def test_006(self):
        """cm secgroup rules-delete --cloud=india --tenant=fg... test-group 80 80 tcp  0.0.0.0/0"""
        HEADING()
        command = "cm secgroup rules-delete --cloud={cloud} --tenant={" \
                  "tenant} test-group 80 80 tcp  0.0.0.0/0"

        result = run(command.format(**self.data))
        assert "Rule [80 | 80 | tcp | 0.0.0.0/0] deleted" in result

        return

    def test_007(self):
        """cm secgroup delete --cloud=india --tenant=fg... test-group"""
        HEADING()
        command = "cm secgroup delete --cloud={cloud} --tenant={tenant} " \
                  "test-group"
        result = run(command.format(**self.data))
        assert "Security Group [test-group] for cloud [{cloud}], " \
               "& tenant [{tenant}] deleted".format(**self.data) in result

        return