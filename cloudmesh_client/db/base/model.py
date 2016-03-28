from __future__ import print_function

import os
from datetime import datetime

from sqlalchemy import Column, Integer, String, MetaData, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict

from ..db import database


db = database()

"""

kind = the general type of the object that can be helpful for the location
       of similar objects accross providers

        examples: vm, image, flavor, ...

type = the table name of the object

provider name of the providor

            example: "openstack", "libcloud", "aws", ...


category = name of the category, this can be the name of the clod,
            batch system or other
            from the name of the category other information can be derived
            while retrieving it from the yaml file

            examples: kilo, chameleon, cybera-e, aws, ...
                      e..g. the names of the clouds

please note that kind and type seem to be confusingly named as the kind is used in

"""


class CloudmeshMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    # __table_args__ = {'mysql_engine': 'InnoDB'}
    __mapper_args__ = {'always_refresh': True}

    id = Column(Integer, primary_key=True)
    # created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    created_at = Column(String,
                        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = Column(String,
                        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    label = Column(String, default="undefined")
    name = Column(String, default="undefined")
    user = Column(String, default=db.user)
    project = Column(String, default="undefined")

    category = Column(String, default="undefined")  # general or the name of teh cloud/queue in the yaml files
    kind = Column(String, default="undefined")
    type = Column(String, default="undefined")
    provider = Column(String, default="undefined")


class COUNTER(CloudmeshMixin, db.Base):
    """
    Table to store Prefix Count for VM auto-naming.
    """
    value = Column(Integer)
    kind = "counter"

    def __init__(self,
                 name,
                 value,
                 user=None):

        self.label = name
        self.name = name
        if user is None:
            self.user = db.user
        else:
            self.user = user
        self.value = value
        self.type = self.__tablename__


# OLD: TODO delete this when done
#
#    def __init__(self, **kwargs):
#        self.id = kwargs["prefix"]
#        self.prefix = kwargs["prefix"]
#        self.count = kwargs["count"]
#        self.kind = self.__tablename__


class DEFAULT(CloudmeshMixin, db.Base):
    """table to store default values

    if the category is "global" it is meant to be a global variable

    todo: check if its global or general
    """
    # name defined in mixin
    value = Column(String)
    type = Column(String, default="string")
    kind = 'default'

    # category = Column(String)

    def __init__(self,
                 name,
                 value,
                 category=None,
                 user=None):
        # self.kind = __tablename__
        self.label = name
        self.category = category or "general"
        self.name = name
        if user is None:
            self.user = db.user
        else:
            self.user = user
        self.value = value
        self.type = self.__tablename__


class VAR(CloudmeshMixin, db.Base):
    """table to store peristant variable values
    """
    # name defined in mixin
    value = Column(String)
    type = Column(String, default="string")
    kind = 'var'

    def __init__(self,
                 name,
                 value,
                 category="var",
                 user=None):

        self.label = name
        self.category = category or "var"
        self.name = name
        if user is None:
            self.user = db.user
        else:
            self.user = user
        self.value = value
        self.type = self.__tablename__


class LAUNCHER(CloudmeshMixin, db.Base):
    """table to store default values

    if the category is "global" it is meant to be a global variable

    todo: check if its global or general
    """
    # name defined in mixin
    value = Column(String)
    type = Column(String, default="string")
    parameters = Column(String)  # This is the parameter represented as yaml object
    kind = 'launcher'

    def __init__(self,
                 name,
                 value,
                 category=None,
                 user=None):

        self.label = name
        self.category = category or "general"
        self.name = name
        if user is None:
            self.user = db.user
        else:
            self.user = user
        self.value = value
        self.type = self.__tablename__


# TODO: BUG the value is not properly used here
class KEY(CloudmeshMixin, db.Base):
    value = Column(String)
    fingerprint = Column(String, unique=True)
    source = Column(String)
    comment = Column(String)
    uri = Column(String)
    is_default = Column(String)
    kind = 'key'

    def __init__(self,
                 name,
                 value,
                 uri=None,
                 source=None,
                 fingerprint=None,
                 comment=None,
                 category=None,
                 user=None,
                 is_default="False"):

        self.value = value
        self.label = name
        self.category = category or "general"
        self.uri = uri
        self.comment = comment
        self.fingerprint = fingerprint
        self.source = source
        self.name = name
        if user is None:
            self.user = db.user
        else:
            self.user = user
        self.type = self.__tablename__
        self.is_default = is_default


class GROUP(CloudmeshMixin, db.Base):
    member = Column(String)
    species = Column(String)
    kind = 'group'

    def __init__(self,
                 name,
                 member,
                 species=None,
                 category=None,
                 user=None):

        self.label = name
        self.category = category or "general"
        self.species = species or "vm"
        self.name = name
        self.member = member
        if user is None:
            self.user = db.user
        else:
            self.user = user
        self.type = self.__tablename__


class RESERVATION(CloudmeshMixin, db.Base):
    hosts = Column(String)  # should be list of strings
    description = Column(String)
    start_time = Column(String)  # date, time
    end_time = Column(String)  # date, time
    type = Column(String)
    kind = "reservation"

    def __init__(self, **kwargs):

        self.label = kwargs['name']
        self.hosts = kwargs['hosts']
        if 'category' in kwargs:
            self.category = kwargs['category'] or "general"
        else:
            self.category = 'general'
        self.start_time = kwargs['start']
        self.end_time = kwargs['end']
        self.description = kwargs['description']
        self.name = kwargs['name']
        if kwargs['user'] is None:
            self.user = db.user
        else:
            self.user = kwargs['user']
        self.project = kwargs['project']
        self.type = self.__tablename__


class SECGROUP(CloudmeshMixin, db.Base):
    uuid = Column(String)
    kind = 'secgroup'

    def __init__(self,
                 name,
                 uuid,
                 category=None,
                 user=None,
                 project=None,
                 **kwargs):

        self.label = name
        self.category = category or "general"
        self.name = name
        if user is None:
            self.user = db.user
        else:
            self.user = user
        self.uuid = uuid
        self.project = project
        self.type = self.__tablename__

        if kwargs is not None:
            for key, value in kwargs.items():
                # print("{} = {}".format(key, value))
                self[key] = value


class SECGROUPRULE(CloudmeshMixin, db.Base):
    groupid = Column(String)
    fromPort = Column(String)
    toPort = Column(String)
    protocol = Column(String)
    cidr = Column(String)
    uuid = Column(String)
    kind = "secgrouprule"

    # noinspection PyPep8Naming
    def __init__(self,
                 uuid,
                 name,
                 groupid,
                 category=None,
                 user=None,
                 project=None,
                 fromPort=None,
                 toPort=None,
                 protocol=None,
                 cidr=None,
                 **kwargs):

        self.uuid = uuid
        self.label = name
        self.category = category or "general"
        self.name = name
        if user is None:
            self.user = db.user
        else:
            self.user = user
        self.groupid = groupid
        self.project = project
        self.fromPort = fromPort
        self.toPort = toPort
        self.protocol = protocol
        self.cidr = cidr
        self.type = self.__tablename__

        if kwargs is not None:
            for key, value in kwargs.items():
                # print("{} = {}".format(key, value))
                self[key] = value


class BATCHJOB(CloudmeshMixin, db.Base):
    """table to store default values

    if the category is "global" it is meant to be a global variable

    todo: check if its global or general
    """
    # name defined in mixin
    type = Column(String, default="string")
    dir = Column(String, default="string")
    nodes = Column(String, default="string")
    output_file = Column(String, default="string")
    queue = Column(String, default="string")
    time = Column(String, default="string")
    cluster = Column(String, default="string")
    sbatch_file_path = Column(String, default="string")
    cmd = Column(String, default="string")
    # noinspection PyRedeclaration
    time = Column(String, default="string")
    group = Column(String, default="string")
    job_id = Column(String, default="string")
    category = Column(String, default="string")
    kind = 'batchjob'

    def __init__(self,
                 name,
                 user=None,
                 category=None,
                 **kwargs
                 ):
        self.provider = "slurm"
        self.label = name
        self.name = name
        if user is None:
            self.user = db.user
        else:
            self.user = user
        self.type = 'batchjob'
        self.dir = kwargs.get('dir')
        self.nodes = kwargs.get('nodes')
        self.output_file = kwargs.get('output_file')
        self.queue = kwargs.get('queue')
        self.time = kwargs.get('time')
        self.cluster = kwargs.get('cluster')
        self.sbatch_file_path = kwargs.get('sbatch_file_path')
        self.cmd = kwargs.get('cmd')
        self.time = kwargs.get('time')
        self.group = kwargs.get('group')
        self.job_id = kwargs.get('job_id')
        self.type = self.__tablename__
        self.category = category or "general"


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
c.value = "kilo"
add(c)


for n in session.query(Default).filter_by(name='image').all():
    print ("------\n")
    pprint (n.__dict__)


for n in session.query(Default).all():
    print ("------\n")
    pprint (n.__dict__)


#session.query(MyModel).filter(name=name).first()
"""
