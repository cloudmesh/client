""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_vm.py:Test_vm.test_001

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default


# noinspection PyPep8Naming
class Test_vm:
    data = dotdict({
        "wrong_cloud": "no_cloud",
        "cloud": Default.cloud,
        "group": "test",
        "image": Default.get_image(category=Default.cloud),
        "flavor": Default.get_flavor(category=Default.cloud),
        "vm": "{}_testvm".format(Default.user),
        "vm_rename": "{}_renamed_testvm".format(Default.user),
    })
    data.image = Default.get_image()
    data.flavor = Default.get_flavor()

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

    def load_key(self):
        try:
            self.run("cm key load")
            result = self.run("cm key upload")
        except Exception as e:
            print(e)


    def test_000(self):
        HEADING("key upload")
        command= "cm key add --ssh"
        result = self.run(command)

    def test_001(self):
        HEADING("cm vm boot --name={vm} --cloud={cloud} --image={image} --flavor=2 --group={group}".format(**self.data))
        self.load_key()
        command = "cm vm boot --name={vm} --cloud={cloud} --image={image}" + \
                  " --flavor={flavor} --group={group}"
        result = self.run(command)
        assert "OK." in result

    def test_002(self):
        HEADING("cm vm refresh --cloud={cloud}".format(**self.data))
        result = self.run("cm vm refresh --cloud={cloud}")
        assert "OK." in result

    def test_003(self):
        HEADING("cm vm list --cloud={cloud}".format(**self.data))
        result = self.run("cm vm list --cloud={cloud}")
        assert "Listing VMs on Cloud: {cloud}".format(**self.data) in result

    def test_004(self):
        HEADING("cm vm list {vm} --cloud={cloud}".format(**self.data))
        result = self.run("cm vm list {vm} --cloud={cloud}")
        assert "Listing VMs on Cloud: {cloud}".format(**self.data) in result

    def test_005(self):
        HEADING("cm vm status --cloud={cloud}".format(**self.data))
        result = self.run("cm vm status --cloud={cloud}")
        assert "OK." in result

    def test_006(self):
        from pprint import pprint; pprint(self.data)
        HEADING("cm vm ip show {vm} --cloud={cloud}".format(**self.data))
        result = self.run("cm vm list --refresh --cloud={cloud}")

        result = self.run("cm vm ip show {vm} --cloud={cloud}")
        assert "name" in result
        assert "{vm}".format(**self.data) in result

    def test_007(self):
        HEADING("cm vm rename {vm} {vm_rename}".format(**self.data))
        result = self.run("cm vm rename {vm} {vm_rename}")
        assert "OK." in result

    def test_008(self):
        HEADING("cm vm delete {vm_rename} --cloud={cloud} ".format(**self.data))
        result = self.run("cm vm delete {vm_rename} --cloud={cloud}")
        assert "OK." in result

    def test_009(self):
        HEADING("testing purgeing a vm")
        result = self.run("cm key add --ssh")
        result = self.run("cm info")
        result = self.run("cm vm boot")
        result = self.run("cm vm list")
        result = self.run("cm vm delete last")
        result = self.run("cm vm list")

    '''
    def test_009(self):
        from pprint import pprint;
        pprint(self.data)
        HEADING("cm vm ip assign {vm} --cloud={cloud}".format(**self.data))
        result = self.run("cm vm list --refresh --cloud={cloud}")

        result = self.run("cm vm ip show {vm} --cloud={cloud}")
        assert "name" in result
        assert "{vm}".format(**self.data) in result
    '''
