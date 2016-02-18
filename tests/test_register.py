""" run with

python setup.py install; nosetests -v --nocapture  tests/test_register.py:Test_register.test_001

nosetests -v --nocapture tests/test_register.py

or

nosetests -v tests/test_register.py

"""
from __future__ import print_function
import os

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING


def run(command):
    print ("EXECUTING:", command)
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

        self.data = {
            "cloud": "kilo",
            "group": "test",
            "image": "Ubuntu-14.04-64",
            "vm": "testvm",
            "flavor": "m1.small"
        }


    def test_001(self):
        """testing cm register india"""
        HEADING()
        # os.sytem("yes | cm register india")
        result = run("cm register {cloud}".format(**self.data))
        print(result)
        #result = Shell.cm("register", "india", "--force")
        assert "{cloud}".format(**self.data) in result
        assert "OS_AUTH_URL" in result


    def test_002(self):
        """testing cm register random1 --force"""
        HEADING()
        result = run ("cm register random1")
        print (result)
        assert "ERROR: executing" in result

    def test_003(self):
        """testing cm register list"""
        HEADING()
        result = run ("cm register list")
        print (result)
        assert "{cloud}".format(**self.data) in result

    def test_004(self):
        """testing cm register CLOUD CERT"""
        HEADING()
        self.data["cert"] =  " ~/.cloudmesh/clouds/india/{cloud}/cacert.pem"
        result = run ("cm register {cloud}".format(**self.data))
        print (result)
        assert "https://kilo.futuresystems.org:5000/v3" in result

    def test_005(self):
        """testing cm register info"""
        HEADING()
        result = run("cm register info")
        print (result)
        assert "exists" in result

    def test_006(self):
        """testing cm register cat"""
        HEADING()
        result = run("cm register cat")
        print (result)
        assert "yaml_version:" in result

    def test_007(self):
        """testing cm register cat --yaml=cloudmesh1.yaml"""
        HEADING()
        result = run("cm register cat --yaml=cloudmesh1.yaml")
        print (result)
        assert "ERROR: executing command" in result

    def test_008(self):
        """testing cm register edit --yaml=cloudmesh1.yaml"""
        HEADING()
        result = run("cm register edit --yaml=cloudmesh1.yaml")
        print (result)
        assert "ERROR: executing command" in result

    def test_009(self):
        """testing cm register list ssh"""
        HEADING()
        result = run("cm register list ssh")
        print (result)
        assert "india" in result

    def test_010(self):
        """testing cm register rc india"""
        HEADING()
        result = run("cm register remote")
        print (result)
        assert "Reading rc file from" in result

    def test_011(self):
        """testing cm register json india"""
        HEADING()
        result = run ("cm register json {cloud}".format(**self.data))
        print (result)
        assert "openstack" in result

    def test_012(self):
        """testing cm register json hadoop"""
        HEADING()
        result = run ("cm register json hadoop")
        print (result)
        assert "Cloud hadoop is not described in cloudmesh.yaml" in result
