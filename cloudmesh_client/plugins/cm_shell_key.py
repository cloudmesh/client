from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_key import command_key


class cm_shell_key:
    def activate_cm_shell_key(self):
        self.register_command_topic('cloud', 'key')

    @command
    def do_key(self, args, arguments):
        """
        ::

          Usage:
              key list [--output=FORMAT]


          managing the keys test test test test

          Arguments:

                the name of the key
            VALUE  the value to set the  to

          Options:

             --cloud=CLOUD    the name of the cloud [key: general]
             --output=FORMAT  the output format [key: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_key()
    command.do_key("list")
    command.do_key("a=x")
    command.do_key("x")
