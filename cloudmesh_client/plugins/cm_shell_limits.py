from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_limits import command_limits


class cm_shell_limits:
    def activate_cm_shell_limits(self):
        self.register_command_topic('cloud', 'limits')

    @command
    def do_limits(self, args, arguments):
        """
        ::

            Usage:
                limits [CLOUD...] [--format=FORMAT]

            Current usage data with limits on a selected project/tenant

            Arguments:

              CLOUD          Cloud name to see the usage

            Options:

               -v       verbose mode

        """
        # pprint(arguments)
        clouds = arguments["CLOUD"]
        output_format = arguments["--format"]
        Console.ok('limits {} {}'.format(clouds, output_format))
        pass


if __name__ == '__main__':
    command = cm_shell_limits()
    command.do_limits("list")
    command.do_limits("a=x")
    command.do_limits("x")
