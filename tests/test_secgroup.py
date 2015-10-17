""" run with

python setup.py install; nosetests -v --nocapture  tests/test_secgroup.py:Test_secgroup.test_001

nosetests -v --nocapture tests/test_secgroup.py

or

nosetests -v tests/test_secgroup.py

"""
import os

from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import HEADING
from cloudmesh_base.util import banner
from cloudmesh_client.cloud.secgroup import SecGroup

def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result

class Test_secgroup:

    def setup(self):

        pass

    def tearDown(self):
        pass

    def test_001(self):
        """testing cm secgroup create --cloud india --tenant fg479 test-group"""
        HEADING()
        banner("cm secgroup create --cloud india "
               "--tenant fg479 test-group")

        result = run("cm secgroup create --cloud india "
                     "--tenant fg479 test-group")
        assert "Created a new security group [test-group]" in result
        return

    def test_002(self):
        """testing cm secgroup list --cloud india --tenant fg479"""
        HEADING()
        banner("cm secgroup list --cloud india --tenant fg479")

        result = run("cm secgroup list --cloud india --tenant fg479")
        assert "default" in result

        return

    def test_003(self):
        """testing cm secgroup rules-add --cloud india --tenant fg479 test-group 80 80 tcp  0.0.0.0/0"""
        HEADING()
        banner("cm secgroup rules-add --cloud india "
               "--tenant fg479 test-group 80 80 tcp  0.0.0.0/0")

        result = run("cm secgroup rules-add --cloud india "
                     "--tenant fg479 test-group 80 80 tcp  0.0.0.0/0")
        assert "Added rule" in result

    def test_004(self):
        """testing cm secgroup rules-add --cloud india --tenant fg479 test-group 443 443 udp  0.0.0.0/0"""
        HEADING()
        banner("cm secgroup rules-add india --cloud india "
               "--tenant test-group 443 443 udp  0.0.0.0/0")

        result = run("cm secgroup rules-add --cloud india "
                     "--tenant fg479 test-group 443 443 udp  0.0.0.0/0")
        assert "Added rule" in result

        return

    def test_005(self):
        """cm secgroup rules-list --cloud india --tenant fg479 test-group"""
        HEADING()
        banner("cm secgroup rules-list --cloud india "
               "--tenant fg479 test-group")

        result = run("cm secgroup rules-list --cloud india "
                     "--tenant fg479 test-group")
        assert "test-group | 80" in result

        return

    def test_006(self):
        """cm secgroup rules-delete --cloud india --tenant fg479 test-group 80 80 tcp  0.0.0.0/0"""
        HEADING()
        banner("cm secgroup rules-delete --cloud india "
               "--tenant fg479 test-group 80 80 tcp  0.0.0.0/0")

        result = run("cm secgroup rules-delete --cloud india "
                     "--tenant fg479 test-group 80 80 tcp  0.0.0.0/0")
        assert "Rule [80 | 80 | tcp | 0.0.0.0/0] deleted" in result

        return

    def test_007(self):
        """cm secgroup delete --cloud india --tenant fg479 test-group"""
        HEADING()
        banner("cm secgroup delete --cloud india "
               "--tenant fg479 test-group")

        result = run("cm secgroup delete --cloud india "
                     "--tenant fg479 test-group")
        assert "Security Group [test-group] for cloud [india], & tenant [fg479] deleted" in result

        return