from __future__ import print_function

from cloudmesh_client.cloud.group import Group
from cloudmesh_client.cloud.default import Default
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.shell.command import PluginCommand, CloudCommand


class GroupCommand(PluginCommand, CloudCommand):
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
                group add NAME [--type=TYPE] [--cloud=CLOUD] [--id=IDs]
                group list [--cloud=CLOUD] [--format=FORMAT] [NAME]
                group delete NAME [--cloud=CLOUD]
                group remove [--cloud=CLOUD] --name=NAME --id=ID
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

        if arguments["list"]:

            output = arguments["--format"] or Default.get("format") or "table"
            cloud = arguments["--cloud"] or Default.get_cloud()
            name = arguments["NAME"]

            if name is None:

                result = Group.list(format=output, cloud=cloud)
                if result:
                    print(result)
                else:
                    print("There are no groups in the cloudmesh database!")

            else:

                result = Group.get_info(name=name, cloud=cloud, output=output)

                if result:
                    print(result)
                else:
                    msg_a = ("No group found with name `{name}` found in the "
                             "cloud `{cloud}`.".format(**locals()))

                    # find alternate
                    result = Group.get(name=name)
                    msg_b = ""
                    if result is not None:
                        msg_b = " However we found such a variable in " \
                                "cloud `{cloud}`. Please consider " \
                                "using --cloud={cloud}".format(**result)
                        Console.error(msg_a + msg_b)

                return

        elif arguments["add"]:
            data = {
                "name": arguments["NAME"],
                "type": arguments["--type"] or Default.get("type"),
                "cloud": arguments["--cloud"] or Default.get("cloud"),
                "id": arguments["--id"] or Default.get("id") or "vm"
            }

            Group.add(**data)
            return

        elif arguments["delete"]:
            data = {
                "name": arguments["NAME"],
                "cloud": arguments["--cloud"] or Default.get("cloud"),
            }

            result = Group.delete(**data)
            if result:
                Console.ok("Deletion completed. ok.")
            else:
                Console.error(
                    "No group with name `{name}` found".format(**data))
            return

        elif arguments["remove"]:
            name = arguments["--name"]
            id = arguments["--id"]
            cloud = arguments["--cloud"] or \
                    Default.get("cloud")

            if not cloud:
                Console.error("Default cloud not set!")
                return

            result = Group.remove(name, id, cloud)
            if result:
                Console.ok(result)
            else:
                Console.error(
                    "Failed to delete ID [{}] from group [{}] in the database!".format(
                        id, name))
            return

        elif arguments["copy"]:
            _from = arguments["FROM"]
            _to = arguments["TO"]

            Group.copy(_from, _to)
            return

        elif arguments["merge"]:
            _groupA = arguments["GROUPA"]
            _groupB = arguments["GROUPB"]
            _mergedGroup = arguments["MERGEDGROUP"]

            Group.merge(_groupA, _groupB, _mergedGroup)
            return


if __name__ == '__main__':
    # TODO: do something useful here
    command = GroupCommand()
    command.do_group("list")
