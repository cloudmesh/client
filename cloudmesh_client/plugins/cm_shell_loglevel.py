from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_loglevel import command_loglevel


class cm_shell_loglevel:
    def activate_cm_shell_loglevel(self):
        self.register_command_topic('cloud', 'loglevel')

    @command
    def do_loglevel(self, args, arguments):
        """
        ::

          Usage:
              loglevel list [--output=FORMAT]


          managing the loglevels test test test test

          Arguments:

            KEY    the name of the loglevel
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [loglevel: general]
             --output=FORMAT  the output format [loglevel: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_loglevel()
    command.do_loglevel("list")
    command.do_loglevel("a=x")
    command.do_loglevel("x")
