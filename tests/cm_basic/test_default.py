""" self.run with

python setup.py install; nosetests -v --nocapture tests/cm_basic/test_default.py:Test_default.test_001

nosetests -v --nocapture tests/cm_basic/test_default.py

or

nosetests -v tests/cm_basic/test_default.py

"""
from __future__ import print_function

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default


# noinspection PyMethodMayBeStatic,PyMethodMayBeStatic,PyPep8Naming
class Test_default(object):
    """  """

    data = dotdict({
        "cloud": Default.cloud,
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
        defaults = Default.list()
        print("LIST:", defaults)
        assert defaults is None

    def test_002(self):
        HEADING("list default cloud")
        result = Default.list()
        print("LIST:", result)
        # assert result is None

        print("------")
        name = self.data.cloud
        print("Name", name, self.data, self.data.cloud)
        Default.set("cloud", name)
        print("HHH", Default.cloud)
        print("------")

        result = Default.list()
        print("LIST:", result)

        print("Default.cloud", Default.cloud)

        assert Default.cloud == name

    def test_003(self):
        HEADING("set default image")
        name = self.data.image

        print(self.data)
        Default.set_image(name, self.data.cloud)

        print(Default.get(name=name, category=self.data.cloud))

        assert Default.get(name="image", category=self.data.cloud) == name

    def test_004(self):
        HEADING("set default flavor")
        name = "myflavor"
        Default.set_flavor(name, self.data.cloud)
        assert Default.get_flavor(self.data.cloud) == name

    def test_005(self):
        HEADING("set default key ")
        name = "mykey"
        Default.set_key(name)
        assert Default.key == name

    def test_006(self):
        HEADING("set default key  ")
        name = "mygroup"
        Default.set_group(name)
        assert Default.group == name

    def test_007(self):
        HEADING(" set default variable ")
        name = "myvar"
        value = "myvalue"
        cloud = self.data.cloud
        Default.set(name, value, cloud)
        assert Default.get(name=name, category=cloud) == value

    def test_008(self):
        HEADING("cm default test=testValue --cloud={cloud}"
                .format(**self.data))
        result = self.run("cm default test=testValue --cloud={cloud}")
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
        result = self.run("cm default list")
        assert "test" in result
        print(result)
        result = self.run("cm default delete test --cloud={cloud}")
        assert "ERROR" not in str(result)

    def test_012(self):
        HEADING("cm default delete doesnotexist --cloud={cloud}"
                .format(**self.data))
        result = self.run("cm default delete doesnotexist --cloud={cloud}")
        assert "doesnotexist not present" in str(result)

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
