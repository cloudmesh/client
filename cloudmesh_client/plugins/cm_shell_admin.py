from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_admin import command_admin


class cm_shell_admin:
    def activate_cm_shell_admin(self):
        self.register_command_topic('cloud', 'admin')

    @command
    def do_admin(self, args, arguments):
        """
        ::

          Usage:
              admin list [--output=FORMAT]


          managing the admins test test test test

          Arguments:

            KEY    the name of the admin
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [admin: general]
             --output=FORMAT  the output format [admin: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_admin()
    command.do_admin("list")
    command.do_admin("a=x")
    command.do_admin("x")
