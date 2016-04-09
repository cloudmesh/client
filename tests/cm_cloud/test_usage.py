""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_usage.py:Test_usage.test_001

nosetests -v --nocapture tests/cm_cloud/test_usage.py

or

nosetests -v tests/test_usage.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default


# noinspection PyPep8Naming
class Test_usage:
    """
        This class tests the UsageCommand
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
        HEADING("cm usage list --cloud={cloud}".format(**self.data))
        result = self.run("cm usage list --cloud={cloud}")
        assert "start" in result
