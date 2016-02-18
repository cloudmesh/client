""" run with

python setup.py install; nosetests -v --nocapture  tests/test_quota.py:Test_quota.test_001

nosetests -v --nocapture tests/test_quota.py

or

nosetests -v tests/test_quota.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING


def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result


class Test_quota():
    """
        This class tests the QuotaCommand
    """

    def test_001(self):
        """
        test quota list
        :return:
        """
        HEADING()
        result = run("cm quota list")
        assert "Quota" in result

    def test_002(self):
        """
        test quota list with csv output
        :return:
        """
        HEADING()
        result = run("cm quota list --cloud=kilo --format=csv")
        assert "ram" in result

    def test_003(self):
        """
        test quota class where cloud doesnt exist
        :return:
        """
        HEADING()
        result = run("cm quota list --cloud=doesnotexist")
        assert "is not defined in the yaml file" in result