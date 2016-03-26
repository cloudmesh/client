""" self.run with

python setup.py install; nosetests -v --nocapture tests/cm_basic/test_default.py:Test_default.test_001

nosetests -v --nocapture tests/cm_basic/test_default.py

or

nosetests -v tests/cm_basic/test_default.py

"""
from __future__ import print_function
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING

from cloudmesh_client.default import Default
from cloudmesh_client.util import banner
from cloudmesh_client.common.dotdict import dotdict


# noinspection PyMethodMayBeStatic,PyMethodMayBeStatic,PyPep8Naming
class Test_default(object):
    """  """

    data = dotdict({
        "cloud": Default.get_cloud(),
        "image": "myimage",
        "flavor": "myflavor"
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

    def test_001(self):
        HEADING("delete defaults")
        Default.clear()
        assert Default.list() is None

    def _check(self, content):
        result = Default.list()
        print(result)
        assert content in str(result)

    def test_002(self):
        HEADING("list default cloud")
        result = Default.list()
        print(result)

        name = self.data.cloud
        Default.set_cloud(name)

        result = Default.list()
        print(result)

        print("KKK", Default.get_cloud())

        assert Default.get_cloud() == name
        self._check(name)

    def test_003(self):
        HEADING("set default image")
        name = self.data.image
        Default.set_image(name, self.data.cloud)
        assert Default.get_image(self.data.cloud) == name
        self._check(name)

    def test_004(self):
        HEADING("set default flavor")
        name = "myflavor"
        Default.set_flavor(name, self.data.cloud)
        assert Default.get_flavor(self.data.cloud) == name
        self._check(name)

    def test_005(self):
        HEADING("set default key ")
        name = "mykey"
        Default.set_key(name)
        assert Default.get_key() == name
        self._check(name)

    def test_006(self):
        HEADING("set default key  ")
        name = "mygroup"
        Default.set_group(name)
        assert Default.get_group() == name
        self._check(name)

    def test_007(self):
        HEADING(" set default variable ")
        name = "myvar"
        value = "myvalue"
        cloud = self.data.cloud
        Default.set(name, value, cloud)
        assert Default.get(name, cloud) == value
        self._check(value)

    def test_008(self):
        HEADING("cm default test=testValue --cloud={cloud}"
                .format(**self.data))
        result = self.run("cm default test=testValue --cloud={cloud}")
        print("HHHH", result)

        assert "ok." in result

    def test_009(self):
        HEADING("cm default test --cloud={cloud}"
                .format(**self.data))
        self.run("cm default test=testValue --cloud={cloud}")
        result = self.run("cm default test --cloud={cloud}")
        assert "testValue" in result

    def test_010(self):
        HEADING("cm default doesnotexist --cloud={cloud}"
                .format(**self.data))
        result = self.run("cm default doesnotexist --cloud={cloud}")
        assert "No default values found" in result

    def test_011(self):
        HEADING("cm default delete test")
        self.run("cm default test=testValue --cloud={cloud}")
        result = self.run("cm default delete test --cloud={cloud}")
        assert "Deleted key" in result

    def test_012(self):
        HEADING("cm default delete doesnotexist --cloud={cloud}"
                .format(**self.data))
        result = self.run("cm default delete doesnotexist --cloud={cloud}")
        assert "Key doesnotexist not present" in result

    def test_999(self):
        HEADING("clear the defaults")

        Default.clear()
        Default.set_cloud(self.data.cloud)
        assert True

    '''
    def test_002(self):
        HEADING("tries to start a vm with an invalid image")
        result = self.run ("cm vm start --cloud=india --flavor=m1.medium --image=futuresystems/linux>windows")

        assert "not found" in result
    '''
