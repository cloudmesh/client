from __future__ import print_function

from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.db.general.model import CLUSTER
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.network import Network
from cloudmesh_client.cloud.vm import Vm


_db = CloudmeshDatabase()


class Cluster(CLUSTER):

    def __init__(self, *args, **kwargs):
        super(Cluster, self).__init__(*args, **kwargs)

        self.provider = CloudProvider(self.cloud).provider.cloud_type

        _db.insert(self)

    @property
    def instances(self):

        tablename = 'vm_{}'.format(self.provider)
        table = _db.table_from_name(tablename)
        return _db.select(table, cluster=self.name).all()

    def __len__(self):
        return len(self.instances)

    def _assign_floating_ip(self, vm):
        """Assign a floating ip

        :returns: floating ip
        :rtype: :class:`str`
        """

        ip = Network.find_assign_floating_ip(
            cloudname=self.cloud,
            instance_id=vm.name,
        )

        Vm.refresh(cloud=self.cloud)

        return ip

    def assign_floating_ip(self):
        """Assign a floating ip to all nodes in the cluster, if they do not
        already have one
        """

        for vm in self.instances:
            if not vm.floating_ip:
                self._assign_floating_ip(vm)

    def boot_single(self):
        """Boots a new instance and adds it to this cluster
        """

        instance_name = Vm.generate_vm_name()

        uuid = Vm.boot(
            cloud=self.cloud,
            key=self.key,
            name=instance_name,
            image=self.image,
            flavor=self.flavor,
            group=self.secgroup,
            cluster=self.name,
        )

        model = _db.table(name='vm_{}'.format(self.provider))
        vm = _db.select(model, uuid=uuid).all()
        assert len(vm) == 1, vm
        vm = vm[0]

        if self.assignFloatingIP:
            vm.floating_ip = self._assign_floating_ip(vm)

    def boot(self):
        """Boot all the nodes in the cluster
        """

        for _ in xrange(self.count - len(self.instances)):
            self.boot_single()
