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
class Test_base:
    """
        This class tests the FlavorCommand
    """

    # noinspection PyTypeChecker
    data = dotdict({
        "cloud": Default.cloud,
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
        result = self.run("cm default cloud={cloud}")
        assert "ok" in result

    def test_002(self):
        HEADING("get default cloud")
        result = self.run("cm default cloud")
        print(result)
