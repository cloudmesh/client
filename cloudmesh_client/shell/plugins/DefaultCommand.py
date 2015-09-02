from __future__ import print_function
import os
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.cm import command
from pprint import pprint
from cloudmesh_client.cloud.default import Default


class DefaultCommand(object):

    topics = {"default": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command default")

    @command
    def do_default(self, args, arguments):
        """
        ::

          Usage:
              default list [--format=FORMAT]
              default delete KEY [--cloud=CLOUD]
              default KEY [--cloud=CLOUD]
              default KEY=VALUE [--cloud=CLOUD]


          managing the defaults test test test test

          Arguments:

            KEY    the name of the default
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [default: general]
             --format=FORMAT  the output format [default: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        if arguments["list"]:

            output_format = arguments["--format"]
            result = Default.list(format=output_format)
            if result is None:
                Console.error("No default values found")
                return
            else:
                print (result)

        elif arguments["delete"]:
            key = arguments["KEY"]
            Default.delete(key, cloud)
        elif "=" in arguments["KEY"]:
            key, value = arguments["KEY"].split("=")
            Default.set(key, value, cloud)
        elif arguments["KEY"]:

            key = arguments["KEY"]
            result = Default.get(key, cloud)

            if result is None:
                Console.error("No default values found")
                return
            else:
                print (result)

        pass


if __name__ == '__main__':
    command = Default()
    command.do_default("list")
    command.do_default("a=x")
    command.do_default("x")
