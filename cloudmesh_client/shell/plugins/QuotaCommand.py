from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.quota import Quota
from cloudmesh_client.cloud.default import Default


class QuotaCommand(object):

    topics = {"quota": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command quota")

    @command
    def do_quota(self, args, arguments):
        """
        ::

            Usage:
                quota list [--cloud=CLOUD] [--format=FORMAT]

                Prints quota limit on a current project/tenant

            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name

            Examples:
                cm quota list
                cm quota list --cloud=india --format=csv

        """
        if arguments["list"]:
            cloud = arguments["--cloud"] or Default.get("cloud")

            if not cloud:
                Console.error("cloud doesn't exist")
                return

            output_format = arguments["--format"]
            list_quotas = Quota.list_quotas(cloud, format=output_format)
            Console.msg(list_quotas)
            return


if __name__ == '__main__':
    command = cm_shell_quota()
    command.do_quota("list")
    command.do_quota("a=x")
    command.do_quota("x")
