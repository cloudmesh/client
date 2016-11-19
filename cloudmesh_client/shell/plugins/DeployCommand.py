
import os.path

from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.default import Default
from cloudmesh_client.deployer.ansible.role import AnsibleRole
from cloudmesh_client.shell.command import (CloudPluginCommand, PluginCommand,
    command)
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.plugins.ClusterCommand2 import (
    Command as ClusterCommand)


class AnsibleCommand(object):

    def playbook(self, cluster=None, path=None):
        Console.debug_msg('NotImplementedError')


    def role(self, cluster=None, path=None, user=None):
        """Deploy a role to all the nodes in the cluster

        :param str cluster: cluster name (default is the active cluster)
        :param str path: path to the role (default is current working directory)
        :param str name: name of the role

        """

        cluster = cluster or Default.active_cluster

        inventory = ClusterCommand().inventory(cluster=cluster, format='ansible').ini()
        role = AnsibleRole(path)
        role.run(inventory, user=user)



class DeployCommand(PluginCommand, CloudPluginCommand):
    topics = {'deploy': 'cluster'}

    def __init__(self, context):
        Console.debug_msg("init command deploy")

    @command
    def do_deploy(self, args, arguments):
        """
        ::
            Usage:
              deploy ansible [-p PATH...] [-u NAME] [CLUSTER]

            Commands:

              ansible                        Ansible deployment

            Ansible Commands:
              playbook                       Deploy a pre-prepared playbook
              role                           Deploy a role to all nodes

            Arguments:

              CLUSTER                        Cluster name to deploy to
              NAME                           Alphanumeric name
              COUNT                          Integer > 0
              PATH                           Path to entry on the filesystem

            Options:

              -p --path=PATH                 Path to the location of the item
              -u --user=NAME                 Username of the nodes to manage

        """

        arguments = dotdict(arguments)
        from pprint import pprint
        pprint(arguments)

        if arguments.ansible:
            ansible = AnsibleCommand()
            for path in arguments['--path']:

                # playbook
                if os.path.isfile(path):
                    ansible.playbook(
                        cluster = arguments.CLUSTER,
                        path = path,
                        user = arguments['--user'],
                    )

                # role
                elif os.path.isdir(path):
                    ansible.role(
                        cluster = arguments.CLUSTER,
                        path = path,
                        user = arguments['--user'],
                    )


if __name__ == '__main__':
    import sys
    rolepath = sys.argv[1]

    c = AnsibleCommand()
    c.role(path=rolepath)
