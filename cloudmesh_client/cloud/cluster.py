from __future__ import print_function

from sqlalchemy import Column, Boolean, String

from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.db import CloudmeshDatabase, CloudmeshMixin
from cloudmesh_client.cloud.vm import Vm

from cloudmesh_client.cloud.network import Network


_db = CloudmeshDatabase()


class ClusterModel(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = 'cluster'
    __kind__ = 'cluster'

    name = Column(String)
    cloudname = Column(String)
    username = Column(String)
    imagename = Column(String)
    flavorname = Column(String)
    keyname = Column(String)
    secgroupname = Column(String)
    assignFloatingIP = Column(Boolean)

    @classmethod
    def _cluster(cls, **kwargs):
        """Create a single :class:`Cluster` instance from a single row in the
        cluster table

        Here, ``kwargs`` is a :class:`dict` mapping column name to
        value for this row.

        :returns: the cluster
        :rtype: :class:`Cluster`
        """

        cluster_details = dotdict(kwargs)
        table_name = 'vm_{}'.format(cluster_details.provider)
        table = _db.table(name=table_name)

        cluster = Cluster(
            name=cluster_details.name,
            cloudname=cluster_details.cloud,
            username=cluster_details.user,
            imagename=cluster_details.image,
            secgroupname=cluster_details.secgroup,
            assignFloatingIP=cluster_details.assignFloatingIP
        )

        for vm_details in _db.find(table=table,
                                   cluster=cluster_details.cluster):
            cluster.add_existing_instance(vm_details)

        return cluster

    @classmethod
    def iter(cls):
        """List all the entries

        :returns: all the Clusters
        :rtype: :class:`list` of :class:`Cluster`
        """

        for key_value in _db.find(table=cls):
            cluster = cls._cluster(**key_value)
            yield cluster


    @classmethod
    def register(cls, cluster):
        """Register a cluster to the database

        :param Cluster cluster: the cluster to register
        :returns: 
        :rtype: 
        """

        row_values = cluster.__dict__
        row_values.pop('_instances')
        obj = cls(**row_values)

        _db.insert(obj)



class Cluster(object):

    def __init__(self, name=None, cloudname=None, username=None,
                 imagename=None, flavorname=None, keyname=None,
                 secgroupname=None, assignFloatingIP=True):

        assert cloudname is not None
        assert imagename is not None
        assert flavorname is not None
        assert keyname is not None

        self.name = name
        self.cloudname = cloudname
        self.username = username
        self.imagename = imagename
        self.flavorname = flavorname
        self.keyname = keyname
        self.secgroupname = secgroupname
        self.assignFloatingIP = True

        self._instances = list()

    def __len__(self):
        return len(self._instances)


    def _assign_floating_ip(self, vm):
        """Assign a floating ip

        :returns: floating ip
        :rtype: :class:`str`
        """

        ip = Network.find_assign_floating_ip(
            cloudname=self.cloudname,
            instance_id=vm['name'],
        )

        Vm.refresh(cloud=self.cloudname)

        return ip

    def add_instance(self):
        """Boots a new instance and adds it to this cluster
        """

        instance_name = Vm.generate_vm_name()

        uuid = Vm.boot(
            cloud=self.cloudname,
            key=self.keyname,
            name=instance_name,
            image=self.imagename,
            flavor=self.flavorname,
            group=self.secgroupname,
        )

        vm = Vm.get(instance_name)

        if self.assignFloatingIP:
            vm['floating_ip'] = self._assign_floating_ip(vm)

        self.add_existing_instance(vm)

    def add_existing_instance(self, vm_details):
        """Adds a previously booted instance to the cluster.

        :param vm_details: a dict-like object containing the 
                           details of the vm (eg from Vm.boot)
        """

        self._instances.append(vm_details)
