import time
from cloudmesh_client.api import Provider

from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.network import Network
from cloudmesh_client.cloud.vm import Vm
from cloudmesh_client.db import CloudmeshDatabase, IntegrityError
from cloudmesh_client.db.general.model import CLUSTER
from cloudmesh_client.exc import ClusterNameClashException
from cloudmesh_client.shell.console import Console


class Cluster(CLUSTER):  # list abstraction see other commands

    cm = CloudmeshDatabase()


    def __init__(self, *args, **kwargs):

        # Use the table defined in the model, but we need to look up
        # the provider object dynamically

        super(Cluster, self).__init__(*args, **kwargs)
        self.provider = CloudProvider(self.cloud).provider.cloud_type

        # put this cluster in the database, the 'name' attribute must
        # be unique

        try:
            self.cm.insert(self)
        except IntegrityError as e:
            line = 'UNIQUE constraint failed: {}.name'\
                   .format(self.__tablename__)
            if line in e.message:
                raise ClusterNameClashException(self.__tablename__,
                                                self.name)

    @classmethod
    def from_name(cls, name):
        return cls.cm.select(Cluster, name=name).one()


    def __iter__(self):
        return iter(self.list())

    def list(self):
        """List the nodes in the cluster.

        The type of the instance is determined by the provider.

        :returns: the nodes of the cluster
        :rtype: :class:`list` of instances
        """

        table = self.cm.vm_table_from_provider(self.provider)
        return self.cm.select(table, cluster=self.name).all()

    def delete(self, force=False):
        """Delete this cluster and all component nodes"""
        for node in self:
            Vm.delete(servers=[node.name], force=force)

        self.cm.delete_(self.__class__, cm_id=self.cm_id)

    def create(self, sleeptime_s=5):
        """Boot all nodes in this cluster

        :param float sleeptime_s: sleep this number of seconds between
                                  polling VMs for ACTIVE status
        """
        for _ in xrange(self.count - len(self.list())):
            self.add()

    def add(self):
        """Boots a new instance and adds it to this cluster"""

        provider = Provider.from_cloud(self.cloud)

        Console.info('Booting VM for cluster {}'.format(self.name))
        node = provider.boot(
            key      = self.key,
            image    = self.image,
            flavor   = self.flavor,
            secgroup = self.secgroup,
            cluster  = self.name,
            username = self.username
        )

        if self.assignFloatingIP:
            node.create_ip()

    def remove(self, cm_id):
        """Removes a node to the cluster, but otherwise leaves it intact.

        See :meth:`delete` to delete this cluster

        :param int cm_id: the node id of the instance to remove
        """

        table = self.cm.vm_table_from_provider(self.provider)
        self.cm.update_(
            table,
            where={'cm_id': cm_id},
            values={'cluster': None}
        )

    def modify(self):
        "Modifies the cluster"
        raise NotImplementedError()

    def terminate(self):
        "Terminates the cluster"
        raise NotImplementedError()

    def suspend(self):
        "Suspends the cluster"
        raise NotImplementedError()

    def resume(self):
        "Resumes the cluster"
        raise NotImplementedError()

    def add_key(self, public_key):
        "Adds an ssh public key to the cluster"
        raise NotImplementedError()

    def remove_key(self, public_key):
        "Removes an ssh public key from the cluster"
        raise NotImplementedError()

    def enable_cross_ssh_login(self):
        "Enables each node to log into all other nodes of the cluster"
        raise NotImplementedError()

    def disable_cross_ssh_login(self):
        raise NotImplementedError()

    def delete_key(self):
        raise NotImplementedError()

    # """

    # Parameter.expand

    # cluster
    #     name
    #     node+
    #                     (some object in models)
    #         label
    #         name
    #         ip+
    #         private key
    #         ssh authorized keys
    #         owner
    #         user

    # type cluster
    # type node

    # """
