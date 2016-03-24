""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_usage.py:Test_usage.test_001

nosetests -v --nocapture tests/cm_cloud/test_usage.py

or

nosetests -v tests/test_usage.py

"""

from cloudmesh_client.util import banner
from cloudmesh_client.util import HEADING

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict


class Test_usage:
    """
        This class tests the UsageCommand
    """

    data = dotdict({
        "cloud": "kilo",
        "wrong_cloud": "kilo_wrong"
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
        test list
        :return:
        """
        HEADING()
        result = self.run("cm usage list --cloud={cloud}")
        assert "start" in result