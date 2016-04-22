""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_flavor.py:Test_flavor.test_001

nosetests -v --nocapture tests/test_flavor.py

or

nosetests -v tests/test_flavor.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default


# noinspection PyPep8Naming
class Test_flavor:
    """
        This class tests the FlavorCommand
    """

    data = dotdict({
        "cloud": Default.cloud,
        "wrong_cloud": "no_cloud"
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
        return str(result)

    def setup(self):
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_001(self):
        HEADING("test flavor refresh")
        result = self.run("cm flavor refresh --cloud={cloud}")
        assert "ok" in result

    def test_002(self):
        HEADING("test flavor refresh fail")
        result = self.run("cm flavor refresh --cloud={wrong_cloud}")
        assert "failed" in result

    def test_003(self):
        HEADING("test flavor list")
        result = self.run("cm flavor list --cloud={cloud}")
        assert "Name" in result

    def test_004(self):
        HEADING("test flavor list fail")
        result = self.run("cm flavor list --cloud={wrong_cloud}")
        assert "failed" in result

    def test_005(self):
        HEADING("test flavor list ID")
        result = self.run("cm flavor list 1 --cloud={cloud}")
        assert "Value" in result

    def test_006(self):
        HEADING('test flavor list ID fail')
        result = self.run("cm flavor list i --cloud={wrong_cloud}")
        assert "failed" in result
