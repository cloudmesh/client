from __future__ import print_function
from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console


class CloudCommand(object):

    topics = {"cloud": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command cloud")

    @command
    def do_cloud(self, args, arguments):
        """
        ::

          Usage:
              cloud list [--output=FORMAT]


          managing the admins test test test test

          Arguments:

            KEY    the name of the admin
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [cloud: general]
             --output=FORMAT  the output format [cloud: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        Console.ok("cloud command called")
        pass


if __name__ == '__main__':
    command = CloudCommand()
    command.do_cloud("list")
