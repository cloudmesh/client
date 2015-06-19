from cloudmesh_client import cloudmesh_db
from cloudmesh_client.common import dict_printer
from pprint import pprint
import getpass

cm = cloudmesh_db.CloudmeshDatabase()

# create instances of my user object
vms = []
vms.append(cloudmesh_db.VM('gregor1'))
vms.append(cloudmesh_db.VM('gregor2'))

cm.add(vms)
cm.save()

# When you query the data back it returns instances of your class:

for v in cm.data.query(cloudmesh_db.VM):
    print (v.name, v.label, v.uuid, v.id)

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

cm.name("gregor-001")
print (cm.get_name())

cm.name("gregor-002")
print (cm.get_name())
print (cm.next_name())




