from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_volume import command_volume


class cm_shell_volume:
    def activate_cm_shell_volume(self):
        self.register_command_topic('cloud', 'volume')

    @command
    def do_volume(self, args, arguments):
        """
        ::

          Usage:
              volume list [--output=FORMAT]


          managing the volumes test test test test

          Arguments:

            KEY    the name of the volume
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [volume: general]
             --output=FORMAT  the output format [volume: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_volume()
    command.do_volume("list")
    command.do_volume("a=x")
    command.do_volume("x")
