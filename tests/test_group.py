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

from cloudmesh_client.cloud.group import Group
from cloudmesh_client.cloud.default import Default

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
        """testing cm group add --cloud india --id test-001 --type vm --name groupA"""
        HEADING()
        banner("cm group add --cloud india --id test-001 --type vm --name groupA")

        run("cm group add --cloud india --id test-001 --type vm --name groupA")
        id = str(Group.get_group(name="groupA", cloud="india").value)
        assert "test-001" in id
        return

    def test_002(self):
        """testing cm group copy groupA groupB"""
        HEADING()
        banner("cm group copy groupA groupB")

        result = run("cm group copy groupA groupB")
        print(result)
        assert "Created a new group [groupB] and added ID [test-001] to it" in result

        return

    def test_003(self):
        """testing cm group merge groupA groupB groupC"""
        HEADING()
        banner("cm group merge groupA groupB groupC")

        result = run("cm group merge groupA groupB groupC")
        assert "Merge of group [groupA] & [groupB] to group [groupC] successful!" in result
        return

    def test_004(self):
        """testing cm group info groupA"""
        HEADING()
        banner("group info groupA")

        result = run("cm group info groupA")
        assert "groupA" in result
        return

    def test_005(self):
        """testing cm group info --format json groupA"""
        HEADING()
        banner("group info --format json groupA")

        result = run("cm group info --format json groupA")
        assert "groupA" in result
        return

    def test_006(self):
        """testing cm group list --cloud india --format table"""
        HEADING()
        banner("cm group list --cloud india --format table")

        result = run("cm group list --cloud india --format tables")
        assert "groupC" in result
        return

    def test_007(self):
        """testing cm group add --name groupX --id gourav-00x [WITH DEFAULT CLOUD=INDIA, TYPE=VM]"""
        HEADING()
        banner("cm group add --name groupX --id gourav-00x")

        result1 = run("cm default cloud=india")
        assert "Successfully added cloud" in result1

        result1 = run("cm default type=vm")
        assert "Successfully added type" in result1

        result2 = run("cm group add --name groupX --id gourav-00x")
        assert "gourav-00x" in result2

        result3 = run("cm group info groupX")
        assert "india" in result3
        assert "vm" in result3

    def test_008(self):
        """testing cm group delete --cloud india --name groupA"""
        HEADING()
        banner("cm group delete --cloud india --name groupA")
        result = run("cm group delete --cloud india --name groupA")
        assert "Deletion Successful!" in result

        banner("cm group delete --cloud india --name groupB")
        result = run("cm group delete --cloud india --name groupB")
        assert "Deletion Successful!" in result

        banner("cm group delete --cloud india --name groupC")
        result = run("cm group delete --cloud india --name groupC")
        assert "Deletion Successful!" in result

        banner("cm group delete --name groupX")
        result = run("cm group delete --name groupX")
        assert "Deletion Successful!" in result

        # Cleanup defaults
        run("cm default delete cloud")
        run("cm default delete type")

        return

