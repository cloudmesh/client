""" run with

python setup.py install; nosetests -v --nocapture  tests/test_image.py:Test_image.test_001

nosetests -v --nocapture tests/test_image.py

or

nosetests -v tests/test_image.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING
import json

def run(command):
    print(command)
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    print(result)
    return result


class Test_image():
    """
        This class tests the ImageCommand
    """

    def test_001(self):
        """
        test image refresh
        :return:
        """
        HEADING()
        result = run("cm image refresh --cloud=kilo")
        assert "ok." in result

    def test_002(self):
        """
        test image refresh fail
        :return:
        """
        HEADING()
        result = run("cm image refresh --cloud=kilo11")
        assert "failed" in result

    def test_003(self):
        """
        test image list
        :return:
        """
        HEADING()
        result = run("cm image list --cloud=kilo")
        assert "description" in result

    def test_004(self):
        """
        test image list fail
        :return:
        """
        HEADING()
        result = run("cm image list --cloud=kilo11")
        assert "failed" in result

    def test_005(self):
        """
        test image list ID
        :return:
        """
        HEADING()
        result = run("cm image list --cloud=kilo --format=json")
        assert "Ubuntu" in result

    def test_006(self):
        """
        test image list ID fail
        :return:
        """
        HEADING()
        result = run("cm image list i --cloud=kilo11")
        assert "failed" in result

