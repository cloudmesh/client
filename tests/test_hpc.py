""" run with

python setup.py install; nosetests -v --nocapture  tests/test_hpc.py:Test_hpc.test_001

nosetests -v --nocapture tests/test_hpc.py

or

nosetests -v tests/test_hpc.py

"""

from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import HEADING


def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result


class Test_hpc():
    """
        This class tests the HpcCommand
    """

    def test_001(self):
        """
        test hpc info
        :return:
        """
        HEADING()
        result = run("cm hpc info --cluster=india")
        assert "cluster" in result

    def test_002(self):
        """
        test hpc queue
        :return:
        """
        HEADING()
        result = run("cm hpc queue --cluster=india")
        assert "cluster" in result

    def test_003(self):
        """
        test hpc status
        :return:
        """
        HEADING()
        result = run("cm hpc status --cluster=india")
        assert "cluster" in result