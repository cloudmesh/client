""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_group.py:Test_group.test_001

nosetests -v --nocapture tests/test_group.py

or

nosetests -v tests/test_group.py

"""
from __future__ import print_function

from pprint import pprint

from cloudmesh_client.cloud.group import Group
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default


# noinspection PyPep8Naming
class Test_group:
    data = dotdict({
        "cloud": Default.cloud,
        "user": "test",
        "prefix": "test",
        "group": "groupA"
    })

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c='-')
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


    def test_000(self):
        HEADING("testing cm group list")

        c = "cm group list"
        self.run(c)

    def test_001(self):
        HEADING("testing cm group add ")

        c = "cm group add {prefix}-001 --group={group}  --type=vm"
        self.run(c)

        index = str(Group.get(name="{group}".format(**self.data), scope='all'))
        print("INDEX", index)
        assert "test-001" in index

    def test_002(self):
        HEADING("testing cm group add")

        command = "cm group add {prefix}-002 --group={group}   --type=vm"
        self.run(command)

        group = Group.get(name="groupA", scope='all')

        print("GGGG", group)

        names = ["{prefix}-001".format(**self.data),
                 "{prefix}-002".format(**self.data)]
        for element in group:
            pprint(element)
            assert element["name"] == "groupA"
            assert element["species"] == "vm"
            assert element["member"] in names


    def test_003(self):
        HEADING("testing cm group copy groupA groupB")

        command = "cm group copy {group} groupB"

        result = self.run(command)
        assert "groupB" in result


    def test_004(self):
        HEADING("testing cm group merge groupA groupB groupC")
        command = "cm group merge {group} groupB groupC"

        result = self.run(command)
        assert "ok." in result

    def test_005(self):
        HEADING("testing cm group list  groupA")
        command = "cm group list  {group}"

        result = self.run(command)
        assert "groupA" in str(result)

    def test_006(self):
        HEADING("testing cm group list  --format=json groupA")
        command = "cm group list  --format=json {group}"

        result = self.run(command)
        assert "groupA" in result
        return

    def test_007(self):
        HEADING("testing cm group list  --format=table")
        command = "cm group list  --format=table"

        result = self.run(command)
        assert "groupA" in result

    def test_008(self):
        HEADING("testing cm group add with default cloud")
        banner("cm group add --name=groupX --id=albert-00x", c='-')

        result = self.run("cm default cloud")
        print("UUUU", result)
        pprint(self.data.cloud)
        print(type(result), type(self.data.cloud))
        assert self.data.cloud in result

        result = self.run("cm default type=vm")
        assert "ok." in result

        result = self.run("cm group add albert-00x --group=groupX ")
        # print ("RRR", result)
        # assert "albert-00x" in result

        result = self.run("cm group list groupX")

        print("DDDDD", result)

        assert "groupX" in result

    def test_009(self):
        HEADING("testing cm group remove ")
        banner("cm group remove {prefix}-002  --group={group}")

        result = self.run("cm group remove {prefix}-002  --group={group} ")
        print(result)
        assert "ok" in result

        result = self.run("cm group list {group}")
        assert "test-002" not in result

    def test_010(self):
        HEADING("testing cm group delete ")

        command = "cm group delete {group} "
        result = self.run(command)
        print(result)

        for group in ["groupA", "groupB", "groupC", "groupX"]:
            self.data.group = group
        command = "cm group delete {group} "

        result = self.run(command)

        assert "ok." in result

    def test_011(self):

        HEADING("list vms in group")

        setup = [
            "cm group add vm_1 --group=group_x",
            "cm group add vm_2 --group=group_x",
            "cm group add vm_3 --group=group_y",
            "cm group add vm_3 --group=group_x",
            "cm group list"]

        for command in setup:
            self.run(command)

        print("T1")
        result = Group.get_vms("group_x")
        print("group x", result)
        assert 'vm_1' in result
        assert 'vm_2' in result
        assert 'vm_3' in result

        print("T2")
        result = Group.get_vms("group_y")
        print("group y", result)
        assert 'vm_3' in result
        assert 'vm_1' not in result
        assert 'vm_2' not in result

        print("T3")
        result = Group.names()
        print("names", result)
        assert 'group_x' in result
        assert 'group_y' in result

        print("T4")
        result = Group.vm_groups("vm_1")
        print("vm_1", result)
        assert 'group_x' in result
        assert 'group_y' not in result

        print("T5")
        result = Group.vm_groups("vm_3")
        print("vm_3", result)
        assert 'group_x' in result
        assert 'group_y' in result

        print("T6")
        result = Group.delete(name="group_x")
        print(result)
        result = self.run("cm group list")
        print(result)

        assert 'vm_1' not in result
        assert 'vm_2' not in result

        print("T7")
        self.run("cm group list")

        for command in setup:
            self.run(command)
        result = self.run("cm group list")
        print(result)

        result = Group.delete(name="group_y")

        print(result)
        result = self.run("cm group list")

        assert 'group_y' not in result
        assert 'vm_3' in result

    def test_012(self):
        HEADING("list non existing group")
        command = "cm group list DOESNOTEXIST"
        result = self.run(command)

        assert "ERROR" in result
