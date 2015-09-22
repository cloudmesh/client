from __future__ import print_function

from six import iteritems
import os
from datetime import datetime

from cloudmesh_client.common.ConfigDict import Config
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, String, DateTime, MetaData, create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from cloudmesh_client.common.todo import TODO


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

        self.filename = Config.path_expand(os.path.join("~", ".cloudmesh", "cloudmesh.db"))
        self.endpoint = 'sqlite:///{:}'.format(self.filename)
        self.engine = create_engine(self.endpoint)
        self.Base = declarative_base(bind=self.engine)

        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)
        # self.session = sessionmaker(bind=self.engine)


db = database()


class CloudmeshMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__ = {'always_refresh': True}

    id = Column(Integer, primary_key=True)
    # created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    created_at = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = Column(String, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    label = Column(String, default="undefined")
    name = Column(String, default="undefined")
    cloud = Column(String, default="undefined")
    user = Column(String, default="undefined")
    kind = Column(String, default="undefined")
    project = Column(String, default="undefined")


class IMAGE(CloudmeshMixin, db.Base):

    uuid = Column(String)

    def __init__(self,
                 name,
                 uuid,
                 type="string",
                 cloud=None,
                 user=None,
                 **kwargs):
        # self.kind = __tablename__
        self.label = name
        self.cloud = cloud or "general"
        self.type = type
        self.name = name
        self.user = user
        self.uuid = uuid
        self.kind = self.__tablename__

        if kwargs is not None:
            for key, value in kwargs.iteritems():
                print ("{} = {}".format(key, value))
                self[key] = value


class FLAVOR(CloudmeshMixin, db.Base):

    uuid = Column(String)

    def __init__(self,
                 name,
                 uuid,
                 type="string",
                 cloud=None,
                 user=None,
                 **kwargs):
        # self.kind = __tablename__
        self.label = name
        self.cloud = cloud or "general"
        self.type = type
        self.name = name
        self.user = user
        self.uuid = uuid
        self.kind = self.__tablename__

        if kwargs is not None:
            for key, value in kwargs.iteritems():
                print ("{} = {}".format(key, value))
                self[key] = value


class VM(CloudmeshMixin, db.Base):

    uuid = Column(String)

    def __init__(self,
                 name,
                 uuid,
                 type="string",
                 cloud=None,
                 user=None,
                 **kwargs):
        # self.kind = __tablename__
        self.label = name
        self.cloud = cloud or "general"
        self.type = type
        self.name = name
        self.user = user
        self.uuid = uuid
        self.kind = self.__tablename__

        if kwargs is not None:
            for key, value in kwargs.iteritems():
                print ("{} = {}".format(key, value))
                self[key] = value


class DEFAULT(CloudmeshMixin, db.Base):
    """table to store default values

    if the cloud is "global" it is meant to be a global variable

    todo: check if its global or general
    """
    # name defined in mixin
    value = Column(String)
    type = Column(String, default="string")

    # cloud = Column(String)

    def __init__(self,
                 name,
                 value,
                 type="string",
                 cloud=None,
                 user=None):
        # self.kind = __tablename__
        self.label = name
        self.cloud = cloud or "general"
        self.type = type
        self.name = name
        self.user = user
        self.value = value
        self.kind = self.__tablename__


# TODO: BUG the value is not properly used here
class KEY(CloudmeshMixin, db.Base):
    value = Column(String)
    fingerprint = Column(String)
    source = Column(String)
    comment = Column(String)
    uri = Column(String)

    def __init__(self,
                 name,
                 value,
                 uri=None,
                 source=None,
                 fingerprint=None,
                 comment=None,
                 type="string",
                 cloud=None,
                 user=None):
        # self.kind = __tablename__
        self.label = name
        self.cloud = cloud or "general"
        self.uri = uri
        self.comment = comment
        self.fingerprint = fingerprint
        self.source = source
        self.type = type
        self.name = name
        self.user = user
        self.kind = self.__tablename__


class GROUP(CloudmeshMixin, db.Base):
    value = Column(String)
    type = Column(String)

    def __init__(self,
                 name,
                 value,
                 type="vm",
                 cloud=None,
                 user=None):
        # self.kind = __tablename__
        self.label = name
        self.cloud = cloud or "general"
        self.type = type
        self.name = name
        self.value = value
        self.user = user
        self.kind = self.__tablename__


class RESERVATION(CloudmeshMixin, db.Base):
    hosts = Column(String)  # should be list of strings
    description = Column(String)
    start_time = Column(String)  # date, time
    end_time = Column(String)  # date, time

    def __init__(self,
                 name,
                 hosts,
                 start_time,
                 end_time,
                 description=None,
                 cloud=None,
                 user=None,
                 project=None):
        # self.kind = __tablename__
        self.label = name
        self.cloud = cloud or "comet"
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.name = name
        self.user = user
        self.kind = self.__tablename__


class SECGROUP(CloudmeshMixin, db.Base):

    uuid = Column(String)

    def __init__(self,
                 name,
                 uuid,
                 type="string",
                 cloud=None,
                 user=None,
                 project=None,
                 **kwargs):
        # self.kind = __tablename__
        self.label = name
        self.cloud = cloud or "general"
        self.type = type
        self.name = name
        self.user = user
        self.uuid = uuid
        self.project = project
        self.kind = self.__tablename__

        if kwargs is not None:
            for key, value in kwargs.iteritems():
                print ("{} = {}".format(key, value))
                self[key] = value


class SECGROUPRULE(CloudmeshMixin, db.Base):

    groupid = Column(String)
    fromPort = Column(String)
    toPort = Column(String)
    protocol = Column(String)
    cidr = Column(String)

    def __init__(self,
                 name,
                 groupid,
                 type="string",
                 cloud=None,
                 user=None,
                 project=None,
                 fromPort=None,
                 toPort=None,
                 protocol=None,
                 cidr=None,
                 **kwargs):
        # self.kind = __tablename__
        self.label = name
        self.cloud = cloud or "general"
        self.type = type
        self.name = name
        self.user = user
        self.groupid = groupid
        self.project = project
        self.fromPort = fromPort
        self.toPort = toPort
        self.protocol = protocol
        self.cidr = cidr
        self.kind = self.__tablename__

        if kwargs is not None:
            for key, value in kwargs.iteritems():
                print ("{} = {}".format(key, value))
                self[key] = value


def tables():
    """
    :return: the list of tables in model
    """
    classes = [cls for cls in db.Base.__subclasses__()]
    return classes


def tablenames():
    """
    :return: the list of table names in model
    """
    names = [name.__tablename__ for name in tables()]
    return names


def table(name):
    """
    :return: the table class based on a given table name.
             In case the table does not exist an exception is thrown
    """
    for t in tables():
        if t.__tablename__ == name:
            return t

    raise("ERROR: unkown table {}".format(name))


"""
db.Base.metadata.create_all()

Session = sessionmaker(bind=db.engine)
session = Session()

def add(o):
    session.add(o)
    session.commit()
    session.flush()


m = DEFAULT("hallo", "world")

add(m)


n = session.query(DEFAULT).filter_by(name='hallo').first()

print ("\n\n")

pprint (n.__dict__)

"""

"""
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
"""
