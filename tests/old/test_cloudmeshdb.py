""" run with

python setup.py install; nosetests -v --nocapture  tests/test_cloudmeshdb.py:Test_cloudmeshdb.test_001

nosetests -v --nocapture tests/test_cloudmeshdb.py

nosetests -v tests/test_cloudmeshdb.py

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

    def test_001(self):
        """001: testing the name management for VMs"""
        HEADING()
        cm = self.cm

        name = "gregor-001"
        cm.name(name)
        result = cm.get_name()
        assert result == name
        result = cm.next_name()
        print (result)
        assert result == "gregor-002"

    def test_002(self):
        """002: testing adding VMs"""
        HEADING()
        cm = self.cm

        print ("Delete all vms ...")
        cm.delete_all("VM")
        r = cm.info("count")

        assert r['VM'] == 0

        pprint (r)

        print ("Create 3 vms ...")
        vms = []
        vms.append(VM(cm_name='gregor1'))
        vms.append(VM(cm_name='gregor2'))

        print ("Add vms ...")
        cm.add(vms)
        print ("Save vms ...")
        cm.save()
        print ("saving ok")

        try:
            vms = [VM(cm_name='gregor1')]
            cm.add([VM(cm_name='gregor1')])
            cm.save()
            assert False
        except:
            cm.session.rollback()
            print ("adding a vm with existing name failed. ok")
            assert True

        cm.save()
        print("UUUUU")

        found1 = 0
        found2 = 0
        for v in cm.data.query(VM):
            print (v.cm_name, v.cm_uuid)
            if v.cm_name == "gregor1":
                found1 = found1 + 1
            if v.cm_name == "gregor2":
                found2 = found2 + 1

        print ("found", found1, found2)
        assert found1 == 1 and found2 == 1

    def test_003(self):
        """003: finding a specific vm"""
        HEADING()
        cm = self.cm

        name = "gregor1"
        cursor = cm.find(VM, name="gregor1")
        for vm in cursor:
            print (vm.name, vm.id, vm.cloud)
        assert True

    def test_004(self):
        """004: finding a specific vm"""
        HEADING()
        cm = self.cm

        cursor = cm.find_vm_by_name(name="gregor1")
        print (cursor is not None)
        cursor = cm.find_vm_by_name(name="doesnotexist")
        assert cursor is None

    def test_005(self):
        """005: delete vms"""
        HEADING()
        cm = self.cm

        cm.delete_all()
        r = cm.info("count")
        pprint(r)
        assert r['sum'] == 0


    def test_006(self):
        """006: replacing objects in the database
        """
        HEADING()
        cm = self.cm

        for erase_type in [True, False]:
            print ("Erase Type", erase_type)
            cm.delete_all("VM")

            vm = VM(cm_name='gregor1')
            vm.cloud = "india"
            cm.add([vm])
            cm.save()

            vm = VM(cm_name='gregor1')
            vm.group = "hallo"
            cm.replace(VM, [vm], erase=erase_type)
            cm.save()

            found_vm = None
            found1 = 0
            for v in cm.data.query(VM):
                if v.cm_name == "gregor1":
                    found1 = found1 + 1
                    found_vm = v

            print ("found", found1)
            print (v.cm_name, v.group, v.cloud)
            assert found1 == 1 and v.group == "hallo"
            if erase_type:
                assert v.cloud is None
            else:
                assert v.cloud == "india"

    def test_007(self):
        """007: update the db info"""
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



    def test_008(self):
        """008: boot a vom"""
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

    def test_009(self):
        """009: flatten"""
        HEADING()
        cm = self.cm

    def test_010(self):
        """010: add"""
        HEADING()
        cm = self.cm

        vm1 = VM('gregor1')
        d = {"invalid":"noting",
             "label": "mylabel"}



    def test_011(self):
        """011: hostlist"""
        HEADING()

        from cloudmesh_base.hostlist import Parameter
        parameter = "india[01-03]"
        result = Parameter.expand(parameter)
        print (result)
        assert str(result) == "['india01', 'india02', 'india03']"

    def test_012(self):
        """012: dictupdate"""
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

    def  test_013(self):
        """013: datadict update"""
        HEADING()

        cm = self.cm
        cm.update("flavor", "india")

        elements = cm.find("flavor", cm_cloud='india', name='m1.small_e30').all()
        #for element in elements:
        #    d = cm.o_to_d(element)
        #    print (d)

        cloud = OpenStack_libcloud("india", cm_user="gvonlasz")

        result = cloud.list("flavor", output="flat")
        f = result["1"]
        f["label"] = "newlabel"
        f["cm_type"] = "flavor"
        f["cm_id"] = cm.getID("flavor", "1", "india")

        # print("libcloud", f)


        cm.update_from_dict(f)
        cm.save()


        element = cm.find('flavor',id="1").first()
        d = cm.o_to_d(element)
        # print("RRRR", d['label'], d['name'])

        assert d['label'] == "newlabel"

    def  test_014(self):
        """013: testing default get and set"""
        HEADING()

        cm = self.cm

        msg = "in global"
        cm.default("gregor", msg)
        value = cm.get_default("gregor")

        print (value)

        assert value == msg

        msg = "in cloud"
        cm.default("gregor", msg, cloud="india")
        value = cm.get_default("gregor", cloud="india")
        print (value)

        assert value == msg
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




