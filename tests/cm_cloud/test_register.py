""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_register.py:Test_register.test_001

nosetests -v --nocapture tests/test_register.py

or

nosetests -v tests/test_register.py

"""
from cloudmesh_client.util import banner
from cloudmesh_client.util import HEADING

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.default import Default

class Test_register:
    """
        tests for india only
    """

    data = dotdict({
        "cloud": Default.get_cloud(),
        "group": "test",
        "image": "Ubuntu-14.04-64",
        "vm": "testvm",
        "flavor": "m1.small",
        "wrong_cloud": "no_cloud",
        "cert": "~/.cloudmesh/clouds/india/{cloud}/cacert.pem"
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

    def test_001(self):
        """testing cm register india"""
        HEADING()
        # os.sytem("yes | cm register india")
        result = self.run("cm register {cloud}")
        print(result)
        #result = Shell.cm("register", "india", "--force")
        assert "{cloud}".format(**self.data) in result
        assert "OS_AUTH_URL" in result


    def test_002(self):
        """testing cm register random1 --force"""
        HEADING()
        result = self.run ("cm register random1")
        assert "ERROR: executing" in result

    def test_003(self):
        """testing cm register list"""
        HEADING()
        result = self.run ("cm register list")
        assert "{cloud}".format(**self.data) in result

    def test_004(self):
        """testing cm register CLOUD CERT"""
        HEADING()
        result = self.run ("cm register {cloud}")
        assert "https://kilo.futuresystems.org:5000/v3" in result

    def test_005(self):
        """testing cm register info"""
        HEADING()
        result = self.run("cm register info")
        assert "exists" in result

    def test_006(self):
        """testing cm register cat"""
        HEADING()
        result = self.run("cm register cat")
        assert "yaml_version:" in result

    def test_007(self):
        """testing cm register cat --yaml=cloudmesh1.yaml"""
        HEADING()
        result = self.run("cm register cat --yaml=cloudmesh1.yaml")
        assert "ERROR: executing command" in result

    def test_008(self):
        """testing cm register edit --yaml=cloudmesh1.yaml"""
        HEADING()
        result = self.run("cm register edit --yaml=cloudmesh1.yaml")
        assert "ERROR: executing command" in result

    def test_009(self):
        """testing cm register list ssh"""
        HEADING()
        result = self.run("cm register list ssh")
        assert "india" in result

    def test_010(self):
        """testing cm register rc india"""
        HEADING()
        result = self.run("cm register remote")
        assert "Reading rc file from" in result

    def test_011(self):
        """testing cm register json india"""
        HEADING()
        result = self.run ("cm register json {cloud}")
        assert "openstack" in result

    def test_012(self):
        """testing cm register json hadoop"""
        HEADING()
        result = self.run ("cm register json hadoop")
        assert "Cloud hadoop is not described in cloudmesh.yaml" in result
