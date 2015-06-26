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
            admin password reset
            admin version

          Options:


          Description:
            admin password reset
              Reset portal password

            admin version
               Prints the version numbers of cloudmesh and its plugins

        """
        pprint(arguments)

        if arguments['password']:
            password = arguments['password']
            reset = arguments['reset']

            print ('password reset')
        elif arguments['version']:
            print ('version')

if __name__ == '__main__':
    command = cm_shell_admin()
    command.do_admin("list")
    command.do_admin("a=x")
    command.do_admin("x")
