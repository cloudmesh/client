from __future__ import print_function
from cloudmesh_client.cloud.vc import Vc
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default


class VcCommand(PluginCommand, CloudPluginCommand):
    topics = {"vc": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command vc")

    # noinspection PyUnusedLocal
    @command
    def do_vc(self, args, arguments):
        """
        ::

            Usage:
                vc add KEYFILE NAMES
                vc key distribute NAMES
                vc key list NAMES

                This lists out the vcs present for a cloud

            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name
               --refresh        refreshes the data before displaying it
                                from the cloud

            Examples:
                cm vc refresh
                cm vc list
                cm vc list --format=csv
                cm vc show 58c9552c-8d93-42c0-9dea-5f48d90a3188 --refresh

        """

        Console.TODO("NOT IMPLEMENTED YET")
        return

        cloud = arguments["--cloud"] or Default.cloud
        if cloud is None:
            Console.error("Default cloud doesn't exist")
            return

        if arguments["-v"]:
            print("Cloud: {}".format(cloud))

        if arguments["refresh"] or Default.refresh:
            msg = "Refresh vc for cloud {:}.".format(cloud)
            if Vc.refresh(cloud):
                Console.ok("{:} ok".format(msg))
            else:
                Console.error("{:} failed".format(msg))
                return ""

        if arguments["list"]:

            id = arguments['ID']
            live = arguments['--refresh']
            output_format = arguments["--format"]

            counter = 0

            result = None
            while counter < 2:
                if id is None:
                    result = Vc.list(cloud, output_format)
                else:
                    result = Vc.details(cloud, id, live, output_format)
                if counter == 0 and result is None:
                    if not Vc.refresh(cloud):
                        msg = "Refresh vc for cloud {:}.".format(cloud)
                        Console.error("{:} failed.".format(msg))
                counter += 1

            if result is None:
                Console.error("No vc(s) found. Failed.")
            else:
                print(result)
            return ""
