from __future__ import print_function

from cloudmesh_client.cloud.cluster import Cluster
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console

from cloudmesh_client.default import Default

# from cloudmesh_client.cloud.vm import Vm
from cloudmesh_client.cloud.image import Image
# from cloudmesh_client.cloud.flavor import Flavor
# from cloudmesh_client.cloud.group import Group


class Cluster2Command(PluginCommand, CloudPluginCommand):

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

        cluster = Cluster(
            name=clustername,
            cloudname=cloud,
            username=username,
            imagename=image,
            flavorname=flavor,
            keyname=key,
            secgroupname=secgroup
        )

        cluster.boot()
        Console.ok('Cluster {} created'.format(clustername))
        return cluster


if __name__ == '__main__':
    cmd = Cluster2Command()
    cmd.create(
        clustername='test',
        image='CC-Ubuntu14.04',
        flavor='m1.medium',
        key='gambit',
        count=1,
    )


