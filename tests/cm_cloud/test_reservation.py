""" run with


python setup.py install; nosetests -v --nocapture tests/test_reservation.py:Test_reservation.test_001
python setup.py install; nosetests -v --nocapture  tests/test_reservation.py

nosetests -v --nocapture

or

nosetests -v

"""

# from cloudmesh_client.keys.SSHKeyManager import SSHKeyManager
# from cloudmesh_client.keys.SSHkey import SSHkey
# from cloudmesh_client.db.SSHKeyDBManager import SSHKeyDBManager
# from cloudmesh_client.common.Printer import dict_printer

from __future__ import print_function
from cloudmesh_client.util import HEADING

from cloudmesh_client.common.Shell import Shell


def run(command):
    print (command)
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    print (result)
    return str(result)


class Test_reservation:
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """
        cm reservation add --name=test --start='10/31/1988\ at\ 8:09\ pm' --end='10/21/2015\ at\ 9:00\ pm'
        --user=albert --project=cloudmesh --hosts=host001 --description=desc
        """
        HEADING()
        result = run("cm reservation add --name=test_name --start='10/31/1988\ at\ 8:09\ pm' \
                      --end='10/21/2015\ at\ 9:00\ pm' --user=albert --project=cloudmesh")
        assert "OK." in result

    def test_002(self):
        """
        cm reservation list
        """
        HEADING()
        result = run("cm reservation list")
        assert "OK." in result

    def test_003(self):
        """
        cm reservation list --user=albert
        """
        HEADING()
        result = run("cm reservation list --user=albert")
        assert "OK." in result

    def test_004(self):
        """
        cm reservation list --user=albert --format=json
        """

        HEADING()
        result = run("cm reservation list --user=albert --format=json")
        assert "OK." in result

    def test_005(self):
        """
        cm reservation list --user=albert --format=yaml
        """

        HEADING()
        result = run("cm reservation list --user=albert --format=yaml")
        assert "OK." in result

    def test_006(self):
        """
        cm reservation update --name=test_name --project=another_proj
        """

        HEADING()
        result = run("cm reservation update --name=test_name --project=another_proj")
        assert "OK." in result

    def test_007(self):
        """
        cm reservation delete --name=test_name
        """

        HEADING()
        result = run("cm reservation delete --name=test_name")
        assert "OK." in result

    def test_008(self):
        """
        cm reservation delete all
        """

        HEADING()
        result = run("cm reservation delete all")
        assert "OK." in result
