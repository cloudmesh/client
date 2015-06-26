from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_limits import command_limits


class cm_shell_limits:
    def activate_cm_shell_limits(self):
        self.register_command_topic('cloud', 'limits')

    @command
    def do_limits(self, args, arguments):
        """
        ::

          Usage:
              limits list [--output=FORMAT]


          managing the limitss test test test test

          Arguments:

            KEY    the name of the limits
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [limits: general]
             --output=FORMAT  the output format [limits: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_limits()
    command.do_limits("list")
    command.do_limits("a=x")
    command.do_limits("x")
