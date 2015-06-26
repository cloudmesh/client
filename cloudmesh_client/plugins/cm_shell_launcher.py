from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_launcher import command_launcher


class cm_shell_launcher:
    def activate_cm_shell_launcher(self):
        self.register_command_topic('cloud', 'launcher')

    @command
    def do_launcher(self, args, arguments):
        """
        ::

          Usage:
              launcher list [--output=FORMAT]


          managing the launchers test test test test

          Arguments:

            KEY    the name of the launcher
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [launcher: general]
             --output=FORMAT  the output format [launcher: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_launcher()
    command.do_launcher("list")
    command.do_launcher("a=x")
    command.do_launcher("x")
