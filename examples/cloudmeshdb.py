import cloudmesh_db
from cloudmesh_common.tables import dict_printer
from pprint import pprint
import getpass

database = cloudmesh_db.CloudmeshDatabase()

# create instances of my user object
vms = []
vms.append(cloudmesh_db.VM('gregor1'))
vms.append(cloudmesh_db.VM('gregor2'))

database.add(vms)
database.save()

# When you query the data back it returns instances of your class:

for v in database.data.query(cloudmesh_db.VM):
    print (v.name, v.label, v.uuid, v.id)

pprint(database.dict(cloudmesh_db.VM))
pprint(database.json(cloudmesh_db.VM))

for output in ["dict", "json", "yaml", "table"]:
    print (dict_printer(database.dict(cloudmesh_db.VM), output=output))

# d = [DEFAULT(name="user", value="albert")]
# db.add(d)
# db.save()

database.default("cloud", "india")
database.default("user", getpass.getuser())

for v in database.data.query(cloudmesh_db.DEFAULT):
    print (v.name, v.value)

print (dict_printer(database.dict(cloudmesh_db.DEFAULT), output='yaml'))

print (dict_printer(database.dict(cloudmesh_db.DEFAULT),
                    order=['id', 'name', 'value']))

#                    ,
#                    header=['Name', 'Value']))

