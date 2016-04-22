from __future__ import print_function
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.usage import Usage
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand


class UsageCommand(PluginCommand, CloudPluginCommand):
    topics = {"usage": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command list")

    # noinspection PyUnusedLocal
    @command
    def do_usage(self, args, arguments):
        """
        ::

            Usage:
                usage list [--cloud=CLOUD] [--start=START] [--end=END] [--tenant=TENANT] [--format=FORMAT]

                Show usage data.

            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name
               --tenant=TENANT  the tenant name
               --start=START    Usage range start date ex 2012-01-20, default is: 4 weeks ago
               --end=END        Usage range end date, ex 2012-01-20, default is: tomorrow


            Examples:
                cm usage list

        """

        if arguments["list"]:
            cloud = arguments["--cloud"] or Default.get(name="cloud")

            if not cloud:
                Console.error("cloud doesn't exist")
                return ""
            output_format = arguments["--format"]
            start = arguments["--start"]
            end = arguments["--end"]
            tenant = arguments["--tenant"]
            usage = Usage.list(cloud,
                               start=start,
                               end=end,
                               tenant=tenant,
                               format=output_format)
            Console.msg(usage)
            return ""
