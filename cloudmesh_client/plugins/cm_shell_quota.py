from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_quota import command_quota


class cm_shell_quota:
    def activate_cm_shell_quota(self):
        self.register_command_topic('cloud', 'quota')

    @command
    def do_quota(self, args, arguments):
        """
        ::

            Usage:
                quota [CLOUD...] [--format=FORMAT]

            print quota limit on a current project/tenant

            Arguments:

              CLOUD          Cloud name

            Options:

               -v       verbose mode

        """
        # pprint(arguments)
        clouds = arguments["CLOUD"]
        output_format = arguments["--format"]
        Console.ok('quota {} {}'.format(clouds,output_format))
        pass


if __name__ == '__main__':
    command = cm_shell_quota()
    command.do_quota("list")
    command.do_quota("a=x")
    command.do_quota("x")
