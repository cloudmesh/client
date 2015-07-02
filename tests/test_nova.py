__author__ = 'daniel'
from cloudmesh_base.util import HEADING
from cloudmesh_base.Shell import Shell

""" run with

python setup.py install; nosetests -v --nocapture  tests/test_nova.py

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

    def test_001(self):
        """
        cm nova set india
        """

        HEADING()
        cloud = "india"
        result = run ("cm nova set {:}".format(cloud))
        print result
        assert "{:} is set".format(cloud) in result

    def test_002(self):
        """
        cm nova info india
        """

        HEADING()
        result = run ("cm nova info india")
        print ("resultado test 2: "+result)
        assert "OK." in result


