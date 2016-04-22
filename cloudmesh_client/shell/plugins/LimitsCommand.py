from __future__ import print_function
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.limits import Limits
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand


class LimitsCommand(PluginCommand, CloudPluginCommand):
    topics = {"limits": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command limits")

    # noinspection PyUnusedLocal
    @command
    def do_limits(self, args, arguments):
        """
        ::

            Usage:
                limits list [--cloud=CLOUD] [--tenant=TENANT] [--format=FORMAT]

                Current list data with limits on a selected project/tenant.
                The --tenant option can be used by admin only

            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name
               --tenant=TENANT  the tenant name

            Examples:
                cm limits list
                cm limits list --cloud=kilo --format=csv

        """
        if arguments["list"]:
            cloud = arguments["--cloud"] or Default.cloud

            if not cloud:
                Console.error("cloud doesn't exist")
                return ""

            output_format = arguments["--format"]
            tenant = arguments["--tenant"]
            result = Limits.list(cloud,
                                 output=output_format,
                                 tenant=tenant)
            Console.msg(result)
            return ""

