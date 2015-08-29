from __future__ import print_function

from cloudmesh_client.common.ConfigDict import Config
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import json
from pprint import pprint

class MyMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__= {'always_refresh': True}

    id =  Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    label = Column(String, default="undefined")
    cloud = Column(String, default="undefined")
    cloud_id = Column(String, default="undefined")

class database(object):
    """
    A simple class with all the details to create and
    provide some elementary methods for the database.

    This class is a state sharing class also known as Borg Pattern.
    Thus, multiple instantiations will share the same sate.

    TODO: An import to the model.py will instantiate the db object.
    """
    __monostate = None

    def __init__(self):
        """Initializes the database and shares the state with other instantiations of it"""
        if not database.__monostate:
            database.__monostate = self.__dict__
            self.activate()

        else:
            self.__dict__ = database.__monostate

    def activate(self):
        """activates the shared variables"""
        self.debug = False

        # engine = create_engine('sqlite:////tmp/test.db', echo=debug)

        self.filename = Config.path_expand("~/.cloudmesh/cloudmesh.db")
        self.endpoint = 'sqlite:///{:}'.format(self.filename)
        self.engine = create_engine(self.endpoint)
        self.Base = declarative_base(bind=self.engine)

        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)
        # self.session = sessionmaker(bind=self.engine)

db = database()

class User(MyMixin, db.Base):
    name = Column(String)

class Default(MyMixin, db.Base):
    name = Column(String)
    value = Column(String)



db.Base.metadata.create_all()

Session = sessionmaker(bind=db.engine)
session = Session()

def setid(o):
    o.label = "{}-{}-{}".format(o.__tablename__, o.name, o.id)
    o.classname = o.__tablename__

def add(o):
    session.add(o)
    session.commit()
    setid(o)
    session.flush()


m = User()

m.name = "gregor"
m.newfield = "P"
add(m)


n = session.query(User).filter_by(name='gregor').first()

print ("\n\n")

pprint (n.__dict__)

d = Default()

d.name  = "image"
d.value = "no image found"
add(d)

c = Default()

c.name  = "cloud"
c.value = "india"
add(c)


for n in session.query(Default).filter_by(name='image').all():
    print ("------\n")
    pprint (n.__dict__)


for n in session.query(Default).all():
    print ("------\n")
    pprint (n.__dict__)


#session.query(MyModel).filter(name=name).first()

