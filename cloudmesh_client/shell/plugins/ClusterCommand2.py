from __future__ import print_function

from pprint import pprint

from cloudmesh_client.exc import UnrecoverableErrorException
from cloudmesh_client.cloud.cluster import Cluster, ClusterNameClashException, generate_cluster_name
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase

# from cloudmesh_client.cloud.vm import Vm
from cloudmesh_client.cloud.image import Image
# from cloudmesh_client.cloud.flavor import Flavor
# from cloudmesh_client.cloud.group import Group


db = CloudmeshDatabase


class Cluster2Command(PluginCommand, CloudPluginCommand):
    topics = {'cluster2': 'cluster'}

    def create(self, clustername=None, cloud=None, count=1, user=None,
               username=None, image=None, flavor=None, key=None,
               secgroup=None):
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
        :returns: a cluster
        :rtype: :class:`Cluster`
        """

        clustername = clustername or None  # FIXME
        cloud = cloud or Default.cloud
        user = user or Default.user
        image = image or Default.image
        username = username or Image.guess_username(image)
        flavor = flavor or Default.flavor
        key = key or Default.key
        secgroup = secgroup or Default.secgroup

        try:
            cluster = Cluster(
                name=clustername,
                count=count,
                cloud=cloud,
                user=username,
                image=image,
                flavor=flavor,
                key=key,
                secgroup=secgroup
            )
        except ClusterNameClashException as e:
            Console.error(str(e))
            raise UnrecoverableErrorException(str(e))

        cluster.boot()
        Console.ok('Cluster {} created'.format(clustername))
        return cluster

    def list(self):
        """List the clusters created

        :returns: a list of clusters
        :rtype: :class:`list` of :class:`Cluster`
        """

        return db.select(Cluster).all()

    @command
    def do_cluster2(self, args, arguments):
        """
        ::
            Usage:
              cluster2 create [-n NAME] [-c COUNT] [-C CLOUD] [-u USER] [-i IMAGE] [-f FLAVOR] [-k KEY] [-s NAME]
              cluster2 list

            Commands:

              create     Create a cluster
              list       List the available clusters

            Arguments:

              NAME                Alphanumeric name
              COUNT               Integer > 0

            Options:

              -n NAME --name=NAME            Name of the cluster
              -c COUNT --count=COUNT         Number of nodes in the cluster
              -C NAME --cloud=NAME           Name of the cloud
              -u USER --user=NAME
              -i NAME --image=NAME           Name of the image
              -f NAME --flavor=NAME          Name of the flavor
              -k NAME --key=NAME             Name of the key
              -s NAME --secgroup=NAME        NAME of the security group
        """

        arguments = dotdict(arguments)

        if arguments.create:

            self.create(
                clustername=arguments['--name'] or generate_cluster_name(),
                count=arguments['--count'] or 1,
                cloud=arguments['--cloud'] or Default.cloud,
                user=arguments['--user'] or Default.user,
                image=arguments['--image'] or Default.image,
                flavor=arguments['--flavor'] or Default.flavor,
                key=arguments['--key'] or Default.key,
                secgroup=arguments['--secgroup'] or Default.secgroup,
            )

        elif arguments.list:

            for cluster in self.list():
                print(cluster.name)


if __name__ == '__main__':
    cmd = Cluster2Command()
    cmd.create(
        clustername='test3',
        image='CC-Ubuntu14.04',
        flavor='m1.medium',
        key='gambit',
        count=3,
    )


