""" run with

python setup.py install; nosetests -v --nocapture  tests/test_flavor.py:Test_flavor.test_001

nosetests -v --nocapture tests/test_flavor.py

or

nosetests -v tests/test_flavor.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING


def run(command):
    print(command)
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    print (result)
    return result


class Test_flavor():
    """
        This class tests the FlavorCommand
    """

    def test_001(self):
        """
        test flavor refresh
        :return:
        """
        HEADING()
        result = run("cm flavor refresh")
        assert "ok" in result

    def test_002(self):
        """
        test flavor refresh fail
        :return:
        """
        HEADING()
        result = run("cm flavor refresh --cloud=kilo11")
        assert "failed" in result

    def test_003(self):
        """
        test flavor list
        :return:
        """
        HEADING()
        result = run("cm flavor list")
        assert "Name" in result

    def test_004(self):
        """
        test flavor list fail
        :return:
        """
        HEADING()
        result = run("cm flavor list --cloud=kilo11")
        assert "failed" in result

    def test_005(self):
        """
        test flavor list ID
        :return:
        """
        HEADING()
        result = run("cm flavor list 1 --cloud=kilo")
        assert "Value" in result

    def test_006(self):
        """
        test flavor list ID fail
        :return:
        """
        HEADING()
        result = run("cm flavor list i --cloud=kilo11")
        assert "failed" in result

