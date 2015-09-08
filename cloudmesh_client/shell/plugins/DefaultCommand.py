from __future__ import print_function
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command
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

        Description:

            Cloudmesh has the ability to manage teasily multiple
            clouds. One of the key oncepts to make the usage of such
            clouds easier is the introduction of defaults for each
            cloud or globally. Hence it is possible to set default
            images, flavors for each cloud, but also the defauld
            cloud. The default command is used to set and list the
            default values. These defaults are used in other commands
            if they are not overwritten by a command parameter.

	    The current default values can by listed with:(if you have
	    a default cloud specified. You can also add a
	    --cloud=CLOUD parameter to apply the command to a specific
	    cloud) 

	    	default list

            A deafult can be set with

                 default KEY=VALUE

             To look up a default value you can say

                  default KEY

               A deafult can be deleted with

                   default delete KEY

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
