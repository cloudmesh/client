from __future__ import print_function

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

        self.filename = Config.path_expand("~/.cloudmesh/cloudmesh.db")
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
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    label = Column(String, default="undefined")
    name = Column(String, default="undefined")
    cloud = Column(String, default="undefined")
    user = Column(String, default="undefined")
    kind = Column(String, default="undefined")


class DEFAULT(CloudmeshMixin, db.Base):
    """table to store defualt values

    if the cloud is "global" it is ment to be a global variable

    todo: check if its global or general
    """
    # name defined in mixin
    value = Column(String)
    type = Column(String, default="string")

    cloud = Column(String)

    def __init__(self,
                 name,
                 value,
                 type="string",
                 cloud=None,
                 user=None):
        # self.kind = __tablename__
        self.label = name
        if cloud is None:
            cloud = "general"
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
    fingerprint = Column(String)
    source = Column(String)
    comment = Column(String)
    uri = Column(String)

    def __init__(self,
                 name,
                 cloud=None,
                 user=None):
        # self.kind = __tablename__
        self.label = name
        self.cloud = cloud or "general"
        self.name = name
        self.user = user
        self.kind = self.__tablename__

    def add(self, tablename, id, name):
        """ This adds an object to the group specifying the
        table name and the name of the object"""
        # TODO: implement
        TODO("implement")

    def get(self, name):
        """
        returns a list of all elements in that group
        """
        TODO("implement")

        """
        TODO: implement in cloud.group
                class Group

        The purpos is to store a list of objects and retrieve them
        conveniently.

        an example would be to store a number of vms in a group that we can
        than use to delete (we assume the anme of the vm is unique

        Group.add(groupname, "VM", id, name)
        Group.delete(groupname)
        Group.delete("VM", groupname)
        Group.delete("VM", cloud, groupname)
        Group.list("VM")
        Group.list("IMAGE")  note each cloud could have its own images, so the cloudname
            is in result.
        """


def tables():
    # inspector = inspect(self.db.engine)
    return [DEFAULT, KEY, GROUP]


def tablenames():
    inspector = inspect(db.engine)
    return inspector.get_table_names()


def table(name):
    if name == "default":
        return DEFAULT
    elif name == "key":
        return KEY
    elif name == "group":
        return GROUP


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
