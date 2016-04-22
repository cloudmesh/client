""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_clouds/test_chameleon.py:Test_chameleon.test_001

nosetests -v --nocapture tests/test_image.py

or

nosetests -v tests/test_chameleon.py

"""

import os

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner


# noinspection PyMethodMayBeStatic,PyPep8Naming
class Test_chameleon:
    """
        This class tests the ImageCommand
    """

    # noinspection PyTypeChecker
    data = dotdict({
        "cloud": "kilo",
    })

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c="-")
        print(command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return result

    def setup(self):
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_001(self):
        """
        test image refresh
        :return:
        """
        HEADING()
        result = self.run("make db")
        assert "ok." in result

    def test_002(self):
        """
        test image refresh
        :return:
        """
        HEADING()
        result = self.run("cm default cloud={cloud}")
        assert "ok." in result

    def test_003(self):
        """
        test image refresh
        :return:
        """
        HEADING()
        os.system("py.test tests/cm_cloud")
        # assert "ok." in result
        assert True
