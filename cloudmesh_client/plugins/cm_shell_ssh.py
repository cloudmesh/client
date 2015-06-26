from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_ssh import command_ssh


class cm_shell_ssh:
    def activate_cm_shell_ssh(self):
        self.register_command_topic('cloud', 'ssh')

    @command
    def do_ssh(self, args, arguments):
        """
        ::

          Usage:
              ssh list [--output=FORMAT]


          managing the sshs test test test test

          Arguments:

            KEY    the name of the ssh
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [ssh: general]
             --output=FORMAT  the output format [ssh: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_ssh()
    command.do_ssh("list")
    command.do_ssh("a=x")
    command.do_ssh("x")
