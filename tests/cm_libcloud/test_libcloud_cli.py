""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_libcloud/test_libcloud_cli.py:Test_flavor.test_001

nosetests -v --nocapture tests/cm_libcloud/test_libcloud_cli.py

or

nosetests -v tests/cm_libcloud/test_libcloud_cli.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from pprint import pprint

class Test_libcloud_cli:

    data = dotdict({
        "cloud": "aws",
    })

    def run(self, command):
        self.cloud = "aws"
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
        HEADING()
        result = self.run("cm default cloud=aws")
        assert "ok." in result

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_001(self):
        """
            Test VM refresh
        :return:
        """
        HEADING()
        result = self.run("cm vm refresh")
        assert "Refresh VMs for cloud aws" in result

    def test_002(self):
        """
            Test VM list
        :return:
        """
        HEADING()
        result = self.run("cm vm list")
        assert "Listing VMs on Cloud: aws" in result

    # def test_003(self):
    #     """
    #         Test Image refresh
    #     :return:
    #     """
    #     HEADING()
    #     result = self.run("cm image refresh")
    #     assert "Refresh image for cloud aws" in result

    def test_004(self):
        """
            Test Image list
        :return:
        """
        HEADING()
        result = self.run("cm image list")
        assert "name" in result

    def test_005(self):
        """
            Test Flavor refresh
        :return:
        """
        HEADING()
        result = self.run("cm flavor refresh")
        assert "Refresh flavor for cloud aws" in result

    def test_006(self):
        """
            Test Flavor list
        :return:
        """
        HEADING()
        result = self.run("cm flavor list")
        assert "RAM" in result

    def test_007(self):
        """
            Test VM instance boot
        :return:
        """
        HEADING()
        result = self.run("cm vm boot")
        assert "VM boot up success" in result

    def test_008(self):
        """
            Test VM login
        :return:
        """
        HEADING()
        result = self.run("cm vm ssh")
        assert "Refresh flavor for cloud aws" in result
