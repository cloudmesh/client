""" run with

python setup.py install; nosetests -v --nocapture  tests/test_register.py:Test_register.test_001

nosetests -v --nocapture tests/test_register.py

or

nosetests -v tests/test_register.py

"""
import os

from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import HEADING


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
        """testing cm register list"""
        HEADING()
        result = run ("cm register list")
        assert "india" in result

    def test_005(self):
        """testing cm register CLOUD CERT"""
        HEADING()
        cert =  " ~/.cloudmesh/clouds/india/juno/cacert.pem"
        result = run ("cm register india {} --force".format(cert))
        assert "cert registered " in result

    def test_006(self):
        """testing cm register CLOUD CERT"""
        HEADING()
        cert =  " ~/.cloudmesh/clouds/donotexist/juno/cacert.pem"
        result = run ("cm register india {} --force".format(cert))
        assert "ERROR" in result

    def test_007(self):
        """testing cm register info"""
        HEADING()
        result = run("cm register info")
        assert "exists" in result

    def test_008(self):
        """testing cm register cat"""
        HEADING()
        result = run("cm register cat")
        assert "yaml_version:" in result

    def test_009(self):
        """testing cm register cat --yaml=cloudmesh1.yaml"""
        HEADING()
        result = run("cm register cat --yaml=cloudmesh1.yaml")
        assert "doesn't exist" in result

    def test_010(self):
        """testing cm register edit --yaml=cloudmesh1.yaml"""
        HEADING()
        result = run("cm register edit --yaml=cloudmesh1.yaml")
        assert "doesn't exist" in result

    def test_011(self):
        """testing cm register list ssh"""
        HEADING()
        result = run("cm register list ssh")
        assert "The following hosts are defined in ~/.ssh/config" in result

    def test_012(self):
        """testing cm register rc india"""
        HEADING()
        result = run("cm register rc india")
        assert "Reading rc file from" in result

    def test_013(self):
        """testing cm register rc india --version=juno"""
        HEADING()
        result = run("cm register rc india --version=juno")
        assert "Reading rc file from" in result

    def test_014(self):
        """testing cm register rc doesntexist"""
        HEADING()
        result = run("cm register rc doesntexist")
        assert "ERROR: No openrc file specified or found" in result

    def test_015(self):
        """testing cm register json india"""
        HEADING()
        result = run ("cm register json india")
        assert "openstack" in result

    def test_016(self):
        """testing cm register json hadoop"""
        HEADING()
        result = run ("cm register json hadoop")
        assert "Cloud hadoop is not described in cloudmesh.yaml" in result
