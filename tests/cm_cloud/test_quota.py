""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_quota.py:Test_quota.test_001

nosetests -v --nocapture tests/test_quota.py

or

nosetests -v tests/test_quota.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default


# noinspection PyPep8Naming
class Test_quota:
    """
        This class tests the QuotaCommand
    """

    data = dotdict({
        "cloud": Default.cloud,
        "format": "csv",
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
        HEADING("test quota list")
        result = self.run("cm quota list")
        assert "Quota" in result

    def test_002(self):
        HEADING("test quota list with csv output")
        result = self.run("cm quota list --cloud={cloud} --format={format}")
        assert "ram" in result

    def test_003(self):
        HEADING("test quota class where cloud doesnt exist")
        result = self.run("cm quota list --cloud={wrong_cloud}")
        assert "is not defined in the yaml file" in result
