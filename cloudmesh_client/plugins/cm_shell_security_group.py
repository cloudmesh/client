from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_security_group import command_security_group


class cm_shell_security_group:
    def activate_cm_shell_security_group(self):
        self.register_command_topic('cloud', 'security_group')

    @command
    def do_security_group(self, args, arguments):
        """
        ::

          Usage:
              security_group list [--output=FORMAT]


          managing the security_groups test test test test

          Arguments:

            KEY    the name of the security_group
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [security_group: general]
             --output=FORMAT  the output format [security_group: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_security_group()
    command.do_security_group("list")
    command.do_security_group("a=x")
    command.do_security_group("x")
