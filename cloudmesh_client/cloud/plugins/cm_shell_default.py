from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
from cloudmesh_client.cloud import command_default


class cm_shell_default:
    def activate_cm_shell_default(self):
        self.register_command_topic('cloud', 'default')

    @command
    def do_default(self, args, arguments):
        """
        ::

          Usage:
              default list [--output=FORMAT]
              default KEY
              default KEY=VALUE

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
    command = cm_shell_default()
    command.do_default("list")
    command.do_default("a=x")
    command.do_default("x")
