


from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.shell.command import (CloudPluginCommand, PluginCommand,
    command)
from cloudmesh_client.shell.console import Console


class AnsibleCommand(object):

    def playbook(self, cluster=None, path=None):
        Console.debug_msg('NotImplementedError')


    def role(self, cluster=None, path=None):
        Console.debug_msg('NotImplementedError')


class DeployCommand(PluginCommand, CloudPluginCommand):
    topics = {'deploy': 'cluster'}

    def __init__(self, context):
        Console.debug_msg("init command deploy")

    @command
    def do_deploy(self, args, arguments):
        """
        ::
            Usage:
              deploy ansible playbook [-p PATH...] [CLUSTER]
              deploy ansible role [-p PATH...] [CLUSTER]

            Commands:

              ansible                        Ansible deployment

            Ansible Commands:
              playbook                       Deploy a pre-prepared playbook
              role                           Deploy a role to all nodes

            Arguments:

              CLUSTER [default=active]       Cluster name to deploy to
              NAME                           Alphanumeric name
              COUNT                          Integer > 0
              PATH                           Path to entry on the filesystem

            Options:

              -p --path=PATH                 Path to the location of the item

        """

        arguments = dotdict(arguments)

        if arguments.ansible and arguments.playbook:
            ansible = AnsibleCommand()
            ansible.playbook(
                cluster = arguments.CLUSTER,
                path = arguments['--path'],
            )

        elif arguments.ansible and arguments.role:
            ansible = AnsibleCommand()
            ansible.role(
                cluster = arguments.CLUSTER,
                path = arguments['--path'],
            )
