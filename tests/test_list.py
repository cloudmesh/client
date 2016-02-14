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
    banner(command, c='-')
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    print(result)
    return result

class Test_list:

    def setup(self):

            self.data = {
            "cloud": "kilo",
            "group": "test",
            "image": "Ubuntu-14.04-64",
            "vm": "testvm",
            "flavor": "m1.small"
        }

    def tearDown(self):
        pass

    def test_001(self):
        """testing cm list --cloud india default"""
        HEADING()
        banner("cm list --cloud={cloud} default")

        # set default
        result = run("cm default --cloud={cloud}")
        assert "value"

        result = run("cm list --cloud={cloud} default")
        assert "hallo" in result

        # delete the default name
        run("cm default delete name --cloud={cloud}")
        assert "Deleted key name"

        return

    def test_002(self):
        """testing cm list --cloud kilo --format json default"""
        HEADING()
        banner("cm list --cloud={cloud} --format json default")

        run("cm default --cloud={cloud} testvar=hallo")
        assert "Successfully added name"

        result = run("cm list --cloud={cloud} --format=json default")
        assert "hallo" in result

        # delete the default name
        run("cm default delete name --cloud={cloud}")
        assert "Deleted key name"

        return

    def test_003(self):
        """testing cm list --cloud trial --user fake default"""
        HEADING()
        banner("cm list --cloud=trial --user=fake default")

        result = run("cm list --cloud=trial --user=fake default")
        assert "No" in result

        return