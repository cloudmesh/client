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
        command= "cm key add --ssh"
        HEADING(command)
        result = self.run(command)

    def test_001(self):
        HEADING("cm vm boot --name=testvm --cloud=cloud --image=<image_id> --flavor=2 --group=test")
        self.load_key()
        command = "cm vm boot --name={vm} --cloud={cloud} --image={image}" + \
                  " --flavor={flavor} --group={group}"
        result = self.run(command)
        assert "OK." in result

    def test_002(self):
        HEADING("cm vm refresh --cloud=cloud")
        result = self.run("cm vm refresh --cloud={cloud}")
        assert "OK." in result

    def test_003(self):
        HEADING("cm vm list --cloud=cloud")
        result = self.run("cm vm list --cloud={cloud}")
        assert "OK." in result

    def test_004(self):
        HEADING("cm vm list testvm --cloud=cloud")
        result = self.run("cm vm list {vm} --cloud={cloud}")
        assert "OK." in result

    def test_005(self):
        HEADING("cm vm status --cloud=cloud")
        result = self.run("cm vm status --cloud={cloud}")
        assert "OK." in result

    def test_006(self):
        HEADING("cm vm ip_show testvm --cloud=cloud")
        result = self.run("cm vm ip show {vm} --cloud={cloud}")
        assert "OK." in result

    def test_007(self):
        HEADING("cm vm rename testvm --new=test_renamed_vm --cloud=cloud")
        result = self.run("cm vm rename {vm} --new={vm_rename} --cloud={cloud}")
        assert "OK." in result

    def test_008(self):
        HEADING("cm vm delete test_renamed_vm --cloud=cloud")
        result = self.run("cm vm delete {vm_rename} --cloud={cloud}")
        assert "OK." in result
