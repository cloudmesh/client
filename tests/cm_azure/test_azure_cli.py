""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_azure/test_azure_cli.py:Test_flavor.test_001

nosetests -v --nocapture tests/cm_azure/test_azure_cli.py

or

nosetests -v tests/cm_azure/test_azure_cli.py

"""

import os
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from pprint import pprint

class Test_azure_cli:

    data = dotdict({
        "cloud": "azure",
    })

    def run(self, command):
        self.cloud = "azure"
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
        result = self.run("cm default cloud=azure")
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
        assert "Refresh VMs for cloud azure" in result

    def test_002(self):
        """
            Test VM list
        :return:
        """
        HEADING()
        result = self.run("cm vm list")
        assert "Listing VMs on Cloud: azure" in result

    def test_003(self):
        """
            Test Image refresh
        :return:
        """
        HEADING()
        result = self.run("cm image refresh")
        assert "Refresh image for cloud azure" in result

    def test_004(self):
        """
            Test Image list
        :return:
        """
        HEADING()
        result = self.run("cm image list")
        assert "image_family" in result

    def test_005(self):
        """
            Test Flavor refresh
        :return:
        """
        HEADING()
        result = self.run("cm flavor refresh")
        assert "Refresh flavor for cloud azure" in result

    def test_006(self):
        """
            Test Flavor list
        :return:
        """
        HEADING()
        result = self.run("cm flavor list")
        assert "web_worker_resource_disk_size" in result

    def test_007(self):
        """
            Test AKEY command test
        :return:
        """
        HEADING()
        # os.getcwd()
        pprint("This test will work only if mycer.pub,mycer.pem and mycer.pfx is copied to home directory")
        pprint("Current Working directory::"+os.getcwd())
        key_name = "test-key"
        pub_key_path = "~/mycer.pub"
        certificate_path = "~/mycer.pem"
        pfx_file_path = "~/mycer.pfx"
        cm_akey_command = "cm akey add --name="+key_name+" --pub="+pub_key_path+" --cert="+certificate_path+" --pfx="+pfx_file_path
        result = self.run(cm_akey_command)
        assert "Azure key added" in result

    def test_008(self):
        """
            Test VM create command
        :return:
        """
        HEADING()
        result = self.run("cm vm boot")
        assert "VM boot up successful" in result


    def test_009(self):
        """
            Test VM delete command
        :return:
        """
        HEADING()
        result = self.run("cm vm delete")
        assert "Delete Success" in result
