from __future__ import print_function
from cloudmesh_client.shell.command import command


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
              group add [--name=NAME] [--type=TYPE] --id=IDs
              group list [--cloud=CLOUD] [--type=TABLE] [--name=NAME]
              group delete [--cloud=CLOUD] [--name=NAME]
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
             --type=TYPE     the resource type [default: all]
             --name=NAME      the name of the group [default: None]


        Description:

	    Todo: design parameters that are useful and match
	    description
	    Todo: discuss and propose command
	    
            cloudmesh can manage groups of resources and cloud related
            objects. As it woudl be combersome to for example delete
            many virtual machines or delete VMs that are in the same
            group, but are running in different clouds.

	    Hence it is possible to add a virtual machine to a
	    specific group. The group name to be added to can be set
	    as a default. This way all suubsequent commands use this
	    default group. It can also be set via a command parameter.
	    Another convenience function is that the group command can
	    use the last used virtual machine. If a vm is started it
	    will be automatically added to the deafult group if it is set.

	    The delete command has an optional cloud parameter so that
	    deletion of vms of a partial group by cloud can be
	    achieved.

	    If finer grained deletion is needed, it can be acheved
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
        # TODO: do something useful here
        if arguments["list"]:
            name = arguments["--name"]
            type = arguments["--type"]
            cloud = arguments["--cloud"]
            print ("[Command To be Implemented] set group, name: " + name +
                   ", type: " + type +
                   ", cloud: " + cloud)
            return

        # TODO: do something useful here
        elif arguments["info"]:
            output_format = arguments["--output"]
            print ("[Command To be Implemented] group, format: " + output_format)
            return

        # TODO: do something useful here
        elif arguments["add"]:
            name = arguments["--name"]
            type = arguments["--type"]
            id = arguments["--id"]
            print ("[Command To be Implemented] add to group, name: " + name +
                   ", type: " + type +
                   ", id: " + id)
            return

        # TODO: do something useful here
        elif arguments["delete"]:
            name = arguments["--name"]
            cloud = arguments["--cloud"]
            print ("[Command To be Implemented] deleted group, name: " + name +
                   ", cloud: " + cloud)
            return

        # TODO: do something useful here
        elif arguments["copy"]:
            _from = arguments["FROM"]
            _to = arguments["TO"]
            print ("[Command To be Implemented] copy FROM group: " + _from +
                   ", TO group: " + _to)
            return

        # TODO: do something useful here
        elif arguments["merge"]:
            _groupA = arguments ["GROUPA"]
            _groupB = arguments ["GROUPB"]
            _mergedGroup = arguments ["MERGEDGROUP"]
            print ("[Command To be Implemented] merge, group: " + _groupA +
                   ", & group: " + _groupB +
                   ", to group: " + _mergedGroup)
            return

if __name__ == '__main__':
    # TODO: do something useful here
    command = GroupCommand()
    command.do_group("list")
