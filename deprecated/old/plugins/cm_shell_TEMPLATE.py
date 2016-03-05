from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_TEMPLATE import command_TEMPLATE


class cm_shell_TEMPLATE:
    def activate_cm_shell_TEMPLATE(self):
        self.register_command_topic('cloud', 'TEMPLATE')

    @command
    def do_TEMPLATE(self, args, arguments):
        """
        ::

          Usage:
              TEMPLATE list [--output=FORMAT]


          managing the TEMPLATEs test test test test

          Arguments:

            KEY    the name of the TEMPLATE
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [TEMPLATE: general]
             --output=FORMAT  the output format [TEMPLATE: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_TEMPLATE()
    command.do_TEMPLATE("list")
    command.do_TEMPLATE("a=x")
    command.do_TEMPLATE("x")
