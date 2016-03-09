from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_stack import command_stack


class cm_shell_stack:
    def activate_cm_shell_stack(self):
        self.register_command_topic('cloud', 'stack')

    @command
    def do_stack(self, args, arguments):
        """
        ::

          Usage:
              stack list [--output=FORMAT]


          managing the stacks test test test test

          Arguments:

            KEY    the name of the stack
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [stack: general]
             --output=FORMAT  the output format [stack: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_stack()
    command.do_stack("list")
    command.do_stack("a=x")
    command.do_stack("x")
