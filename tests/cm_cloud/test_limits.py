""" run with

python setup.py install; nosetests -v --nocapture  tests/test_limits.py:Test_limits.test_001

nosetests -v --nocapture tests/test_limits.py

or

nosetests -v tests/test_limits.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING


def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result


class Test_limits():
    """
        This class tests the LimitsCommand
    """

    def test_001(self):
        """
        test limits list
        :return:
        """
        HEADING()
        result = run("cm limits list")
        assert "Name" in result

    def test_002(self):
        """
        test limits list with csv output
        :return:
        """
        HEADING()
        result = run("cm limits list --format=csv").split('\n')
        assert "maxTotalFloatingIps" in result[0]

    def test_003(self):
        """
        test limits class where cloud doesnt exist
        :return:
        """
        HEADING()
        result = run("cm limits list --cloud=india1")


        assert "Error" in result

    def test_004(self):
        """
        test limits class with unauthorised access
        :return:
        """
        HEADING()
        result = run("cm limits list --tenant=fg232")
        assert "Not authorized" in result
