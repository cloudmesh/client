from __future__ import print_function

from cloudmesh_client.util import HEADING
from cloudmesh_client.common.Shell import Shell

""" run with

python setup.py install; nosetests -v --nocapture tests/test_limits.py:Test_nova.test_001

nosetests -v --nocapture tests/test_nova.py

or

nosetests -v tests/test_nova.py

"""


def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result


class Test_nova():
    """tests nova command"""

    data = {
        "cloud": "kilo",
        "group": "mygroup"
    }

    def setup(self):
        result = run("cm default group={group}".format(**self.data))
        print (result)
        #assert "{cloud} is set".format(**self.data) in result

    def test_001(self):
        """
        cm nova set <cloud>
        """

        HEADING()
        cloud = "india"
        result = run("cm nova set {cloud}".format(**self.data))
        print (result)
        assert "{cloud} is set".format(**self.data) in result

    def test_002(self):
        """
        cm nova info <cloud>
        """

        HEADING()
        result = run("cm nova info {cloud}".format(**self.data))
        print (result)
        assert "OK." in result

    def test_003(self):
        """
        cm nova list
        """

        HEADING()
        result = run("cm nova list")
        print (result)
        assert "+" in result

    def test_004(self):
        """
        cm nova image-list
        """

        HEADING()
        result = run("cm nova image-list")
        print (result)
        assert "ACTIVE" in result
