from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_admin import command_admin
from getpass import getpass
from cloudmesh_base.util import yn_choice, path_expand
from cloudmesh_base.ConfigDict import ConfigDict


class cm_shell_admin:
    def activate_cm_shell_admin(self):
        self.register_command_topic('cloud', 'admin')

    @command
    def do_admin(self, args, arguments):
        """
        ::

          Usage:
            admin password reset
            admin password

          Options:


          Description:
            admin password reset
              Reset portal password

        """
        pprint(arguments)

        if arguments['password'] and arguments['reset']:
            Console.ok('password reset ...')

            self.password = getpass("Password:")

            filename = path_expand("~/.cloudmesh/cmd3.yaml")
            config = ConfigDict(filename=filename)
            config["cmd3"]["properties"]["password"] = self.password
            config.write(filename=filename, output="yaml")
            Console.ok("Resetting password. ok.")

        elif arguments['password']:

            if yn_choice("Would you like to print the password?"):
                filename = path_expand("~/.cloudmesh/cmd3.yaml")
                config = ConfigDict(filename=filename)
                try:
                    self.password = config["cmd3"]["properties"]["password"]
                except Exception:
                    Console.error("could not find the password. Please set it.")
                    return
                Console.msg("Password: {:}".format(self.password))


if __name__ == '__main__':
    command = cm_shell_admin()
    command.do_admin("list")
    command.do_admin("a=x")
    command.do_admin("x")
