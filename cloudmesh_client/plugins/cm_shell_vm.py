from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_vm import command_vm


class cm_shell_vm:
    def activate_cm_shell_vm(self):
        self.register_command_topic('cloud', 'vm')

    @command
    def do_vm(self, args, arguments):
        """
        ::

          Usage:
              vm list [--output=FORMAT]


          managing the vms test test test test

          Arguments:

            KEY    the name of the vm
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [vm: general]
             --output=FORMAT  the output format [vm: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_vm()
    command.do_vm("list")
    command.do_vm("a=x")
    command.do_vm("x")
