""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_register.py:Test_register.test_001

nosetests -v --nocapture tests/test_register.py

or

nosetests -v tests/test_register.py


from cloudmesh_client.util import banner
from cloudmesh_client.util import HEADING

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.default import Default

class Test_register:
    """
# tests
# for india only
"""
    data = dotdict({
        "cloud": Default.cloud,
        "group": "test",
        "vm": "testvm",
        "flavor": "TBD",
        "image": "TBD",
        "wrong_cloud": "no_cloud",
        "cert": "~/.cloudmesh/clouds/india/{cloud}/cacert.pem"
    })
    data.image = Default.get_image()
    data.flavor = Default.get_flavor()


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
        
        HEADING("testing cm register india")
        # os.sytem("yes | cm register india")
        result = self.run("cm register {cloud}")
        print(result)
        #result = Shell.cm("register", "india", "--force")
        assert "{cloud}".format(**self.data) in result
        assert "OS_AUTH_URL" in result


    def test_002(self):
        HEADING("testing cm register random1 --force")
        result = self.run ("cm register random1")
        assert "ERROR: executing" in result

    def test_003(self):
        HEADING("testing cm register list")
        result = self.run ("cm register list")
        assert "{cloud}".format(**self.data) in result

    def test_004(self):
        HEADING("testing cm register CLOUD CERT")
        result = self.run ("cm register {cloud}")
        assert "https://kilo.futuresystems.org:5000/v3" in result

    def test_005(self):
        HEADING("testing cm register info")
        result = self.run("cm register info")
        assert "exists" in result

    def test_006(self):
        HEADING("testing cm register cat")
        result = self.run("cm register cat")
        assert "yaml_version:" in result

    def test_007(self):
        HEADING("testing cm register cat --yaml=cloudmesh1.yaml")
        result = self.run("cm register cat --yaml=cloudmesh1.yaml")
        assert "ERROR: executing command" in result

    def test_008(self):
        HEADING("testing cm register edit --yaml=cloudmesh1.yaml")
        result = self.run("cm register edit --yaml=cloudmesh1.yaml")
        assert "ERROR: executing command" in result

    def test_009(self):
        HEADING("testing cm register list ssh")
        result = self.run("cm register list ssh")
        assert "india" in result

    def test_010(self):
        HEADING("testing cm register rc india")
        result = self.run("cm register remote")
        assert "Reading rc file from" in result

    def test_011(self):
        HEADING("testing cm register json india")
        result = self.run ("cm register json {cloud}")
        assert "openstack" in result

    def test_012(self):
        HEADING("testing cm register json hadoop")
        result = self.run ("cm register json hadoop")
        assert "Cloud hadoop is not described in cloudmesh.yaml" in result
"""