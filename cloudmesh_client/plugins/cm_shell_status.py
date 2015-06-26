from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_status import command_status


class cm_shell_status:
    def activate_cm_shell_status(self):
        self.register_command_topic('cloud', 'status')

    @command
    def do_status(self, args, arguments):
        """
        ::

          Usage:
              status list [--output=FORMAT]


          managing the statuss test test test test

          Arguments:

            KEY    the name of the status
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [status: general]
             --output=FORMAT  the output format [status: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_status()
    command.do_status("list")
    command.do_status("a=x")
    command.do_status("x")
