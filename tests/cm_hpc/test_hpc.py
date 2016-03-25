""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_hpc/test_hpc.py:Test_hpc.test_001

python setup.py install; nosetests -v --nocapture tests/cm_hpc/test_hpc.py

or

nosetests -v tests/test_hpc.py

"""

from cloudmesh_client.util import banner
from cloudmesh_client.util import HEADING

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict


class Test_hpc:
    """
        This class tests the HpcCommand
    """
    data = dotdict({
        "cluster": "comet",
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

    def setup(self):
        HEADING()
        result = self.run("cm default cluster={cluster}")
        assert "{cluster}".format(**self.data) in result

    def test_001(self):
        """test hpc info:return:"""
        HEADING()
        result = self.run("cm hpc info --cluster={cluster}")
        assert "{cluster}".format(**self.data) in result

    def test_002(self):
        """test hpc queue:return: """
        HEADING()
        result = self.run("cm hpc queue --cluster={cluster}")
        assert "{cluster}".format(**self.data) in result

    def test_003(self):
        """ test hpc status :return: """
        HEADING()
        result = self.run("cm hpc status --cluster={cluster}")
        assert "{cluster}".format(**self.data) in result