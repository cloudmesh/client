
import os.path

from cloudmesh_client.platform.virtual_cluster.cluster import Cluster
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.default import Default
from cloudmesh_client.deployer.ansible.inventory import Inventory
from cloudmesh_client.deployer.ansible.role import AnsibleRole
from cloudmesh_client.deployer.ansible.playbook import AnsiblePlaybook
from cloudmesh_client.shell.command import (CloudPluginCommand, PluginCommand,
    command)
from cloudmesh_client.shell.console import Console


class AnsibleCommand(object):

    def playbook(self, cluster=None, path=None):
        Console.debug_msg('NotImplementedError')


    def role(self, cluster=None, uris=None, hostsPattern='all',
             become=True, username=None, modifyKnownHosts=True):
        """Deploy a role to all the nodes in the cluster

        :param str cluster: cluster name (default is the active cluster)
        :param str path: path to the role (default is current working directory)
        :param str username: login username of the nodes (overrides autodetected value)
        :param modifyKnownHosts: whether to update ~/.ssh/known_hosts
        """

        uris = uris or []
        assert len(uris) > 0, uris

        cluster = Cluster.from_name(cluster or Default.cluster)
        inventory = Inventory.from_cluster(cluster)
        roles = [AnsibleRole(uri, become=become, hosts=hostsPattern) for uri in uris]
        play = AnsiblePlaybook(
            roles=roles,
            inventory=inventory,
            username=username,
            modifyKnownHosts=modifyKnownHosts,
            subprocess_kwargs=dict(stdout=None, stderr=None),
        )

        play.run()



class DeployCommand(PluginCommand, CloudPluginCommand):
    topics = {'deploy': 'cluster'}

    def __init__(self, context):
        Console.debug_msg("init command deploy")

    @command
    def do_deploy(self, args, arguments):
        """
        ::
            Usage:
              deploy ansible role [-c CLUSTER] [-u NAME] [-N] [-H HOST] [-b] URI...

            Commands:

              ansible                        Ansible deployment

            Ansible Commands:
              playbook                       Deploy a pre-prepared playbook
              role                           Deploy a role to all nodes

            Arguments:

              CLUSTER                        Cluster name to deploy to
              NAME                           Alphanumeric name
              COUNT                          Integer > 0
              URI                            Location of the item as a uri
              HOST                           Host matching pattern

            Options:

              -c --cluster=CLUSTER           Cluster name to operate on (defaults to active)
              -N --no-modify-known-hosts     Don't let ssh update ~/.ssh/known_hosts
              -u --username=NAME             Username of the nodes to manage
              -H HOST --hosts=HOST           Host matching pattern [default: all]
              -b --no-become                 Don't become privileged user
        """

        arguments = dotdict(arguments)
        from pprint import pprint
        pprint(arguments)

        if arguments.ansible and arguments.role:
            ansible = AnsibleCommand()
            ansible.role(
                cluster = arguments.CLUSTER,
                hostsPattern = arguments['--hosts'],
                uris = arguments.URI,
                become = not arguments['--no-become'],
                username = arguments['--username'],
                modifyKnownHosts = not arguments['--no-modify-known-hosts'],
            )


if __name__ == '__main__':
    from docopt import docopt
    print(docopt(DeployCommand.do_deploy.__doc__))


    # import sys
    # rolepath = sys.argv[1]

    # c = AnsibleCommand()
    # c.role(path=rolepath)
