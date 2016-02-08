""" run with

python setup.py install; nosetests -v --nocapture  tests/test_vm.py:Test_vm.test_001

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_base.util import HEADING
#
from cloudmesh_base.Shell import Shell


def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result


class Test_vm:
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

    def test_001(self):
        """
        cm vm boot --name=testvm --cloud=kilo --image=<image_id> --flavor=2
        --group=test
        """

        HEADING()
        command = "cm vm boot --name={vm} --cloud={cloud} --image={image}" + \
                  "--flavor={flavor} --group={group}"
        result = run(command.format(**self.data))
        print result
        assert "OK." in result

    def test_002(self):
        """
        cm vm refresh --cloud=kilo
        """
        HEADING()
        result = run("cm vm refresh --cloud={cloud}".format(**self.data))
        print result
        assert "OK." in result

    def test_003(self):
        """
        cm vm list --cloud=kilo
        """
        HEADING()
        result = run("cm vm list --cloud={cloud}".format(**self.data))
        print result
        assert "OK." in result

    def test_004(self):
        """
        cm vm list testvm --cloud=kilo
        """
        HEADING()
        result = run("cm vm list {vm} --cloud={cloud}".format(**self.data))
        print result
        assert "OK." in result

    def test_005(self):
        """
        cm vm status --cloud=kilo
        """
        HEADING()
        result = run("cm vm status --cloud={cloud}".format(**self.data))
        print result
        assert "OK." in result

    def test_006(self):
        """
        cm vm ip_show testvm --cloud=kilo
        """
        HEADING()
        result = run("cm vm ip show {vm} --cloud={cloud}".format(**self.data))
        print result
        assert "OK." in result

    def test_007(self):
        """
        cm vm delete testvm --cloud=kilo
        """
        HEADING()
        result = run("cm vm delete {vm} --cloud={cloud}".format(**self.data))
        print result
        assert "OK." in result
