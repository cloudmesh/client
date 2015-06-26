from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_project import command_project


class cm_shell_project:
    def activate_cm_shell_project(self):
        self.register_command_topic('cloud', 'project')

    @command
    def do_project(self, args, arguments):
        """
        ::

          Usage:
              project list [--output=FORMAT]


          managing the projects test test test test

          Arguments:

            KEY    the name of the project
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [project: general]
             --output=FORMAT  the output format [project: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_project()
    command.do_project("list")
    command.do_project("a=x")
    command.do_project("x")
