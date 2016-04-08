""" run with


python setup.py install; nosetests -v --nocapture tests/cm_cloud/test_reservation.py:Test_reservation.test_001
python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_reservation.py

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default


# noinspection PyPep8Naming
class Test_reservation:
    data = dotdict({
        "cloud": Default.cloud,
        "json": "json",
        "yaml": "yaml",
        "user": "albert",
        "name": "test_name",
        "project": "cloudmesh",
        "wrong_cloud": "no_cloud",
        "category": Default.cloud
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

    def setup(self):
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_001(self):
        HEADING(
            "cm reservation add --name=test "
            "--start='10/31/1988\ at\ 8:09\ pm' "
            "--end='10/21/2015\ at\ 9:00\ pm' "
            "--user=albert --project=cloudmesh "
            "--hosts=host001 --description=desc")
        result = self.run("cm reservation add --name={name} "
                          "--start='10/31/1988\ at\ 8:09\ pm' "
                          "--end='10/21/2015\ at\ 9:00\ pm' "
                          "--user={user} --project={project}")
        assert "OK." in result

    def test_002(self):
        HEADING("cm reservation list")
        result = self.run("cm reservation list")
        assert "OK." in result

    def test_003(self):
        HEADING("cm reservation list --user=albert")
        result = self.run("cm reservation list --user={user}")
        assert "OK." in result

    def test_004(self):
        HEADING("cm reservation list --user=albert --format=json")
        result = self.run("cm reservation list --user={user} --format={json}")
        assert "OK." in result

    def test_005(self):
        HEADING("cm reservation list --user=albert --format=yaml")
        result = self.run("cm reservation list --user={user} --format={yaml}")
        assert "OK." in result

    def test_006(self):
        HEADING("cm reservation update --name=test_name --project=another_proj")
        result = self.run("cm reservation update --name={name} --project=another_proj")
        assert "OK." in result

    def test_007(self):
        HEADING("cm reservation delete --name=test_name")
        result = self.run("cm reservation delete --name={name}")
        assert "OK." in result

    def test_008(self):
        HEADING("cm reservation delete all")
        result = self.run("cm reservation delete all")
        assert "OK." in result
