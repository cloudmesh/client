""" run with

python setup.py install; nosetests -v --nocapture tests/cm_basic/test_model.py:Test_model.test_001

nosetests -v --nocapture tests/cm_basic/test_model.py

or

nosetests -v tests/cm_basic/test_model.py

"""
from __future__ import print_function

from pprint import pprint
from cloudmesh_client.common.FlatDict import FlatDict
from cloudmesh_client.db import VM_OPENSTACK, VM_LIBCLOUD
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.db import database

from cloudmesh_client.util import banner
from cloudmesh_client.util import HEADING
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.default import Default
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.shell.console import Console



# noinspection PyPep8Naming
class Test_cloud_model(object):

    data = dotdict({
        "cloud": Default.get_cloud(),
    })

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c="-")
        print(command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return str(result)

    def setup(self):
        self.d = {
            'cloud': 'india',
            'update': '2015-06-18 22:11:48 UTC',
            'user': 'gregor',
            'extra': {'created': '2015-05-21T20:37:10Z',
                      'metadata': {'base_image_ref': '398746398798372493287',
                                   'description': None,
                                   'image_location': 'snapshot',
                                   'image_state': 'available',
                                   'image_type': 'snapshot',
                                   'instance_type_ephemeral_gb': '0',
                                   'instance_type_flavorid': '3',
                                   'instance_type_id': '1',
                                   'instance_type_memory_mb': '4096',
                                   'instance_type_name': 'm1.medium',
                                   'instance_type_root_gb': '40',
                                   'instance_type_rxtx_factor': '1.0',
                                   'instance_type_swap': '0',
                                   'instance_type_vcpus': '2',
                                   'instance_uuid': '386473678463876387',
                                   'kernel_id': None,
                                   'network_allocated': 'True',
                                   'owner_id': '36487264932876984723649',
                                   'ramdisk_id': None,
                                   'user_id': '762387463827463278649837'},
                      'minDisk': 40,
                      'minRam': 0,
                      'progress': 100,
                      'serverId': 'yiuksajhlkjahl',
                      'status': 'ACTIVE',
                      'updated': '2015-05-27T02:11:48Z'},
            'id': '39276498376478936247832687',
            'name': 'VM with Cloudmesh Configured Completely'
        }

        self.vm = {
            'extra': {'access_ip': '',
                      'availability_zone': 'nova',
                      'config_drive': '',
                      'created': '2015-06-19T00:06:58Z',
                      'disk_config': 'MANUAL',
                      'flavorId': '1',
                      'hostId': '',
                      'imageId': 'abcd',
                      'key_name': None,
                      'metadata': {},
                      'password': '********',
                      'tenantId': '1234',
                      'updated': '2015-06-19T00:06:58Z',
                      'uri': 'http://i5r.idp.iu.futuregrid.org/v2/1234/servers/abcd'},
            'id': '67f6bsf67a6b',
            'image': None,
            'name': 'gregor-cm_test',
            'private_ips': [],
            'public_ips': [],
            'size': None,
            'state': 3
        }

        self.d = FlatDict(self.vm)
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_001(self):
        HEADING("check the model")
        d = self.d

        banner("VM Data")
        pprint(d.__dict__)

        banner("Add VM")
        cm = CloudmeshDatabase()


        name = "vm1"
        uuid = d.id

        vm = VM_OPENSTACK(name=name,
                          uuid=uuid,
                          user="test",
                          category=self.data.cloud,
                          **d)
        banner("VM added")

        pprint(vm.__dict__)
        vm.bla = "bla"
        cm.add(vm)
        cm.save()

        banner("Get VM from Database")

        o = cm.find(VM_OPENSTACK, name=name)
        # o = cm.find_by_name(VM, name)
        pprint(o)

        assert True

    def test_002(self):
        HEADING("VM DB test")
        result = self.run("make db")
        cm = CloudmeshDatabase()

        print ("ADD TO OS ")
        for index in range(1,6):
            name = "vm_" + str(index).zfill(3)
            print ("ADD", name)
            try:
                vm = VM_OPENSTACK(name=name,
                                  uuid="uuid_"+str(index),
                                  user="test",
                                  category=self.data.cloud)
            except Exception as e:
                Console.error("issue adding vm", traceflag=True)
            print ("VM", vm.__dict__)
            cm.add(vm)
        print ("ADD TO LIBCLOUD ")
        for index in range(6,11):
            name = "vm_" + str(index).zfill(3)
            vm = VM_LIBCLOUD(name=name,
                             uuid="uuid_"+str(index),
                             user="test",
                             category=self.data.cloud)
            cm.add(vm)
        cm.save()

        result = self.run("cm refresh off")
        print (result)
        result = self.run("cm vm list")
        print(result)



    def test_003(self):
        HEADING("find vm tables")
        cm = CloudmeshDatabase()


        print ("---------")
        all_tables = cm.db.tables()
        for t in all_tables:
            print (t.__tablename__, t.kind)

        print ("---------")
        vm_tables = cm.db.tables(kind="vm")
        for t in vm_tables:
            print (t.__tablename__, t.kind)
        assert len(vm_tables) == 2


    def test_004(self):
        HEADING("find vm tables")
        cm = CloudmeshDatabase()

        print ("-------------")
        vm = cm.x_find(name="vm_001")
        pprint (vm)
        #assert vm.provider == 'openstack'


        print ("-------------")
        vm = cm.x_find(name="vm_006")
        pprint (vm)
        #assert vm.provider == 'libcloud'

        print ("-------------")
        vms = cm.x_find(kind="vm", scope="all")
        pprint (vms)
        print (len(vms))
        #assert len(vms) == 10

