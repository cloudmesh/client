""" run with

python setup.py install; nosetests -v --nocapture tests/cm_cloud/test_nova.py:Test_nova.test_001

nosetests -v --nocapture tests/test_nova.py

or

nosetests -v tests/test_nova.py

"""

from cloudmesh_client.util import banner
from cloudmesh_client.util import HEADING

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.default import Default

class Test_nova:
    """tests nova command"""

    data = dotdict({
        "cloud": Default.get_cloud(),
        "group": "mygroup",
        "wrong_cloud": "no_cloud"
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

    def test_000(self):
        HEADING()
        result = self.run("cm default group={group}")
        #assert "{cloud} is set".format(**self.data) in result

    def test_001(self):
        """
        cm nova set <cloud>
        """
        HEADING()
        result = self.run ("cm nova set {cloud}")
        assert "{cloud} is set".format(**self.data) in result

    def test_002(self):
        """
        cm nova info <cloud>
        """
        HEADING()
        result = self.run ("cm nova info {cloud}")
        assert "OK." in result

    def test_003(self):
        """
        cm nova list
        """
        HEADING()
        result = self.run ("cm nova list")
        assert "+" in result

    def test_004(self):
        """
        cm nova image-list
        """
        HEADING()
        result = self.run ("cm nova image-list")
        assert "ACTIVE" in result
