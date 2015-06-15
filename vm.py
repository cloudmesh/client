from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from prettytable import PrettyTable
from cloudmesh_common.tables import dict_printer
import uuid
import os
import getpass
import json
from pprint import pprint

debug = False

#engine = create_engine('sqlite:////tmp/test.db', echo=debug)
engine = create_engine('sqlite://')
Base = declarative_base(bind=engine)

class DEFAULT(Base):
    __tablename__ = 'default'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
    user = Column(String)


class VM(Base):
    __tablename__ = 'vm'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    label = Column(String)
    group = Column(String)
    uuid = Column(String)
    cloud = Column(String)
    user = Column(String)

    def __init__(self,
                 name,
                 label=None,
                 group=None,
                 cloud=None,
                 user=None):

        self.name = name
        self.label = label

        if label is None:
            self.label = name
        if group is None:
            self.group = 'default'
        if user is None:
            self.user = getpass.getuser()

        self.uuid = str(uuid.uuid4())

class DB (object):

    def add(self, items):
        self.session.add_all(items)

    def __init__(self):
        Base.metadata.create_all()
        self.session = self.connect()

    def connect(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        return self.session

    def save(self):
        self.session.commit()

    def default(self, key, value):
        # find
        d = [DEFAULT(name=key, value=value)]
        current = self.session.query(DEFAULT).filter_by(name=key).first()
        if current is None:
            self.session.add_all(d)
        else:
            current.value = value
            self.save()
        self.save()

    @property
    def data(self):
        return self.session

    def dict(self, table):
        result = dict()
        for u in self.session.query(table).all():
            _id = u.id
            values = {}
            for key in u.__dict__.keys():
                if not key.startswith("_sa"):
                    values[key] = u.__dict__[key]
            result[_id] = values
        return result

    def json(self, table):
        d = self.dict(table)
        return json.dumps(d)

db = DB()

# create instances of my user object
vms = []
vms.append(VM('gregor1'))
vms.append(VM('gregor2'))

db.add(vms)
db.save()

# When you query the data back it returns instances of your class:

for v in db.data.query(VM):
    print v.name, v.label, v.uuid, v.id

pprint (db.dict(VM))
pprint (db.json(VM))

for output in ["dict", "json", "yaml", "table"]:
    print (dict_printer(db.dict(VM), output=output))



# d = [DEFAULT(name="user", value="albert")]
# db.add(d)
# db.save()

db.default("cloud", "india")
db.default("user", getpass.getuser())

for v in db.data.query(DEFAULT):
    print v.name, v.value

print (dict_printer(db.dict(DEFAULT), output='yaml'))

print (dict_printer(db.dict(DEFAULT),
                    order=['id', 'name', 'value']))

#                    ,
#                    header=['Name', 'Value']))
