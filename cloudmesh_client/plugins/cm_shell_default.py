from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
from cloudmesh_client.cloud.command_default import command_default


class cm_shell_default:
    def activate_cm_shell_default(self):
        self.register_command_topic('cloud', 'default')

    @command
    def do_default(self, args, arguments):
        """
        ::

          Usage:
              default list [--output=FORMAT]
              default delete KEY [--cloud=CLOUD]
              default KEY [--cloud=CLOUD]
              default KEY=VALUE [--cloud=CLOUD]


          managing the defaults test test test test

          Arguments:

            KEY    the name of the default
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [default: general]
             --output=FORMAT  the output format [default: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        if arguments["list"]:
            output = arguments["--output"]
            result = command_default.list(output=output)
            print (result)
        elif arguments["delete"]:
            key = arguments["KEY"]
            command_default.delete(key, cloud)
        elif "=" in arguments["KEY"]:
            key, value = arguments["KEY"].split("=")
            command_default.set(key, value, cloud)
        elif arguments["KEY"]:
            key = arguments["KEY"]
            result = command_default.get(key, cloud)
            return result
        pass


if __name__ == '__main__':
    command = cm_shell_default()
    command.do_default("list")
    command.do_default("a=x")
    command.do_default("x")
