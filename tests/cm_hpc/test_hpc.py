""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_hpc/test_hpc.py:Test_hpc.test_001

python setup.py install; nosetests -v --nocapture tests/cm_hpc/test_hpc.py

or

nosetests -v tests/test_hpc.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING


def run(command):
    print(command)
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    print(result)
    return result


class Test_hpc():
    """
        This class tests the HpcCommand
    """
    data = {
        "cluster": "comet"
    }

    def setup(self):
        HEADING()
        result = run("cm default cluster={cluster}".format(**self.data))
        print (type(self.data["cluster"]))
        print (type(result))
        assert self.data["cluster"] in result

    def test_001(self):
        """
        test hpc info
        :return:
        """
        HEADING()
        result = run("cm hpc info --cluster={cluster}".format(**self.data))
        assert self.data["cluster"] in result

    def test_002(self):
        """
        test hpc queue
        :return:
        """
        HEADING()
        result = run("cm hpc queue --cluster={cluster}".format(**self.data))
        assert self.data["cluster"] in result

    def test_003(self):
        """
        test hpc status
        :return:
        """
        HEADING()
        result = run("cm hpc status --cluster={cluster}".format(**self.data))
        assert self.data["cluster"] in result