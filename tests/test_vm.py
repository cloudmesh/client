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
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """
        cm vm start --name=testvm --cloud=india --image=<image_id> --flavor=2
        """
        image_id = "619b8942-2355-4aa2-bae3-74b8f1751911"

        HEADING()
        result = run("cm vm start --name=testvm --cloud=juno --image={:} --flavor=2".format(image_id))
        print result
        assert "OK." in result

    def test_002(self):
        """
        cm vm list --cloud=india
        """
        HEADING()
        result = run("cm vm list --cloud=juno")
        print result
        assert "OK." in result

    def test_003(self):
        """
        cm vm ip_show testvm --cloud=india
        """
        HEADING()
        result = run("cm vm ip_show testvm --cloud=juno")
        print result
        assert "OK." in result

    def test_004(self):
        """
        cm vm delete testvm --cloud=india
        """
        HEADING()
        result = run("cm vm delete testvm --cloud=juno")
        print result
        assert "OK." in result
