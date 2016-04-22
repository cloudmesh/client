""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_image.py:Test_image.test_001

nosetests -v --nocapture tests/test_image.py

or

nosetests -v tests/test_image.py

"""
from __future__ import print_function

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.image import Image
from pprint import pprint

# noinspection PyPep8Naming
class Test_image:
    """
        This class tests the ImageCommand
    """

    data = dotdict({
        "cloud": Default.cloud,
        "wrong_cloud": "no_cloud",
        "format": "json"
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
        HEADING("test image refresh")
        result = self.run("cm image refresh --cloud={cloud}")
        assert "ok." in result

    def test_002(self):
        HEADING("test image refresh fail")
        result = self.run("cm image refresh --cloud={wrong_cloud}")
        assert "failed" in result

    def test_003(self):
        HEADING("test image list")
        result = self.run("cm image list --cloud={cloud}")
        assert "description" in result

    def test_004(self):
        HEADING("test image list fail")
        result = self.run("cm image list --cloud={wrong_cloud}")
        assert "failed" in result

    def test_005(self):
        HEADING("test image list ID")
        result = self.run("cm image list --cloud={cloud} --format={format}")
        assert "Ubuntu" in result

    def test_006(self):
        HEADING("test image list ID fail")
        result = self.run("cm image list i --cloud={wrong_cloud}")
        assert "failed" in result

    def test_007(self):
        HEADING("test image username guess")

        result = Image.guess_username("Ubuntu-image")
        print(result)
        assert result == "ubuntu"

        result = Image.guess_username("wily-image")
        print(result)
        assert result == "ubuntu"

        result = Image.guess_username("fedora-image")
        print(result)
        assert result == "root"

        result = Image.guess_username("image", description="image with wily")
        print(result)
        assert result == "ubuntu"

    def test_008(self):
        HEADING("test image get username")

        # this test only works on chameleon
        if not Default.cloud in ["cm","chameleon"]:
            assert True

        result = self.run("cm image list --refresh")

        Image.set_username(name="CC-Ubuntu14.04", cloud=Default.cloud, username="undefined")
        result = Image.get_username("CC-Ubuntu14.04", Default.cloud)
        print ('Username:', result)
        assert "undefined" in result

        Image.set_username(name="CC-Ubuntu14.04", cloud=Default.cloud, username=None)
        result = Image.get_username("CC-Ubuntu14.04", Default.cloud, guess=True)
        print("Username:", result)


        assert "cc" in result


    def test_009(self):
        HEADING("test image get username")

        # this test only works on chameleon
        if not Default.cloud in ["cm", "chameleon"]:
            assert True

        login  = Image.get_username("CC-Ubuntu14.04", Default.cloud, guess=True)

        print ("LOGIN", login)

        Image.set_username(name="CC-Ubuntu14.04", cloud=Default.cloud, username=login)

        result  = Image.get_username("CC-Ubuntu14.04", Default.cloud)


        print(result)

