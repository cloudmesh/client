""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_hpc/test_hpc.py:Test_hpc.test_001

python setup.py install; nosetests -v --nocapture tests/cm_hpc/test_hpc.py

or

nosetests -v tests/test_hpc.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner


# noinspection PyPep8Naming
class Test_hpc:
    """
        This class tests the HpcCommand
    """
    # noinspection PyTypeChecker
    data = dotdict({
        "cluster": "comet",
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

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def setup(self):
        HEADING("set default cluster")
        result = self.run("cm default cluster={cluster}")
        assert "{cluster}".format(**self.data) in result

    def test_001(self):
        HEADING("test hpc info")
        result = self.run("cm hpc info --cluster={cluster}")
        assert "{cluster}".format(**self.data) in result

    def test_002(self):
        HEADING("test hpc queue ")
        result = self.run("cm hpc queue --cluster={cluster}")
        assert "{cluster}".format(**self.data) in result

    def test_003(self):
        HEADING(" test hpc status  ")
        result = self.run("cm hpc status --cluster={cluster}")
        assert "{cluster}".format(**self.data) in result
