""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_group.py:Test_group.test_001

nosetests -v --nocapture tests/test_group.py

or

nosetests -v tests/test_group.py

"""
from __future__ import print_function
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING
from cloudmesh_client.util import banner

from cloudmesh_client.cloud.group import Group
from pprint import pprint


class Test_group:

    data = {
        "cloud": "kilo",
        "user": "test",
        "group": "groupA"
    }


    def run(self, command):
        command = command.format(**self.data)
        banner(command)
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

    def test_001(self):
        """testing cm group add """
        HEADING()

        c = "cm group add {user}-001 --group={group} --category={cloud}  --type=vm"
        self.run(c)


        id = str(Group.get(name="groupA", category="kilo"))
        print (id)
        assert "test-001" in id
        return

    def test_002(self):
        """testing cm group add groupA --category=kilo --id=test-002 --type=vm"""
        HEADING()

        command = "cm group add {user}-002 --group={group} --category={cloud}  --type=vm"
        self.run(command)

        group = Group.get(name="groupA", category="kilo")

        names = ["{user}-001".format(**self.data),
                "{user}-002".format(**self.data)]
        for id in group:
            element = group[id]
            assert element["category"] == "kilo"
            assert element["name"] == "groupA"
            assert element["type"] == "vm"
            assert element["member"] in names
        return

    def test_003(self):
        """testing cm group copy groupA groupB"""
        HEADING()

        command = "cm group copy {group} groupB"

        result = self.run(command)
        assert "groupB" in result

        return

    def test_004(self):
        """testing cm group merge groupA groupB groupC"""
        HEADING()
        command = "cm group merge {group} groupB groupC"

        result = self.run(command)
        assert "ok." in result
        return

    def test_005(self):
        """testing cm group list --category=kilo groupA"""
        HEADING()
        command = "cm group list --category=kilo {group}"

        result = self.run(command)
        assert "groupA" in result
        return

    def test_006(self):
        """testing cm group list --category=kilo --format json groupA"""
        HEADING()
        command= "cm group list --category={cloud} --format=json {group}"

        result = self.run(command)
        assert "groupA" in result
        return

    def test_007(self):
        """testing cm group list --category=kilo --format table"""
        HEADING()
        command = "cm group list --category={cloud} --format=table"

        result = self.run(command)
        assert "groupA" in result
        return

    def test_008(self):
        """testing cm group add --name=groupX --id albert-00x [WITH DEFAULT CLOUD=kilo, TYPE=VM]"""
        HEADING()
        banner("cm group add --name=groupX --id=albert-00x")

        result = self.run("cm default category=kilo")
        assert "kilo" in result
        assert "category" in result
        assert "ok" in result

        result = self.run("cm default type=vm")
        assert "ok." in result

        result = self.run("cm group add groupX --id=albert-00x")
        assert "albert-00x" in result

        result = self.run("cm group list --category={cloud} groupX")
        assert "kilo" in result
        assert "vm" in result

        return

    def test_009(self):
        """testing cm group remove --category=kilo --name=groupA --id=test-002"""
        HEADING()
        banner("cm group remove --category={cloud} --name=groupA --id=test-002")

        result = self.run("cm group remove --category={cloud} --name={group} --id={user}-002")
        print(result)
        assert "Successfully removed ID" in result

        result = self.run("cm group list {group}")
        assert "test-002" not in result

        return

    def test_010(self):
        """testing cm group delete groupA --category=kilo"""
        HEADING()
        """
        command = "cm group delete {group} --category=kilo"
        result = self.run(command)
        print(result)
        assert "ok." in result
        """

        banner("cm group delete groupB --category=kilo")
        result = self.run("cm group delete groupB --category=kilo")
        assert "ok." in result

        banner("cm group delete groupC --category=kilo")
        result = self.run("cm group delete groupC --category=kilo")
        assert "ok." in result

        banner("cm group delete groupX")
        result = self.run("cm group delete groupX")
        assert "ok." in result


    def test_999(self):
        """Cleanup defaults"""
        self.run("cm default delete category")
        self.run("cm default delete type")

        return

