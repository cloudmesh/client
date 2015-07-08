""" run with

python setup.py install; nosetests -v --nocapture  tests/test_vm.py:Test_register.test_001

nosetests -v --nocapture tests/test_vm.py

or

nosetests -v tests/test_vm.py

"""
from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import HEADING
import os

def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result

class Test_register():
    """

    """


    def setup(self):
        pass

    def test_001(self):
        """
        starts a vm
        :return:
        """
        HEADING()
        result = run ("cm vm start --cloud=india --flavor=m1.medium --image=futuresystems/ubuntu-14.04")
        print result
        assert True

    def test_002(self):
        """
        tries to start a vm with an invalid image
        :return:
        """
        HEADING()
        result = run ("cm vm start --cloud=india --flavor=m1.medium --image=futuresystems/linux>windows")

        assert "not found" in result
