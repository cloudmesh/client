from __future__ import print_function
import os
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.cm import command
from pprint import pprint
# from cloudmesh_client.cloud.command_exp import command_exp


class GroupCommand:

    topics = {"group": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command key")

    @command
    def do_group(self, args, arguments):
        """
        ::

          Usage:
              group info [--output=FORMAT]
              group add [--name=NAME] --id=IDs
              group add [--cloud=CLOUD] [--type=TABLE] --name=NAME
              group list [--cloud=CLOUD] [--type=TABLE] [--name=NAME]
              group delete [--cloud=CLOUD] [--type=TABLE] [--name=NAME]
              group copy FROM TO
              group merge GROUPA GROUPB MERGEDGROUP

          manage the groups

          Arguments:

            FROM    name of a group
            TO      name of a group
            GROUPA  name of a group
            GROUPB  name of a group
            GROUPC  name of a group

          Options:

             --cloud=CLOUD    the name of the cloud [default: general]
             --output=FORMAT  the output format [default: table]
             --type=TABLE     the table type [default: all]
             --name=NAME      the name of the group [default: None]

        Example:
            default group mygroup
            group add --type=vm --id=gregor-[001-003]
                # adds the vms with teh given name using the Parameter see base
            group delete --name=mygroup
                # deletes all objects in the group
        """
        # pprint(arguments)
        # TODO: do something useful here
        if arguments["list"]:
            name = arguments["NAME"]
            print ("set group" + name)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    # TODO: do something useful here
    command = GroupCommand()
    command.do_group("list")
    command.do_group("a=x")
    command.do_group("x")
