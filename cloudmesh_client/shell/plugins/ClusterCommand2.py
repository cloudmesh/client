from __future__ import print_function

import sys
from cloudmesh_client.platform.virtual_cluster.cluster import Cluster

from cloudmesh_client.cloud.image import Image
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.default import Default, Names
from cloudmesh_client.deployer.ansible.inventory import Inventory, Node
from cloudmesh_client.exc import (ClusterNameClashException,
    NoActiveClusterException, UnrecoverableErrorException)
from cloudmesh_client.shell.command import (CloudPluginCommand, PluginCommand,
    command)
from cloudmesh_client.shell.console import Console


db = CloudmeshDatabase


class Command(object):
    def create(self, clustername=None, cloud=None, count=1,
               username=None, image=None, flavor=None, key=None,
               secgroup=None, assignFloatingIP=True,
               activate=True):
            """Create a cluster.

            If values are `None`, they are automatically determined via
            defaults.

            :param str clustername: name of this cluster (generated if None)
            :param str cloud: cloud name
            :param int count: number of instances in the cluster
            :param str user: cloudmesh user
            :param str username: cloud image username
            :param str image: image name
            :param str flavor: instance flavor
            :param str key: key name
            :param str secgroup: security group name
            :param bool activate: activate this cluster after creation
            :returns: a cluster
            :rtype: :class:`Cluster`
            """

            clustername = clustername or Default.generate_name(Names.CLUSTER_COUNTER)
            cloud = cloud or Default.cloud
            username = username or Image.guess_username(image)
            image = image or Default.image
            flavor = flavor or Default.flavor
            key = key or Default.key
            secgroup = secgroup or Default.secgroup

            try:
                cluster = Cluster(
                    name=clustername,
                    count=count,
                    cloud=cloud,
                    username=username,
                    image=image,
                    flavor=flavor,
                    key=key,
                    secgroup=secgroup,
                    assignFloatingIP=assignFloatingIP,
                )
            except ClusterNameClashException as e:
                Console.error(str(e))
                raise UnrecoverableErrorException(str(e))

            cluster.create()
            Console.ok('Cluster {} created'.format(clustername))

            if activate:
                Default.set_cluster(clustername)
                Console.ok('Cluster {} is now active'.format(clustername))

            return cluster

    def list(self):
        """List the clusters created

        The currently active cluster is given as the first element in
        the tuple, while the remainder are listed in the second
        position.

        :returns: a pair: (active, [clusters])
        :rtype: :class:`tuple` (:class:`Cluster`, :class:`list` of :class:`Cluster`)
        :raises: :class:`NoActiveClusterException` if no cluster is active, meaning there are no clusters
        """

        activename = Default.active_cluster.name
        clusters = db.select(Cluster).all()
        active = filter(lambda c: c.name == activename, clusters)[0]
        clusters = filter(lambda c: c.name != activename, clusters)
        return active, clusters

    def delete(self, clusternames=None, force=False, all=False):
        """Delete clusters that have these names.

        If not specified, delete the active cluster.
        If there is no active cluster, delete the first cluster.

        :param list clusternames: list of cluster names to delete
        """

        if all:
            clusters = db.select(Cluster)
        else:

            clusternames = clusternames or [Default.cluster]
            clusters = [db.select(Cluster, name=name).one()
                        for name in clusternames]

        for cluster in clusters:
            Console.ok('Deleting cluster {}'.format(cluster.name))
            cluster.delete(force=force)
            Console.ok('Deleted cluster {}: {} nodes'
                       .format(cluster.name, cluster.count))

        remaining_clusters = db.select(Cluster).all()
        if remaining_clusters:
            name = remaining_clusters[-1].name
        else:
            name = None
        Default.set_cluster(name)
        Console.ok('Active cluster: {}'.format(name))

    def get(self, property, cluster=None):
        """Retrieve the property for a cluster/nodes in a cluster.

        If no cluster is specified, use the currently active cluster.

        :param str property: name of the property
        :param Cluster cluster: the cluster (default: currently active)
        :returns: a list of the values
        :rtype: :class:`list`

        """
        cluster = cluster or db.select(Cluster, name=Default.cluster).one()

        # getting from the cluster itself:
        if hasattr(cluster, property):
            return [getattr(cluster, property)]

        # assume it is a property of the instances
        else:
            values = [getattr(node, property) for node in cluster]
            return values

    def nodes(self, cluster=None):
        """Retrieve the nodes of a cluster

        If no cluster is specified, use the currently active cluster.

        :param Cluster cluster: the cluster (default: currently active)
        :returns: a list of instances
        :rtype: a VM instance

        """

        cluster = cluster or Default.active_cluster
        return cluster.list()


    def inventory(self, cluster=None, format=None, path=None):

        cluster = cluster or Default.active_cluster
        format = format or 'ansible'

        if format == 'ansible':

            inventory = Inventory.from_cluster(cluster)
            inv_ini = inventory.ini()

            if not path:
                print(inv_ini)
            else:
                with open(path, 'w') as fd:
                    fd.write(inv_ini)

            return inventory


class Cluster2Command(PluginCommand, CloudPluginCommand):
    topics = {'cluster2': 'cluster'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command cluster2 ")

    @command
    def do_cluster2(self, args, arguments):
        """
        ::
            Usage:
              cluster2 create [-n NAME] [-c COUNT] [-C CLOUD] [-u NAME] [-i IMAGE] [-f FLAVOR] [-k KEY] [-s NAME] [-AI]
              cluster2 list
              cluster2 nodes [CLUSTER]
              cluster2 delete [--all] [--force] [NAME]...
              cluster2 get [-n NAME] PROPERTY
              cluster2 inventory [-F NAME] [-o PATH] [NAME]

            Commands:

              create     Create a cluster
              list       List the available clusters
              inventory  Obtain an inventory file
              delete     Delete clusters and associated instances
              get        Get properties of a cluster/nodes in a cluster

            Arguments:

              NAME                Alphanumeric name
              COUNT               Integer > 0
              PATH                Path to entry on the filesystem

            Options:

              -A --no-activate               Don't activate this cluster
              -I --no-floating-ip            Don't assign floating IPs
              -n NAME --name=NAME            Name of the cluster
              -c COUNT --count=COUNT         Number of nodes in the cluster
              -C NAME --cloud=NAME           Name of the cloud
              -u NAME --username=NAME        Name of the image login user
              -i NAME --image=NAME           Name of the image
              -f NAME --flavor=NAME          Name of the flavor
              -k NAME --key=NAME             Name of the key
              -s NAME --secgroup=NAME        NAME of the security group
              -F NAME --format=NAME          Name of the output format
              -o PATH --path=PATH            Output to this path
              --force
              --all

            Inventory File Format:

              ansible  [default]            Ansible-compatible inventory
        """

        arguments = dotdict(arguments)
        cmd = Command()

        if arguments.create:

            cmd.create(
                clustername=arguments['--name'],
                count=arguments['--count'] or 1,
                cloud=arguments['--cloud'] or Default.cloud,
                username=arguments['--username'],
                image=arguments['--image'] or Default.image,
                flavor=arguments['--flavor'] or Default.flavor,
                key=arguments['--key'] or Default.key,
                secgroup=arguments['--secgroup'] or Default.secgroup,
                assignFloatingIP=not arguments['--no-floating-ip'],
            )

        elif arguments.list:

            try:
                active, inactive = cmd.list()
            except NoActiveClusterException:
                return

            def show(cluster, isactive=False, stream=sys.stdout):
                if not cluster:
                    return
                if isactive:
                    stream.write('> ')
                else:
                    stream.write('  ')
                stream.write(cluster.name)
                stream.write('\n')
                stream.flush()

            show(active, isactive=True)
            map(show, inactive)

        elif arguments.nodes:

            cluster = db.select(Cluster, name=arguments.CLUSTER).one() \
                    if arguments.CLUSTER \
                    else None
            nodes = cmd.nodes(cluster=cluster)
            for node in nodes:
                print(node.name)

        elif arguments.delete:

            cmd.delete(
                arguments.NAME,
                force=arguments['--force'],
                all=arguments['--all']
            )

        elif arguments['get']:

            values = cmd.get(arguments['PROPERTY'], cluster=arguments['--name'])
            for v in values:
                print(v)

        elif arguments.inventory:
            cmd.inventory(
                cluster=arguments.NAME,
                format=arguments['--format'],
                path=arguments['--path'],
            )



if __name__ == '__main__':
    cmd = Cluster2Command()
    cmd.create(
        clustername='test3',
        image='CC-Ubuntu14.04',
        flavor='m1.medium',
        key='gambit',
        count=3,
    )


