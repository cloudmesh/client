""" run with

python setup.py install; nosetests -v --nocapture  tests/test_reservation.py

nosetests -v --nocapture

or

nosetests -v

"""

# from cloudmesh_client.keys.SSHKeyManager import SSHKeyManager
# from cloudmesh_client.keys.SSHkey import SSHkey
# from cloudmesh_client.db.SSHKeyDBManager import SSHKeyDBManager
# from cloudmesh_client.common.tables import dict_printer

from cloudmesh_base.util import HEADING

from cloudmesh_base.Shell import Shell


def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result


class Test_reservation:
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """
        cm reservation add --name=test_name --start="2015-09-30" --end="2016-09-30" --user=albert --project=cloudmesh
        --hosts=host001 --description=desc
        """
        HEADING()
        result = run('cm reservation add --name=test_name --start=2015-09-30 --end=2016-09-30 --user=albert \
                                                                                            --project=cloudmesh \
                                                                                            --hosts=host001 \
                                                                                            --description=desc')
        print result
        assert "OK." in result

    def test_002(self):
        """
        cm reservation list
        """
        HEADING()
        result = run("cm reservation list")
        print result
        assert "OK." in result

    def test_003(self):
        """
        cm reservation list --user=albert
        """
        HEADING()
        result = run("cm reservation list --user=albert")
        print result
        assert "OK." in result

    def test_004(self):
        """
        cm reservation list --user=albert --format=json
        """

        HEADING()
        result = run("cm reservation list --user=albert --format=json")
        print result
        assert "OK." in result

    def test_005(self):
        """
        cm reservation list --user=albert --format=yaml
        """

        HEADING()
        result = run("cm reservation list --user=albert --format=yaml")
        print result
        assert "OK." in result

    def test_006(self):
        """
        cm reservation update --name=test_name --project=another_proj
        """

        HEADING()
        result = run("cm reservation update --name=test_name --project=another_proj")
        print result
        assert "OK." in result

    def test_007(self):
        """
        cm reservation delete --name=test_name
        """

        HEADING()
        result = run("cm reservation delete --name=test_name")
        print result
        assert "OK." in result

    def test_008(self):
        """
        cm reservation delete all
        """

        HEADING()
        result = run("cm reservation delete all")
        print result
        assert "OK." in result
