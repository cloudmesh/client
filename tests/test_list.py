""" run with

python setup.py install; nosetests -v --nocapture  tests/test_list.py:Test_list.test_001

nosetests -v --nocapture tests/test_list.py

or

nosetests -v tests/test_list.py

"""
import os

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING
from cloudmesh_client.util import banner
from cloudmesh_client.cloud.list import List


class Test_list:

    def D(self, line):
        return (line.format(**self.data))

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c='-')
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return result

    def setup(self):

            self.data = {
                "cloud": "kilo",
                "default": "mydefault",
                "value": "hallo"
        }

    def tearDown(self):
        pass

    def test_001(self):
        """testing cm list --cloud kilo default"""
        HEADING()

        result = self.run('cm default {default}=hallo')
        # set default
        result = self.run("cm default list --cloud={cloud}")
        assert self.D("{default}") in result

        result = self.run("cm list --cloud={cloud} default")
        assert self.D("{value}") in result

        # delete the default name
        result = self.run("cm default delete {default} --cloud={cloud}")

        assert "ok." in result

        return

    def test_002(self):
        """testing cm list --cloud kilo --format json default"""
        HEADING()

        result = self.run("cm default --cloud={cloud} {default}={value}")
        assert "ok." in result

        result = self.run("cm list --cloud={cloud} --format=json default")
        assert "hallo" in result

        # delete the default name
        result = self.run("cm default delete {default} --cloud={cloud}")
        assert "ok." in result

        return

    def test_003(self):
        """testing cm list --cloud trial --user fake default"""
        HEADING()
        banner("cm list --cloud=trial --user=fake default")

        result = self.run("cm list --cloud=trial --user=fake default")
        assert "No" in result

        return