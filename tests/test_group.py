""" run with

python setup.py install; nosetests -v --nocapture  tests/test_group.py:Test_group.test_001

nosetests -v --nocapture tests/test_group.py

or

nosetests -v tests/test_group.py

"""
import os

from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import HEADING
from cloudmesh_base.util import banner

def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result

class Test_group:

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """testing cm group info"""
        HEADING()
        banner("group info")

        result = run("cm group info")
        assert "[Command To be Implemented] group, format: table" in result
        return

    def test_002(self):
        """testing cm group info --format json"""
        HEADING()
        banner("group info --format json")

        result = run("cm group info --format json")
        assert "group, format: json" in result
        return

    def test_003(self):
        """testing cm group list --cloud india --format table groupA"""
        HEADING()
        banner("cm group list --cloud india --format table groupA")

        result = run("cm group list --cloud india --format table groupA")
        assert "set group, name: groupA, format: table, cloud: india" in result
        return

    def test_004(self):
        """testing cm group add --id goshenoy-001 --type vm --name groupA"""
        HEADING()
        banner("cm group add --id goshenoy-001 --type vm --name groupA")

        result = run("cm group add --id goshenoy-001 --type vm --name groupA")
        assert "add to group, name: groupA, type: vm, id: goshenoy-001" in result
        return

    def test_005(self):
        """testing cm group delete --cloud india --name groupA"""
        HEADING()
        banner("cm group delete --cloud india --name groupA")

        result = run("cm group delete --cloud india --name groupA")
        assert "deleted group, name: groupA, cloud: india" in result
        return

    def test_006(self):
        """testing cm group copy groupA groupB"""
        HEADING()
        banner("cm group copy groupA groupB")

        result = run("cm group copy groupA groupB")
        assert "copy FROM group: groupA, TO group: groupB" in result
        return

    def test_007(self):
        """testing cm group merge groupA groupB groupC"""
        HEADING()
        banner("cm group merge groupA groupB groupC")

        result = run("cm group merge groupA groupB groupC")
        assert "merge, group: groupA, & group: groupB, to group: groupC" in result
        return