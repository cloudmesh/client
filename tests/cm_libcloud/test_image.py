""" run with

python setup.py install; nosetests -v --nocapture  tests/test_image.py:Test_image.test_001

nosetests -v --nocapture tests/test_image.py

or

nosetests -v tests/test_image.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING
import json



class Test_image():
    """
        This class tests the ImageCommand
    """

    data = {
        'cloud': 'TBD'
    }


    def run(command):
        command = command.format(**data)
        print(command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return result

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
        test image list
        :return:
        """
        HEADING()
        result = self.run("cm image list --cloud={cloud}")
        assert "description" in result

    def test_005(self):
        """
        test image list ID
        :return:
        """
        HEADING()
        result = self.run("cm image list --cloud={cloud} --format=json")
        assert "Ubuntu" in result

    def test_006(self):
        """
        test image list ID fail
        :return:
        """
        HEADING()
        result = self.run("cm image list 1 --cloud={cloud}")
        assert "ok" in result

