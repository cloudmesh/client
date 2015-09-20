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
        """testing cm secgroup create india fg479 test-group"""
        HEADING()
        banner("cm secgroup create india fg479 test-group")

        result = run("cm secgroup create india fg479 test-group")
        assert "Created a new security group [test-group]" in result
        return

    def test_002(self):
        """testing cm secgroup list india fg479"""
        HEADING()
        banner("cm secgroup list india fg479")

        result = run("cm secgroup list india fg479")
        assert "test-group" in result

        return
