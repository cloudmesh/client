""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_limits.py:Test_limits.test_001

nosetests -v --nocapture tests/test_limits.py

or

nosetests -v tests/test_limits.py

"""

from cloudmesh_client.util import banner
from cloudmesh_client.util import HEADING

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.default import Default
from cloudmesh_client.common.ConfigDict import ConfigDict


# noinspection PyPep8Naming
class Test_limits:
    """
        This class tests the LimitsCommand
    """

    data = dotdict({
        "cloud": Default.get_cloud(),
        "wrong_cloud": "no_cloud",
        "tenant": "TBD"
    })
    config = ConfigDict("cloudmesh.yaml")
    data.tenant = config["cloudmesh"]["clouds"][data.cloud]["credentials"]["OS_TENANT_ID"]

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
        HEADING("test limits list")
        result = self.run("cm limits list --cloud={cloud}")
        assert "Name" in result

    def test_002(self):
        HEADING("test limits list with csv output")
        result = self.run("cm limits list --format={format}").split('\n')
        assert "maxTotalFloatingIps" in result[0]

    def test_003(self):
        HEADING("test limits class where cloud doesnt exist")
        result = self.run("cm limits list --cloud={wrong_cloud}")
        assert "Error" in result

    def test_004(self):
        HEADING("test limits class with unauthorised access")
        result = self.run("cm limits list --tenant={tenant}")
        assert "Not authorized" in result
