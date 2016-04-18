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
                group list [GROUPNAME] [--format=FORMAT]
                group remove NAMES [--group=GROUPNAME]
                group add NAMES [--type=TYPE] [--group=GROUPNAME]
                group delete GROUPS
                group copy FROM TO
                group merge GROUPA GROUPB MERGEDGROUP

            manage the groups

            Arguments:

                NAMES        names of object to be added
                GROUPS       names of a groups
                FROM         name of a group
                TO           name of a group
                GROUPA       name of a group
                GROUPB       name of a group
                MERGEDGROUP  name of a group

            Options:
                --format=FORMAT     the output format
                --type=TYPE         the resource type
                --name=NAME         the name of the group
                --id=IDS            the ID(s) to add to the group


            Description:

                Todo: design parameters that are useful and match
                description
                Todo: discuss and propose command

                cloudmesh can manage groups of resource related
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

                If finer grained deletion is needed, it can be achieved
                with the delete command that supports deletion by name

                It is also possible to remove a VM from the group using the
                remove command, by supplying the ID

            Note:

                The type is internally called for the group species, we may
                eliminate the species column and just use the type column for it,

            Example:
                default group mygroup

                group add --type=vm --id=albert-[001-003]
                    adds the vms with the given name using the Parameter
                    see base

                group add --type=vm
                 adds the last vm to the group

                group delete --name=mygroup
                    deletes all objects in the group
        """
        # pprint(arguments)


        if arguments["list"]:

            output = arguments["--format"] or Default.get(name="format", category="general") or "table"
            name = arguments["GROUPNAME"]
            if name is None:

                result = Group.list(output=output)
                if result:
                    print(result)
                else:
                    print("No groups found other than the default group but it has no members.")

            else:

                result = Group.list(name=name,
                                    output=output)

                if result:
                    print(result)
                else:
                    msg_a = ("No group found with name `{name}` found in the "
                             "category `{category}`.".format(**locals()))

                '''
                    # find alternate
                    result = Group.get(name=name)

                    msg_b = ""
                    if result is not None and len(result) < 0:
                        msg_b = " However we found such a variable in " \
                                "category `{category}`. Please consider " \
                                "using --category={category}".format(**locals())
                        Console.error(msg_a + msg_b)
                    else:
                        Console.error("No group with name {name} exists.".format(**locals()))
                '''

                return ""

        elif arguments["add"]:
            # group add NAME... [--type=TYPE] [--category=CLOUD] [--group=GROUP]

            print ("AAA", arguments["NAMES"])
            members = Parameter.expand(arguments["NAMES"])
            print ("MMMM", members)
            data = dotdict({
                "species": arguments["--type"] or "vm",
                "name": arguments["--group"] or Default.group
            })
            print ("DDD", data)
            for member in members:
                data.member = member
                pprint(data)
                Group.add(**data)

            return ""

        elif arguments["delete"]:
            groups = Parameter.expand(arguments["GROUPS"])

            for group in groups:
                result = Group.delete(group)

                if result:
                    Console.ok(result)
                else:
                    Console.error(
                        "delete group {}. failed.".format(group))
            return ""

        elif arguments["remove"]:
            members = Parameter.expand(arguments["NAMES"])

            group = arguments["--group"] or Default.group

            for member in members:
                result = Group.remove(group, member)

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
