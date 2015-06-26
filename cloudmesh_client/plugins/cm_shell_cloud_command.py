from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_cloud import command_cloud


class cm_shell_cloud:
    def activate_cm_shell_cloud_command(self):
        self.register_command_topic('cloud', 'cloud')

    @command
    def do_cloud(self, args, arguments):
        """
        ::

          Usage:
               list [--output=FORMAT]


          managing the clouds test test test test

          Arguments:

            KEY    the name of the cloud
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [cloud: general]
             --output=FORMAT  the output format [cloud: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_cloud()
    command.do_cloud("list")
    command.do_cloud("a=x")
    command.do_cloud("x")
