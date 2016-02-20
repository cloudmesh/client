""" run with

python setup.py install; nosetests -v --nocapture  tests/test_scripts.py

nosetests -v --nocapture tests/test_scripts.py

or

nosetests -v tests/test_scripts.py

"""
from __future__ import print_function

from cloudmesh_client.util import HEADING
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import banner



class Test_script():
    """tests script command"""

    data = {
        "cloud": "kilo",
        "group": "mygroup"
    }

    def run(self, command):
        command = command.format(**self.data)
        banner(command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print (result)
        return result

    def setup(self):
        self.scripts = [
            ("bash.cm", "README.rst"),
            ("comment.cm", "/* test"),
            ("var.cm", "username"),
            ("py.cm", "2"),
            ("terminal.cm", ""),
            #("hpc.cm", "bravo"),
            ("key.cm", ""),
            ("reservedemo.cm", "cloudnauts"),
            #("cloud.cm", "Active"),
            #("nova.cm", "Status"),
            #("demo.cm", "ephemeral_disk"),


            # BROKEN:
            #("group.cm", ""),
            #("sync.cm", ""),
            #("secgroup.cm", ""),
            #("cluster.cm", ""),
            #("vm.cm", ""),
            #("network.cm", ""),

        ]
        pass

    def test_001(self):
        """
        cm script set india
        """

        HEADING()
        for self.data["script"], self.data["check"] in self.scripts:
            command = "cm scripts/{script}"
            result = self.run(command)
            print (result)
            assert self.data["check"] in result


