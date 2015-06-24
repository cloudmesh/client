""" run with

nosetests -v --nocapture

or

nosetests -v

"""
from __future__ import print_function
from cloudmesh_base.util import HEADING
from  cloudmesh_client.db import FLAVOR, VM, DEFAULT, IMAGE
from pprint import pprint
from cloudmesh_client.db import CloudmeshDatabase, VM, FLAVOR, IMAGE, DEFAULT, Insert
from cloudmesh_client.iaas.openstack_libcloud import OpenStack_libcloud
from datetime import datetime

class Test_cloudmeshdb:
    def setup(self):
        self.cm = CloudmeshDatabase(cm_user="gregor")
        pass


    def tearDown(self):
        pass

    def test_001_name(self):
        HEADING()
        cm = self.cm

        name = "gregor-001"
        cm.name(name)
        result = cm.get_name()
        assert result == name
        result = cm.next_name()
        print (result)
        assert result == "gregor-002"

    def test_002_add(self):
        HEADING()
        cm = self.cm

        print ("Delete all vms ...")
        cm.delete_all("VM")

        print ("Create 3 vms ...")
        vms = []
        vms.append(VM('gregor1'))
        vms.append(VM('gregor1'))
        vms.append(VM('gregor2'))

        print ("Add vms ...")
        cm.add(vms)
        print ("Save vms ...")
        cm.save()

        found1 = 0
        found2 = 0
        for v in cm.data.query(VM):
            print (v.name, v.cm_uuid)
            if v.name == "gregor1":
                found1 = found1 + 1
            if v.name == "gregor2":
                found2 = found2 + 1

        print ("found", found1, found2)
        assert found1 == 2 and found2 == 1

    def test_003_find(self):
        """finding a specific vm"""
        HEADING()
        cm = self.cm

        name = "gregor1"
        cursor = cm.find(VM, name="gregor1")
        for vm in cursor:
            print (vm.name, vm.id, vm.cloud)
        assert True

    def test_004_find_by_name(self):
        """finding a specific vm"""
        HEADING()
        cm = self.cm

        cursor = cm.find_vm_by_name(name="gregor1")
        print (cursor is not None)
        cursor = cm.find_vm_by_name(name="doesnotexist")
        assert cursor is None

    def test_005_delete(self):
        """delete vms"""
        HEADING()
        cm = self.cm

        cm.delete_all()


    def test_006_replace(self):
        HEADING()
        cm = self.cm

        for erase_type in [True, False]:
            print ("Erase Type", erase_type)
            cm.delete_all("VM")

            vm = VM('gregor1')
            vm.cloud = "india"
            cm.add([vm])
            cm.save()

            vm = VM('gregor1')
            vm.group = "hallo"
            cm.replace(VM, [vm], erase=erase_type)
            cm.save()

            found_vm = None
            found1 = 0
            for v in cm.data.query(VM):
                if v.name == "gregor1":
                    found1 = found1 + 1
                    found_vm = v

            print ("found", found1)
            print (v.name, v.group, v.cloud)
            assert found1 == 1 and v.group == "hallo"
            if erase_type:
                assert v.cloud is None
            else:
                assert v.cloud == "india"

    def test_006_update(self):
        HEADING()
        cm = self.cm

        cm.update("flavor", "india")
        print ("UUUU")
        d = cm.get(FLAVOR)
        print("9999")
        pprint(d)
        print("8888")

        d = cm.flavors(clouds="india")
        print ("DICT")
        pprint(d)


        cm.update("image", "india")

        cm.update("vm", "india")



    def test_007_boot(self):
        HEADING()
        cm = self.cm

        cloud = "india"
        cm_user = "gregor"
        name = "gregor"
        image = "futuresystems/ubuntu-14.04"
        flavor = "m1.tiny"
        key = "~/.ssh/id_rsa.pub"
        meta = None

        ## r = cm.boot(cloud, cm_user, name, image, flavor, key, meta)
        # pprint (r)

    def test_008_flatten(self):
        HEADING()
        cm = self.cm

    def test_009_add(self):
        HEADING()
        cm = self.cm

        vm1 = VM('gregor1')
        d = {"invalid":"noting",
             "label": "mylabel"}



    def test_009_paramater(self):
        HEADING()

        from cloudmesh_base.hostlist import Parameter
        parameter = "india[01-03]"
        result = Parameter.expand(parameter)
        print (result)
        assert str(result) == "['india01', 'india02', 'india03']"

    def test_010_dict(self):
        HEADING()


        cm = self.cm

        a = {
            'x': 1,
            'y': 2,
            'z': 3,
        }


        b = {
            'mm': 30,
            'xx': 10,
            'yy': 20,
        }

        mapping = {
            'x': 'xx',
            'y': 'yy',
        }



        r = Insert.merge_two_dicts(a, b)
        print (r)
        assert len(r) == len(a) + len(b)

        r = Insert.merge_into(a, b, mapping, erase=False)

        print (r)
        assert r['y'] == 20 and r['x'] == 10

    def  test_011_data(self):
        HEADING()

        cm = self.cm

        image_dict = {
             'cm_cloud': 'india',
             'cm_update': '2015-06-24 00:55:00 UTC',
             'cm_user': 'gregor',
             'created': '2015-03-23T20:50:29Z',
             'id': '58e5d678-79ec-4a4d-9aa8-37975b7f40ac',
             'minDisk': 0,
             'minRam': 0,
             'name': 'futuresystems/fedora-21',
             'progress': 100,
             'serverId': None,
             'status': 'ACTIVE',
             'updated': '2015-03-23T20:50:33Z'
        }

        image_id = image_dict['id']

        elements = cm.find(FLAVOR, cm_cloud='india', name='m1.small_e30').all()
        for element in elements:
            d = cm.o_to_d(element)
            pprint (d)
            # d = cm.object_to_dict(element)
            #pprint(d)


        cloud = OpenStack_libcloud("india", cm_user="gvonlasz")
        result = cloud.list("flavor", output="flat")
        f = result["1"]
        f["label"] = "newlabel"

        cm.update_from_dict(f)
        cm.save()
        pprint(f)



        elements = cm.find(FLAVOR, name='m1.tiny').all()
        for e in elements:
            pprint(cm.o_to_d (e))
"""
pprint(cm.dict(cloudmesh_db.VM))
pprint(cm.json(cloudmesh_db.VM))

for output in ["dict", "json", "yaml", "table"]:
    print (dict_printer(cm.dict(cloudmesh_db.VM), output=output))

# d = [DEFAULT(name="user", value="albert")]
# db.add(d)
# db.save()

cm.default("cloud", "india", cloud="india")
cm.default("user", getpass.getuser(), cloud="india")

for v in cm.data.query(cloudmesh_db.DEFAULT):
    print (v.name, v.value, v.cloud)

print (dict_printer(cm.dict(cloudmesh_db.DEFAULT), output='yaml'))

print (dict_printer(cm.dict(cloudmesh_db.DEFAULT),
                    order=['id', 'cloud', 'name', 'value']))
"""




