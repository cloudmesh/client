from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command, PluginCommand, \
    CloudPluginCommand, CometPluginCommand
from cloudmesh_client.default import Default
from cloudmesh_client.common.LogUtil import LogUtil

logger = LogUtil.get_logger()


class DefaultCommand(PluginCommand, CloudPluginCommand, CometPluginCommand):
    topics = {"default": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command default")

    # noinspection PyUnusedLocal
    @command
    def do_default(self, args, arguments):
        """
        ::

          Usage:
              default
              default list [--cloud=CLOUD] [--format=FORMAT] [--all]
              default delete KEY [--cloud=CLOUD]
              default KEY [--cloud=CLOUD]
              default KEY=VALUE [--cloud=CLOUD]

          Arguments:
            KEY    the name of the default
            VALUE  the value to set the key to

          Options:
             --cloud=CLOUD    the name of the cloud
             --format=FORMAT  the output format. Values include
                              table, json, csv, yaml.
             --all            lists all the default values

        Description:
            Cloudmesh has the ability to manage easily multiple
            clouds. One of the key concepts to manage multiple clouds
            is to use defaults for the cloud, the images, flavors,
            and other values. The default command is used to manage
            such default values. These defaults are used in other commands
            if they are not overwritten by a command parameter.

            The current default values can by listed with

                default list --all

            Via the default command you can list, set, get and delete
            default values. You can list the defaults with

               default list

            A default can be set with

                default KEY=VALUE

            To look up a default value you can say

                default KEY

            A default can be deleted with

                default delete KEY

            To be specific to a cloud you can specify the name of the
            cloud with the --cloud=CLOUD option. The list command can
            print the information in various formats iv specified.

        Examples:
            default
                lists the default for the current default cloud

            default list --all
                lists all default values

            default list --cloud=kilo
                lists the defaults for the cloud with the name kilo

            default image=xyz
                sets the default image for the default cloud to xyz

            default image=abc --cloud=kilo
                sets the default image for the cloud kilo to xyz

            default image
                list the default image of the default cloud

            default image --cloud=kilo
                list the default image of the cloud kilo

            default delete image
                deletes the value for the default image in the
                default cloud

            default delete image --cloud=kilo
                deletes the value for the default image in the
                cloud kilo

        """
        # pprint(arguments)

        """
        For these keys, the 'cloud' column in db
        will always be 'general'.
        """
        general_keys = ["cloud", "cluster", "queue", "key", "group", "user", "secgroup", "vm",
                        "refresh", "debug", "interactive", "purge"]

        """
        If the default cloud has been set (eg. default category=xxx),
        then subsequent defaults for any key (eg. default image=yyy),
        will have 'cloud' column in db as the default cloud that was set.
        (eg. image=yyy for category=xxx).
        """

        if arguments["KEY"] in general_keys:
            cloud = "general"
        elif args == '':
            cloud = "general"
            arguments["--cloud"] = cloud
            arguments["list"] = True
            order = ['name', 'value']
            output_format = arguments["--format"]
            result = Default.list(category=cloud,
                                  order=order,
                                  output=output_format)
            print(result)
            return ""

        else:
            cloud = arguments["--cloud"] or Default.get(name="cloud", category="general") or "general"

        if arguments["list"]:
            output_format = arguments["--format"] or Default.output or 'table'

            if arguments['--all'] or arguments["--cloud"] is None:
                cloud = None
            result = Default.list(category=cloud, output=output_format)

            if result is None:
                Console.error("No default values found")
            else:
                print(result)
            return ""

        elif arguments["delete"]:

            key = arguments["KEY"]
            if key in general_keys:
                cloud = "general"
            result = Default.delete(key, cloud)
            if not result :
                Console.error("default {} not present".format(key))
            else:
                Console.ok("Deleted key {} for cloud {}. ok.".format(key,
                                                                     cloud))
            return ""

        elif "=" in arguments["KEY"]:
            key, value = arguments["KEY"].split("=")
            if key in general_keys:
                cloud = "general"
            if key in "debug":
                Default.set_debug(value)
            else:
                Default.set(key, value, category=cloud)
            Console.ok(
                "set default {}={}. ok.".format(key, value))
            return ""

        elif arguments["KEY"]:
            key = arguments["KEY"]
            if key in general_keys:
                cloud = "general"
            result = Default.get(name=key, category=cloud)
            if result is None:
                Console.error("No default values found")
            else:
                Console.ok("{}".format(result))
            return ""
