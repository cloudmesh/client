from __future__ import print_function

from cloudmesh_client.cloud.group import Group
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint
from cloudmesh_client.common.hostlist import Parameter

class GroupCommand(PluginCommand, CloudPluginCommand):
    topics = {"group": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command group")

    @command
    def do_group(self, args, arguments):
        """
        ::

            Usage:
                group list [--category=CLOUD] [--format=FORMAT] [GROUPNAME]
                group remove NAME... [--category=CLOUD] --group=GROUPNAME
                group add NAME... [--type=TYPE] [--category=CLOUD] [--group=GROUPNAME]
                group delete GROUP... [--category=CLOUD]
                group copy FROM TO
                group merge GROUPA GROUPB MERGEDGROUP

            manage the groups

            Arguments:

                NAME         name of object to be added
                GROUP        name of a group
                FROM         name of a group
                TO           name of a group
                GROUPA       name of a group
                GROUPB       name of a group
                MERGEDGROUP  name of a group

            Options:
                --category=CLOUD       the name of the category
                --format=FORMAT     the output format
                --type=TYPE         the resource type
                --name=NAME         the name of the group
                --id=IDS            the ID(s) to add to the group


            Description:

                Todo: design parameters that are useful and match
                description
                Todo: discuss and propose command

                cloudmesh can manage groups of resources and category related
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

                The delete command has an optional category parameter so that
                deletion of vms of a partial group by cloud can be
                achieved.

                If finer grained deletion is needed, it can be achieved
                with the delete command that supports deletion by name

                It is also possible to remove a VM from the group using the
                remove command, by supplying the ID

            Example:
                default group mygroup

                group add --type=vm --id=albert-[001-003]
                    adds the vms with teh given name using the Parameter
                    see base

                group add --type=vm
                 adds the last vm to the group

                group delete --name=mygroup
                    deletes all objects in the group
        """
        # pprint(arguments)

        category = arguments["--category"] or Default.get_cloud()

        if arguments["list"]:

            output = arguments["--format"] or Default.get("format", category) or "table"
            name = arguments["GROUPNAME"]

            if name is None:

                result = Group.list(format=output, category=category)
                if result:
                    print(result)
                else:
                    print("No groups found other than the default group but it has no members.")

            else:

                result = Group.get_info(name=name,
                                        category=category,
                                        output=output)

                if result:
                    print(result)
                else:
                    msg_a = ("No group found with name `{name}` found in the "
                             "category `{category}`.".format(**locals()))

                    # find alternate
                    result = Group.get(name=name)
                    msg_b = ""
                    if result is not None:
                        msg_b = " However we found such a variable in " \
                                "category `{category}`. Please consider " \
                                "using --category={category}".format(**result)
                        Console.error(msg_a + msg_b)

                return ""

        elif arguments["add"]:
            # group add NAME... [--type=TYPE] [--category=CLOUD] [--group=GROUP]


            members = Parameter.expand(arguments["NAME"])
            data = dotdict({
                "type": arguments["--type"] or "vm",
                "category": category,
                "name": arguments["--group"] or Default.get_group()
            })
            for member in members:
                data.member = member
                Group.add(**data)

            return ""

        elif arguments["delete"]:
            groups = Parameter.expand(arguments["GROUP"])

            for group in groups:
                result = Group.delete(group, category)

                if result:
                    Console.ok(result)
                else:
                    Console.error(
                        "delete group {}. failed.".format(group))
            return ""


        elif arguments["remove"]:
            members = Parameter.expand(arguments["NAME"])

            group = arguments["--group"] or Default.get_group()

            for member in members:
                result = Group.remove(group, member, category)

                if result:
                    Console.ok(result)
                else:
                    Console.error(
                        "remove {} from group {}. failed.".format(group, member))
            return ""

        elif arguments["copy"]:
            _from = arguments["FROM"]
            _to = arguments["TO"]

            Group.copy(_from, _to)
            return ""

        elif arguments["merge"]:
            _groupA = arguments["GROUPA"]
            _groupB = arguments["GROUPB"]
            _mergedGroup = arguments["MERGEDGROUP"]

            Group.merge(_groupA, _groupB, _mergedGroup)
            return ""


