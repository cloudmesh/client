from __future__ import print_function

from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.vm import Vm

from cloudmesh_client.cloud.network import Network


_db = CloudmeshDatabase()


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

    @classmethod
    def create(cls, **kwargs):
        """Either load a cluster or create a new one.

        kwargs are passed directly to the constructor
        """

        # FIXME: check database
        return cls(**kwargs)


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

        self._instances.append(vm)

