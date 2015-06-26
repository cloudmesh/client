from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_exp import command_exp


class cm_shell_exp:
    def activate_cm_shell_exp(self):
        self.register_command_topic('cloud', 'exp')

    @command
    def do_exp(self, args, arguments):
        """
        ::

          Usage:
              exp list [--output=FORMAT]


          managing the exps test test test test

          Arguments:

            KEY    the name of the exp
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [exp: general]
             --output=FORMAT  the output format [exp: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_exp()
    command.do_exp("list")
    command.do_exp("a=x")
    command.do_exp("x")
