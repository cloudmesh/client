""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_image.py:Test_image.test_001

nosetests -v --nocapture tests/test_image.py

or

nosetests -v tests/test_image.py

"""

from cloudmesh_client.util import banner
from cloudmesh_client.util import HEADING

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict

class Test_image:
    """
        This class tests the ImageCommand
    """

    data = dotdict({
        "cloud": "kilo",
        "wrong_cloud": "kilo_wrong",
        "format": "json"
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
        return result

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """
        test image refresh
        :return:
        """
        HEADING()
        result = self.run("cm image refresh --cloud={cloud}")
        assert "ok." in result

    def test_002(self):
        """
        test image refresh fail
        :return:
        """
        HEADING()
        result = self.run("cm image refresh --cloud={wrong_cloud}")
        assert "failed" in result

    def test_003(self):
        """
        test image list
        :return:
        """
        HEADING()
        result = self.run("cm image list --cloud={cloud}")
        assert "description" in result

    def test_004(self):
        """
        test image list fail
        :return:
        """
        HEADING()
        result = self.run("cm image list --cloud={wrong_cloud}")
        assert "failed" in result

    def test_005(self):
        """
        test image list ID
        :return:
        """
        HEADING()
        result = self.run("cm image list --cloud={cloud} --format={format}")
        assert "Ubuntu" in result

    def test_006(self):
        """
        test image list ID fail
        :return:
        """
        HEADING()
        result = self.run("cm image list i --cloud={wrong_cloud}")
        assert "failed" in result

