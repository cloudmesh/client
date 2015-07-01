""" run with

python setup.py install; nosetests -v --nocapture  tests/test_register.py:Test_register.test_001

nosetests -v --nocapture tests/test_register.py

or

nosetests -v tests/test_register.py

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
        tests for india only
    """


    def setup(self):
        pass

    def test_001(self):
        """testing cm register india"""
        HEADING()
        # os.sytem("yes | cm register india")
        result = run("cm register india --force")
        #result = Shell.cm("register", "india", "--force")

        assert "ok." in result

    def test_002(self):
        """testing cm register random1 --force"""
        HEADING()
        result = run ("cm register random1 --force")
        assert "Could not execute the command." in result

    def test_003(self):
        """testing cm register india --foo"""
        HEADING()
        result = run ("cm register india --foo")

        assert "Could not execute the command." in result


    def test_004(self):
        """testing cm register CLOUD CERT"""
        HEADING()
        result = run ("cm register india .cloudmesh/clouds/india/juno/cacert.pem --force")
        assert "cert registered " in result

    def test_005(self):
        """testing cm register CLOUD CERT"""
        HEADING()

        result = run ("cm register india .cloudmesh/clouds/juno/d/cacert.pem --force")

        assert "ERROR" in result



