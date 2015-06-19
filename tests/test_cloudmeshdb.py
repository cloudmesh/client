""" run with

nosetests -v --nocapture

or

nosetests -v

"""
from __future__ import print_function
from cloudmesh_base.util import HEADING
from  cloudmesh_client.db import FLAVOR, VM, DEFAULT, IMAGE
from pprint import pprint
import cloudmesh_client

class Test_cloudmeshdb:
    def setup(self):
        self.cm = cloudmesh_client.db.CloudmeshDatabase(cm_user="gregor")
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
        d = cm.get(FLAVOR)
        print("9999")
        pprint(d)
        print("8888")

        d = cm.flavors(clouds="india")
        print ("DICT")
        pprint(d)


        #cm.update("vm", "india")
        #cm.update("images", "india")



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




