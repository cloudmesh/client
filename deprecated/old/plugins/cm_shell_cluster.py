from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_cluster import command_cluster


class cm_shell_cluster:
    def activate_cm_shell_cluster(self):
        self.register_command_topic('cloud', 'cluster')

    @command
    def do_cluster(self, args, arguments):
        """
        ::

          Usage:
              cluster list [--output=FORMAT]


          managing the clusters test test test test

          Arguments:

            KEY    the name of the cluster
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [cluster: general]
             --output=FORMAT  the output format [cluster: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_cluster()
    command.do_cluster("list")
    command.do_cluster("a=x")
    command.do_cluster("x")
