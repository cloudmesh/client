""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_base.util import HEADING
import cloudmesh_db
from cloudmesh_db.models import VM, DEFAULT

class Test_cloudmeshdb:
    def setup(self):
        self.cm = cloudmesh_db.CloudmeshDatabase()
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

        vms = []
        vms.append(VM('gregor1'))
        vms.append(VM('gregor2'))

        cm.add(vms)
        cm.save()

        found1 = 0
        found2 = 0
        for v in cm.data.query(VM):
            if v.name == "gregor1":
                found1 = found1 + 1
            if v.name == "gregor2":
                found2 = found2 + 1

        print ("found", found1, found2)
        assert found1 == 1 and found2 == 1

    def test_003_find(self):
        """finding a specific vm"""
        HEADING()
        cm = self.cm

        name = "gregor1"
        cursor = cm.find(VM, name="gregor1")
        for vm in cursor:
            print (vm.name, vm.id, vm.cloud)
        assert True

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




