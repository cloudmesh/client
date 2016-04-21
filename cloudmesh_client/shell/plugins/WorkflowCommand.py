from __future__ import print_function
from cloudmesh_client.cloud.workflow import Workflow
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from pprint import pprint
from cloudmesh_client.common.hostlist import Parameter
from cloudmesh_client.common.dotdict import dotdict

class WorkflowCommand(PluginCommand, CloudPluginCommand):
    topics = {"workflow": "todo"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command workflow")

    # noinspection PyUnusedLocal
    @command
    def do_workflow(self, args, arguments):
        """
        ::

            Usage:
                workflow refresh [--cloud=CLOUD] [-v]
                workflow list [ID] [--cloud=CLOUD] [--format=FORMAT] [--refresh] [-v]
                workflow add NAME LOCATION
                workflow delete NAMES
                workflow status [NAMES]
                workflow show NAMES

                This lists out the workflows present for a cloud

            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name
               --refresh        refreshes the data before displaying it
                                from the cloud

            Examples:
                cm workflow refresh
                cm workflow list
                cm workflow list --format=csv
                cm workflow show 58c9552c-8d93-42c0-9dea-5f48d90a3188 --refresh

        """


        arg = dotdict(arguments)
        if arg.NAMES is not None:
            arg.names = Parameter.expand(arg.NAMES)
        else:
            arg.names = None
        pprint (arg)



        cloud = arguments["--cloud"] or Default.cloud
        if cloud is None:
            Console.error("Default cloud doesn't exist")
            return

        if arguments["-v"]:
            print("Cloud: {}".format(cloud))

        if arguments["refresh"] or Default.refresh:
            msg = "Refresh workflow for cloud {:}.".format(cloud)
            if Workflow.refresh(cloud):
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
                    result = Workflow.list(cloud, output_format)
                else:
                    result = Workflow.details(cloud, id, live, output_format)
                if counter == 0 and result is None:
                    if not Workflow.refresh(cloud):
                        msg = "Refresh workflow for cloud {:}.".format(cloud)
                        Console.error("{:} failed.".format(msg))
                counter += 1

            if result is None:
                Console.error("No workflow(s) found. Failed.")
            else:
                print(result)
            return ""

        elif arguments["show"]:
            Console.ok("I executed show")