
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.ConfigDict import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import cloudmesh_client.common.tables as tables
from cloudmesh_client.db.models import VM,FLAVOR,DEFAULT,IMAGE
import cloudmesh_client.db.models
import cloudmesh_client.db.models as models
from __future__ import print_function

filename = Config.path_expand("~/test/db.db")
endpoint = 'sqlite:///{:}'.format(filename)
engine = create_engine(endpoint)
Base = declarative_base(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

r = session.query(VM).all()
for obj in r:
    print (obj.name)

result = dict()
for u in r:
    _id = u.id
    values = {}
    for key in u.__dict__.keys():
        if not key.startswith("_sa"):
            values[key] = u.__dict__[key]
    result[_id] = values

output = models.dict_printer(result, order=None, header=None, output="dict", sort_keys=True)
print(output)