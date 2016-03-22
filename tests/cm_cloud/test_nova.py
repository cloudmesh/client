from __future__ import print_function

from cloudmesh_client.util import HEADING
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import banner

""" run with

python setup.py install; nosetests -v --nocapture tests/cm_cloud/test_nova.py:Test_nova.test_001

nosetests -v --nocapture tests/test_nova.py

or

nosetests -v tests/test_nova.py

"""




class Test_nova():
    """tests nova command"""

    data = {
        "cloud": "kilo",
        "group": "mygroup"
    }

    def setup(self):
        pass

    def run(self, command):
        command = command.format(**self.data)
        banner(command)
        print (command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return result

    def test_000(self):
        HEADING()
        command = "cm default group={group}"

        result = self.run(command)
        print(result)
        #assert "{cloud} is set".format(**self.data) in result

    def test_001(self):
        """
        cm nova set <cloud>
        """

        HEADING()
        command = "cm nova set {cloud}"
        result = self.run (command)
        print (result)
        assert "{cloud} is set".format(**self.data) in result

    def test_002(self):
        """
        cm nova info <cloud>
        """

        HEADING()
        command = "cm nova info {cloud}"
        result = self.run (command)
        print (result)
        assert "OK." in result

    def test_003(self):
        """
        cm nova list
        """

        HEADING()
        command = "cm nova list"
        result = self.run (command)
        print (result)
        assert "+" in result

    def test_004(self):
        """
        cm nova image-list
        """

        HEADING()
        command = "cm nova image-list"
        result = self.run (command)
        print (result)
        assert "ACTIVE" in result
