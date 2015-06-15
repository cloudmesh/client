from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
from cloudmesh_default.command_default import command_default

class cm_shell_setup:

    def activate_cm_shell_setup(self):
        self.register_command_topic('mycommands', 'setup')

    @command
    def do_setup(self, args, arguments):
        """
        ::

          Usage:
             setup username host OPENRC

          managing the defaults

          Arguments:

            KEY    the name of the default
            VALUE  the value to set the key to

          Options:

             -v       verbose mode

        """
        pprint(arguments)

        if arguments["list"]:
            output = arguments["--output"]
            command_default.list()
        elif "=" in arguments["KEY"]:
            key, value = arguments["KEY"].split("=")
            command_default.set(key, value)
        elif arguments["KEY"]:
            key = arguments["KEY"]
            command_default.get(key)
        pass

if __name__ == '__main__':
    command = cm_shell_register()
    command.do_register("list")
