from __future__ import print_function

from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.vm import Vm



_db = CloudmeshDatabase()


class Cluster(object):

    def __init__(self, name=None, cloudname=None, username=None,
                 imagename=None, flavorname=None, keyname=None,
                 secgroupname=None):

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


    def add_instance(self, addFloatingIP=True):
        """Boots a new instance and adds it to this cluster
        """

        vm = Vm.boot(
            cloud=self.cloudname,
            key=self.keyname,
            name=Vm.generate_vm_name(),
            image=self.imagename,
            flavor=self.flavorname,
            group=self.secgroupname,
        )

        self._instances.append(vm)

