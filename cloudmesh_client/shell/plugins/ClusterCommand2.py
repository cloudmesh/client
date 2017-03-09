from __future__ import print_function

import sys
from pprint import pprint
from cloudmesh_client.platform.virtual_cluster.cluster import Cluster

from cloudmesh_client.cloud.image import Image
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.db import SPECIFICATION
from cloudmesh_client.default import Default, Names
from cloudmesh_client.deployer.ansible.inventory import Inventory, Node
from cloudmesh_client.exc import (ClusterNameClashException,
    NoActiveClusterException, UnrecoverableErrorException)
from cloudmesh_client.shell.command import (CloudPluginCommand, PluginCommand,
    command)
from cloudmesh_client.shell.console import Console

db = CloudmeshDatabase


class Command(object):
    def define(self, clustername=None, **kwargs):
            """Define a cluster.

            kwargs are passed to Cluster

            :returns: a cluster
            :rtype: :class:`Cluster`
            """

            clustername = clustername or Default.generate_name(Names.CLUSTER_COUNTER)

            # remove None to defer default definitions to later
            for k in kwargs.keys():
                if kwargs[k] is None:
                    del kwargs[k]

            try:
                spec = db.select(SPECIFICATION, name=clustername, type='cluster')[0]
                spec.update(kwargs)
                db.updateObj(spec)
            except IndexError:
                spec = SPECIFICATION(clustername, 'cluster', kwargs)
                db.insert(spec)

            Default.set_specification(clustername)
            Console.ok('Defined cluster {}'.format(clustername))

    def undefine(self, specname=None, all=False):

        specs = set()

        if all:
            for spec in db.select(SPECIFICATION, type='cluster'):
                specs.add(spec)


        try:
            spec = db.select(SPECIFICATION, type='cluster', name=specname or Default.active_specification)[0]
            specs.add(spec)
        except IndexError:
            pass

        for spec in specs:

            try:
                cluster = db.select(Cluster, specId=spec.cm_id)[0]
                Console.warning('Cannot undefine allocated cluster {}.'.format(cluster.name))
                Console.warning('Please delete the cluster first')
                continue
            except IndexError:
                pass

            db.delete_(SPECIFICATION, cm_id = spec.cm_id)
            Console.ok('Undefined specification {}'.format(spec.name))

        try:
            spec = db.select(SPECIFICATION, type='cluster')[0]
            Default.set_specification(spec.name)
        except IndexError:
            pass

    def use(self, specname):
        """Activate the given specification

        :param specname: namne of the specification
        """
        spec = db.select(SPECIFICATION, type='cluster', name=specname)[0]
        Default.set_specification(spec.name)
        Default.set_cluster(spec.name)


    def avail(self):
        """Show the available cluster specifications
        """

        specs = db.select(SPECIFICATION, type='cluster')
        active = Default.active_specification

        for spec in specs:
            marker = '>' if spec.name == active else ' '
            print('{} {}'.format(marker, spec.name))
            for k, v in spec.get().iteritems():
                print('{:>4}{:<30}: {}'.format('', k, v))



    def allocate(self, clustername=None):

        specname = clustername or Default.active_specification

        try:
            spec = db.select(SPECIFICATION, name=specname)[0]
        except IndexError:
            Console.error('No specification with name={} found'.format(specname))
            return 1

        defns = spec.get()

        try:
            cluster = db.select(Cluster, name=spec.name, specId=spec.cm_id)[0]
        except IndexError:
            cluster = Cluster(name=spec.name, specId=spec.cm_id, **defns)

        Default.set_cluster(cluster.name)
        Console.ok('Cluster {} is now active'.format(cluster.name))

        cluster.create()
        Console.ok('Cluster {} created'.format(cluster.name))

        return cluster

    def cross_ssh(self, clustername=None):

        clustername = clustername = Default.cluster
        cluster = db.select(Cluster, name=clustername)[0]
        cluster.enable_cross_ssh_login()

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

        try:
            import pdb; pdb.set_trace()
            name = cluster or Default.cluster
            cluster = Cluster.from_name(name)
            return cluster.list()
        except:
            Console.error('Cluster {} is active. Did you forget to allocate?'.format(name))
            return []


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
    topics = {'cluster': 'cluster'}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command cluster2 ")

    @command
    def do_cluster(self, args, arguments):
        """
        ::
            Usage:
              cluster define [-n NAME] [-c COUNT] [-C CLOUD] [-u NAME] [-i IMAGE] [-f FLAVOR] [-k KEY] [-s NAME] [-AI]
              cluster undefine [--all] [NAME]...
              cluster avail
              cluster use <NAME>
              cluster allocate
              cluster cross_ssh
              cluster list
              cluster nodes [CLUSTER]
              cluster delete [--all] [--force] [NAME]...
              cluster get [-n NAME] PROPERTY
              cluster inventory [-F NAME] [-o PATH] [NAME]

            Commands:

              define     Create a cluster specification
              undefine   Delete the active or given specifications
              avail      Show available cluster specifications
              use        Activate the specification with the given name
              allocate   Create a cluster from the active specification
              nodes      Show the nodes of the cluster
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

        if arguments.define:

            cmd.define(
                clustername = arguments['--name'],
                count=arguments['--count'] or 1,
                cloud=arguments['--cloud'] or Default.cloud,
                username=arguments['--username'],
                image=arguments['--image'] or Default.image,
                flavor=arguments['--flavor'] or Default.flavor,
                key=arguments['--key'] or Default.key,
                secgroup=arguments['--secgroup'] or Default.secgroup,
                assignFloatingIP=not arguments['--no-floating-ip'],
            )

        elif arguments.undefine:
            if arguments['NAME']:
                for specname in arguments['NAME']:
                    cmd.undefine(specname=specname, all=arguments['--all'])
            else:
                cmd.undefine(all=arguments['--all'])

        elif arguments.avail:

            cmd.avail()

        elif arguments.use:

            cmd.use(arguments['<NAME>'])

        elif arguments.allocate:

            cmd.allocate()

        elif arguments.cross_ssh:

            cmd.cross_ssh()

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

            nodes = cmd.nodes(cluster=arguments['CLUSTER'])

            for node in nodes:
                print(node.name, node.floating_ip)

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


