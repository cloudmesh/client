""" run with

python setup.py install; nosetests -v --nocapture tests/cm_cloud/test_nova.py:Test_nova.test_001

nosetests -v --nocapture tests/test_nova.py

or

nosetests -v tests/test_nova.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default


# noinspection PyPep8Naming
class Test_nova:
    """tests nova command"""

    data = dotdict({
        "cloud": Default.cloud,
        "group": "mygroup",
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

    def test_000(self):
        HEADING("set the default group")
        result = self.run("cm default group={group}")
        # assert "{cloud} is set".format(**self.data) in result

    def test_001(self):
        HEADING("cm nova set <cloud>")
        result = self.run("cm nova set {cloud}")
        assert "{cloud} is set".format(**self.data) in result

    def test_002(self):
        HEADING("cm nova info <cloud>")
        result = self.run("cm nova info {cloud}")
        assert "OK." in result

    def test_003(self):
        HEADING("cm nova list")
        result = self.run("cm nova list")
        assert "+" in result

    def test_004(self):
        HEADING("cm nova image-list")
        result = self.run("cm nova image-list")
        assert "ACTIVE" in result
