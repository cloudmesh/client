from __future__ import print_function
from cloudmesh_client.cloud.workflow import Workflow
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from pprint import pprint
from cloudmesh_client.common.hostlist import Parameter
from cloudmesh_client.common.dotdict import dotdict
# from cloudmesh_client.cloud.workflowexec import *

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
                workflow list [ID] [NAME] [--cloud=CLOUD] [--format=FORMAT] [--refresh] [-v]
                workflow add NAME LOCATION
                workflow delete ID
                workflow status [NAMES]
                workflow show ID
                workflow save NAME WORKFLOWSTR
                workflow run NAME
                workflow service start
                workflow service stop
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
                cm workflow run workflow1

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

            result = None
            if id is None:
                result = Workflow.list(cloud, output_format)
            else:
                result = Workflow.details(cloud, id, live, output_format)

            if result is None:
                Console.error("No workflow(s) found. Failed.")
            else:
                print(result)
            return ""

        elif arguments["show"]:
            workflow_id = arguments["ID"]
            Console.ok("I executed show")
            # Console.msg(workflow_id)
            if workflow_id is None:
                Console.msg("Please enter a Workflow Id to execute workflow")
            else:
                result = Workflow.run(cloud,workflow_id)
                # print (result)
                if result is None:
                    Console.msg("Use workflow list to view existing workflows or do workflow save to save a new one")
                else:
                    # Console.msg(result)
                    # Console.msg(result[0])
                    Console.msg(result[0]['workflow_str'])
                    # entry_point(result[0]['workflow_str'])
                    Console.msg("All Set to execute")

        elif arguments["save"]:
            workflow_name = arguments["NAME"]
            workflow_str = arguments["WORKFLOWSTR"]

            result = Workflow.save(cloud=cloud,
                                   name=workflow_name,
                                   str=workflow_str)
            if result is not None:
                Console.ok(result)
            else:
                Console.error("Failed to save workflow!")
        elif arguments["run"]:
            Console.msg("Execute Run")
            workflow_name = arguments["NAME"]
            # cm_id = arguments["ID"]

            result = Workflow.run(cloud,name=workflow_name)

        elif arguments["delete"]:
            workflow_id = arguments["ID"]

            result = Workflow.delete(cloud,workflow_id)
            if result is not None:
                Console.msg(result)
            else:
                Console.error("Failed to save workflow!")
        elif arguments["service"] and arguments["start"]:
            # Console.msg()
            # mkdir -pf ~/.cloudmesh/workflow
            pass