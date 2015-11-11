from __future__ import print_function
from cloudmesh_client.cloud.flavor import Flavor
from cloudmesh_client.shell.command import command, PluginCommand, CloudCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.default import Default


class FlavorCommand(PluginCommand, CloudCommand):
    topics = {"flavor": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command flavor")

    @command
    def do_flavor(self, args, arguments):
        """
        ::

            Usage:
                flavor refresh [--cloud=CLOUD]
                flavor list [ID] [--cloud=CLOUD] [--format=FORMAT] [--refresh]

                This lists out the flavors present for a cloud

            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name
               --refresh        refreshes the data before displaying it
                                from the cloud

            Examples:
                cm flavor refresh
                cm flavor list
                cm flavor list --format=csv
                cm flavor show 58c9552c-8d93-42c0-9dea-5f48d90a3188 --refresh

        """
        try:
            cloud = arguments["--cloud"] or Default.get_cloud()
        except:
            Console.error("xxx Default cloud doesn't exist")

        if arguments["refresh"]:

            if cloud is None:
                Console.error("Default cloud doesn't exist")
                return

            msg = "Refresh flavor for cloud {:}.".format(cloud)
            if Flavor.refresh(cloud):
                Console.ok("{:} ok".format(msg))
            else:
                Console.error("{:} failed".format(msg))
            return ""

        if arguments["list"]:

            id = arguments['ID']
            output_format = arguments["--format"]
            live = arguments['--refresh']

            output_format = arguments["--format"]
            if id is None:
                result = Flavor.list(cloud, output_format)
            else:
                result = Flavor.details(cloud, id, live, output_format)

            if result is None:
                #
                # outo refresh
                #
                Console.error("No flavor(s) found.")
                # Flavor.refresh(cloud)
                # Console.ok("Refreshing flavor(s). ok.")

            else:

                print(result)
            return ""
