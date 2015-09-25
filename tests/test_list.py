""" run with

python setup.py install; nosetests -v --nocapture  tests/test_list.py:Test_list.test_001

nosetests -v --nocapture tests/test_list.py

or

nosetests -v tests/test_list.py

"""
import os

from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import HEADING
from cloudmesh_base.util import banner
from cloudmesh_client.cloud.list import List

def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result

class Test_list:

    def setup(self):

        pass

    def tearDown(self):
        pass

    def test_001(self):
        """testing cm list --cloud india default"""
        HEADING()
        banner("cm list --cloud india default")

        # set default name=gourav
        run("cm default --cloud india name=gourav")
        assert "Successfully added name"

        result = run("cm list --cloud india default")
        assert "gourav" in result

        # delete the default name
        run("cm default delete name --cloud india")
        assert "Deleted key name"

        return

    def test_002(self):
        """testing cm list --cloud india --format json default"""
        HEADING()
        banner("cm list --cloud india --format json default")

        # set default name=gourav
        run("cm default --cloud india name=gourav")
        assert "Successfully added name"

        result = run("cm list --cloud india --format json default")
        assert "gourav" in result

        # delete the default name
        run("cm default delete name --cloud india")
        assert "Deleted key name"

        return

    def test_003(self):
        """testing cm list --cloud trial --user fake default"""
        HEADING()
        banner("cm list --cloud trial --user fake default")

        result = run("cm list --cloud trial --user fake default")
        assert "List empty for [DEFAULT] in the database!" in result

        return