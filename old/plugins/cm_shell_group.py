from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_exp import command_exp


class cm_shell_group:
    def activate_cm_shell_group(self):
        self.register_command_topic('cloud', 'group')

    @command
    def do_group(self, args, arguments):
        """
        ::

          Usage:
              group list [--output=FORMAT]
              group set NAME


          managing the exps test test test test

          Arguments:

            KEY    the name of the exp
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [exp: general]
             --output=FORMAT  the output format [exp: table]

        """
        # pprint(arguments)
        if arguments["set"]:
            name = arguments["NAME"]
            print ("set group" + name)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_exp()
    command.do_exp("list")
    command.do_exp("a=x")
    command.do_exp("x")
