""" run with

python setup.py install; nosetests -v --nocapture  tests/test_vm.py:Test_vm.test_001

nosetests -v --nocapture

or

nosetests -v

"""
from __future__ import print_function

from cloudmesh_client.util import HEADING
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import banner



class Test_vm:

    def run(self, command):
        command = command.format(**self.data)
        banner(command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        return result

    def setup(self):

        self.data = {
            "cloud": "kilo",
            "group": "test",
            "image": "Ubuntu-14.04-64",
            "vm": "testvm",
            "flavor": "m1.small"
        }

    def tearDown(self):
        pass

    def load_key(self):
        try:
            command = "cm key load"
            result = self.run(command)
            print(result)

            command = "cm key upload"
            result = self.run(command)
            print(result)
        except Exception, e:
            print(e.message)

    def test_001(self):
        """
        cm vm boot --name=testvm --cloud=kilo --image=<image_id> --flavor=2
        --group=test
        """
        self.load_key()
        HEADING()
        command = "cm vm boot --name={vm} --cloud={cloud} --image={image}" + \
                  " --flavor={flavor} --group={group}"
        result = self.run(command)
        print(result)
        assert "OK." in result

    def test_002(self):
        """
        cm vm refresh --cloud=kilo
        """
        HEADING()
        result = self.run("cm vm refresh --cloud={cloud}")
        print (result)
        assert "OK." in result

    def test_003(self):
        """
        cm vm list --cloud=kilo
        """
        HEADING()
        result = self.run("cm vm list --cloud={cloud}")
        print(result)
        assert "OK." in result

    def test_004(self):
        """
        cm vm list testvm --cloud=kilo
        """
        HEADING()
        result = self.run("cm vm list {vm} --cloud={cloud}")
        print(result)
        assert "OK." in result

    def test_005(self):
        """
        cm vm status --cloud=kilo
        """
        HEADING()
        result = self.run("cm vm status --cloud={cloud}")
        print(result)
        assert "OK." in result

    def test_006(self):
        """
        cm vm ip_show testvm --cloud=kilo
        """
        HEADING()
        result = self.run("cm vm ip show {vm} --cloud={cloud}")
        print(result)
        assert "OK." in result

    def test_007(self):
        """
        cm vm delete testvm --cloud=kilo
        """
        HEADING()
        result = self.run("cm vm delete {vm} --cloud={cloud}")
        print(result)
        assert "OK." in result
