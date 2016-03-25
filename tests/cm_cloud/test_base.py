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

class Test_base:
    """
        This class tests the FlavorCommand
    """

    data = dotdict({
        "cloud": Default.get_cloud(),
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
        result = self.run("cm default cloud={cloud}")
        assert "ok" in result

    def test_002(self):
        result = self.run("cm default cloud")
        print (result)