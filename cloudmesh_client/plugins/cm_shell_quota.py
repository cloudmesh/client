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
              quota list [--output=FORMAT]


          managing the quotas test test test test

          Arguments:

            KEY    the name of the quota
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [quota: general]
             --output=FORMAT  the output format [quota: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_quota()
    command.do_quota("list")
    command.do_quota("a=x")
    command.do_quota("x")
