""" run with

python setup.py install; nosetests -v --nocapture  tests/test_usage.py:Test_usage.test_001

nosetests -v --nocapture tests/test_usage.py

or

nosetests -v tests/test_usage.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING


def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result


class Test_usage():
    """
        This class tests the UsageCommand
    """

    def test_001(self):
        """
        test list
        :return:
        """
        HEADING()
        result = run("cm usage list --cloud=kilo")
        print(result)
        assert "start" in result