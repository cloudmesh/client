from __future__ import print_function
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command, PluginCommand, \
    CloudCommand, CometCommand
from cloudmesh_client.cloud.default import Default


class DefaultCommand(PluginCommand, CloudCommand, CometCommand):
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
              default list [--cloud=CLOUD] [--format=FORMAT] [--all]
              default delete KEY [--cloud=CLOUD]
              default KEY [--cloud=CLOUD]
              default KEY=VALUE [--cloud=CLOUD]

          Arguments:

            KEY    the name of the default
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud
             --format=FORMAT  the output format [default: table]
             --all            lists all the default values

        Description:


            Cloudmesh has the ability to manage easily multiple
            clouds. One of the key concepts to make the list of such
            clouds easier is the introduction of defaults for each
            cloud or globally. Hence it is possible to set default
            images, flavors for each cloud, and also the default
            cloud. The default command is used to set and list the
            default values. These defaults are used in other commands
            if they are not overwritten by a command parameter.


        The current default values can by listed with --all option:(
        if you have a default cloud specified. You can also add a
        cloud parameter to apply the command to a specific cloud)

               default list

            A default can be set with

                default KEY=VALUE

            To look up a default value you can say

                default KEY

            A default can be deleted with

                default delete KEY


        Examples:
            default list --all
            default list --cloud=general
            default image=xyz
            default image=abc --cloud=kilo
            default image
            default image --cloud=kilo
            default delete image
            default delete image --cloud=kilo
        """
        # pprint(arguments)

        """
        For these keys, the 'cloud' column in db
        will always be 'general'.
        """
        general_keys = ["cloud", "cluster"]

        """
        If the default cloud has been set (eg. default cloud=xxx),
        then subsequent defaults for any key (eg. default image=yyy),
        will have 'cloud' column in db as the default cloud that was set.
        (eg. image=yyy for cloud=xxx).
        """

        if arguments["KEY"] in general_keys:
            cloud = "general"
        else:
            cloud = arguments["--cloud"] \
                    or Default.get("cloud", "general") \
                    or "general"

        if arguments["list"]:
            output_format = arguments["--format"]

            if arguments['--all']:
                cloud = None
            result = Default.list(cloud=cloud, format=output_format)

            if result is None:
                Console.error("No default values found")
            else:
                print(result)
            return ""

        elif arguments["delete"]:

            key = arguments["KEY"]
            result = Default.delete(key, cloud)
            if result is None:
                Console.error("Key {} not present".format(key))
            else:
                Console.ok("Deleted key {} for cloud {}. ok.".format(key,
                                                                    cloud))
            return ""

        elif "=" in arguments["KEY"]:
            key, value = arguments["KEY"].split("=")
            if key in general_keys:
                cloud = "general"
            Default.set(key, value, cloud)
            Console.ok(
                "set in defaults {}={}. ok.".format(key, value))
            return ""

        elif arguments["KEY"]:
            key = arguments["KEY"]
            result = Default.get(key, cloud)
            if result is None:
                Console.error("No default values found")
            else:
                Console.ok("Default value for {} is {}".format(key, result))
            return ""


if __name__ == '__main__':
    command = Default()
    command.do_default("list")
    command.do_default("a=x")
    command.do_default("x")
