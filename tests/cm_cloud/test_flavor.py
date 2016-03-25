""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_flavor.py:Test_flavor.test_001

nosetests -v --nocapture tests/test_flavor.py

or

nosetests -v tests/test_flavor.py

"""

from cloudmesh_client.util import banner
from cloudmesh_client.util import HEADING

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.default import Default

class Test_flavor:
    """
        This class tests the FlavorCommand
    """

    data = dotdict({
        "cloud": Default.get_cloud(),
        "wrong_cloud": "no_cloud"
    })

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c ="-")
        print (command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return str(result)

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """
        test flavor refresh
        :return:
        """
        HEADING()
        result = self.run("cm flavor refresh --cloud={cloud}")
        assert "ok" in result

    def test_002(self):
        """
        test flavor refresh fail
        :return:
        """
        HEADING()
        result = self.run("cm flavor refresh --cloud={wrong_cloud}")
        assert "failed" in result

    def test_003(self):
        """
        test flavor list
        :return:
        """
        HEADING()
        result = self.run("cm flavor list --cloud={cloud}")
        assert "Name" in result

    def test_004(self):
        """
        test flavor list fail
        :return:
        """
        HEADING()
        result = self.run("cm flavor list --cloud={wrong_cloud}")
        assert "failed" in result

    def test_005(self):
        """
        test flavor list ID
        :return:
        """
        HEADING()
        result = self.run("cm flavor list 1 --cloud={cloud}")
        assert "Value" in result

    def test_006(self):
        """
        test flavor list ID fail
        :return:
        """
        HEADING()
        result = self.run("cm flavor list i --cloud={wrong_cloud}")
        assert "failed" in result

