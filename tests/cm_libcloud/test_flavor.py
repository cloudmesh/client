""" run with

python setup.py install; nosetests -v --nocapture  tests/test_flavor.py:Test_flavor.test_001

nosetests -v --nocapture tests/test_flavor.py

or

nosetests -v tests/test_flavor.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING




class Test_flavor():
    """
        This class tests the FlavorCommand
    """

    data = {
        'cloud': 'chameleon-ec2'
    }

    def run(command):
        command = command.format(self.data)
        print(command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print (result)
        return result

    def test_001(self):
        """
        test flavor refresh
        :return:
        """
        HEADING()
        result = self.run("cm flavor refresh")
        assert "ok" in result

    def test_002(self):
        """
        test flavor refresh fail
        :return:
        """
        HEADING()
        result = self.run("cm flavor refresh --cloud={cloud}")
        assert "failed" in result

    def test_003(self):
        """
        test flavor list fail
        :return:
        """
        HEADING()
        result = self.run("cm flavor list --cloud={cloud}")
        assert "failed" in result

    def test_004(self):
        """
        test flavor list ID
        :return:
        """
        HEADING()
        result = self.run("cm flavor list 1 --cloud={cloud}")
        assert "Value" in result

