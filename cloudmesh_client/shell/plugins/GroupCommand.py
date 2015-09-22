from __future__ import print_function

from cloudmesh_client.cloud.group import Group
from cloudmesh_client.cloud.default import Default
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console

class GroupCommand(object):

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
                group info [--cloud=CLOUD] [--format=FORMAT] NAME
                group add [--name=NAME] [--type=TYPE] [--cloud=CLOUD] --id=IDs
                group list [--cloud=CLOUD] [--format=FORMAT]
                group delete [--cloud=CLOUD] [--name=NAME]
                group copy FROM TO
                group merge GROUPA GROUPB MERGEDGROUP

            manage the groups

            Arguments:

                NAME         name of a group
                FROM         name of a group
                TO           name of a group
                GROUPA       name of a group
                GROUPB       name of a group
                MERGEDGROUP  name of a group

            Options:
                --cloud=CLOUD    the name of the cloud
                --format=FORMAT  the output format
                --type=TYPE     the resource type
                --name=NAME      the name of the group


            Description:

                Todo: design parameters that are useful and match
                description
                Todo: discuss and propose command

                cloudmesh can manage groups of resources and cloud related
                objects. As it would be cumbersome to for example delete
                many virtual machines or delete VMs that are in the same
                group, but are running in different clouds.

                Hence it is possible to add a virtual machine to a
                specific group. The group name to be added to can be set
                as a default. This way all subsequent commands use this
                default group. It can also be set via a command parameter.
                Another convenience function is that the group command can
                use the last used virtual machine. If a vm is started it
                will be automatically added to the default group if it is set.

                The delete command has an optional cloud parameter so that
                deletion of vms of a partial group by cloud can be
                achieved.

                If finer grained deletion is needed, it can be achieved
                with the delete command that supports deletion by name

            Example:
                default group mygroup

                group add --type=vm --id=gregor-[001-003]
                    adds the vms with teh given name using the Parameter
                    see base

                group add --type=vm
                 adds the last vm to the group

                group delete --name=mygroup
                    deletes all objects in the group
        """
        # pprint(arguments)

        if arguments["list"]:
            #name = arguments["NAME"]
            output_format = arguments["--format"]
            cloud = arguments["--cloud"]

            #If cloud is not specified, get default
            if not cloud:
                cloud = Default.get("cloud") or "general"

            #If format is not specified, get default
            if not output_format:
                output_format = Default.get("format") or "table"

            result = Group.list(format=output_format, cloud=cloud)
            if result:
                print(result)
            else:
                print("There are no groups in the cloudmesh database!")

            return

        elif arguments["info"]:
            output_format = arguments["--format"]
            cloud = arguments["--cloud"]
            name = arguments["NAME"]

            #If format is not specified, get default
            if not output_format:
                output_format = Default.get("format") or "table"

            # Get default cloud
            if not cloud:
                cloud = Default.get("cloud") or "general"

            result = Group.get_info(cloud=cloud, name=name, format=output_format)

            if result:
                print(result)
            else:
                Console.error("No group with name {} found in the cloudmesh database!".format(name))
            return

        # TODO: add logic to check VM exists in cloud
        elif arguments["add"]:
            name = arguments["--name"]
            type = arguments["--type"]
            cloud = arguments["--cloud"]
            id = arguments["--id"]

            # If type is not specified, get default
            if not type:
                type = Default.get("type")

            # If id is not specified, get last created vm id
            if not id:
                id = Default.get("id")

            # If cloud is not specified, get last created vm id
            if not cloud:
                cloud = Default.get("cloud") or "general"

            Group.add(name=name, type=type, id=id, cloud=cloud)
            return

        # TODO: add logic to delete VM(s) in cloud
        elif arguments["delete"]:
            name = arguments["--name"]
            cloud = arguments["--cloud"]

            #If cloud is not specified, get default
            if not cloud:
                cloud = Default.get("cloud") or "general"

            result = Group.delete(name=name, cloud=cloud)
            if result:
                Console.ok("Deletion Successful!")
            else:
                Console.error("No group with name [{}] in the database!".format(name))
            return

        elif arguments["copy"]:
            _from = arguments["FROM"]
            _to = arguments["TO"]

            Group.copy(_from, _to)
            return

        elif arguments["merge"]:
            _groupA = arguments ["GROUPA"]
            _groupB = arguments ["GROUPB"]
            _mergedGroup = arguments ["MERGEDGROUP"]

            Group.merge(_groupA, _groupB, _mergedGroup)
            return

if __name__ == '__main__':
    # TODO: do something useful here
    command = GroupCommand()
    command.do_group("list")
