from __future__ import print_function

import os
from datetime import datetime

from cloudmesh_client.common.ConfigDict import Config
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, String, MetaData, \
    create_engine
from sqlalchemy.ext.declarative import declarative_base


# noinspection PyPep8Naming
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

        self.filename = Config.path_expand(
            os.path.join("~", ".cloudmesh", "cloudmesh.db"))
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
    created_at = Column(String,
                        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = Column(String,
                        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    label = Column(String, default="undefined")
    name = Column(String, default="undefined")
    cloud = Column(String, default="undefined")
    user = Column(String, default="undefined")
    kind = Column(String, default="undefined")
    project = Column(String, default="undefined")


class IMAGE(CloudmeshMixin, db.Base):
    uuid = Column(String)
    status = Column(String)
    updated = Column(String)
    created = Column(String)
    minDisk = Column(String)
    progress = Column(String)
    minRam = Column(String)
    os_image_size = Column(String)  # This is OS-EXT-IMG-SIZE:size
    # metadata info..
    metadata__base_image_ref = Column(String)
    metadata__description = Column(String)
    metadata__image_location = Column(String)
    metadata__image_state = Column(String)
    metadata__image_type = Column(String)
    metadata__instance_type_ephemeral_gb = Column(String)
    metadata__instance_type_flavorid = Column(String)
    metadata__instance_type_id = Column(String)
    metadata__instance_type_memory_mb = Column(String)
    metadata__instance_type_name = Column(String)
    metadata__instance_type_root_gb = Column(String)
    metadata__instance_type_rxtx_factor = Column(String)
    metadata__instance_type_swap = Column(String)
    metadata__instance_type_vcpus = Column(String)
    metadata__instance_uuid = Column(String)
    metadata__kernel_id = Column(String)
    metadata__network_allocated = Column(String)
    metadata__owner_id = Column(String)
    metadata__ramdisk_id = Column(String)
    metadata__user_id = Column(String)

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
        self.status = kwargs.get('status')
        self.updated = kwargs.get('updated')
        self.created = kwargs.get('created')
        self.minDisk = kwargs.get('minDisk')
        self.progress = kwargs.get('progress')
        self.minRam = kwargs.get('minRam')
        self.os_image_size = kwargs.get('OS-EXT-IMG-SIZE:size')
        self.metadata__base_image_ref = kwargs.get('metadata__base_image_ref')
        self.metadata__description = kwargs.get('metadata__description')
        self.metadata__image_location = kwargs.get('metadata__image_location')
        self.metadata__image_state = kwargs.get('metadata__image_state')
        self.metadata__image_type = kwargs.get('metadata__image_type')
        self.metadata__instance_type_ephemeral_gb = kwargs.get(
            'metadata__instance_type_ephemeral_gb')
        self.metadata__instance_type_flavorid = kwargs.get(
            'metadata__instance_type_flavorid')
        self.metadata__instance_type_id = kwargs.get(
            'metadata__instance_type_id')
        self.metadata__instance_type_memory_mb = kwargs.get(
            'metadata__instance_type_memory_mb')
        self.metadata__instance_type_name = kwargs.get(
            'metadata__instance_type_name')
        self.metadata__instance_type_root_gb = kwargs.get(
            'metadata__instance_type_root_gb')
        self.metadata__instance_type_rxtx_factor = kwargs.get(
            'metadata__instance_type_rxtx_factor')
        self.metadata__instance_type_swap = kwargs.get(
            'metadata__instance_type_swap')
        self.metadata__instance_type_vcpus = kwargs.get(
            'metadata__instance_type_vcpus')
        self.metadata__instance_uuid = kwargs.get('metadata__instance_uuid')
        self.metadata__kernel_id = kwargs.get('metadata__kernel_id')
        self.metadata__network_allocated = kwargs.get(
            'metadata__network_allocated')
        self.metadata__owner_id = kwargs.get('metadata__owner_id')
        self.metadata__ramdisk_id = kwargs.get('metadata__ramdisk_id')
        self.metadata__user_id = kwargs.get('metadata__user_id')

        """if kwargs is not None:
            for key, value in kwargs.iteritems():
                print ("{} = {}".format(key, value))
                self[key] = value"""


class FLAVOR(CloudmeshMixin, db.Base):
    uuid = Column(String)
    ram = Column(String)
    os_flv_disabled = Column(String)
    vcpus = Column(String)
    swap = Column(String)
    os_flavor_acces = Column(String)
    rxtx_factor = Column(String)
    os_flv_ext_data = Column(String)
    disk = Column(String)

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
        self.ram = kwargs.get('ram')
        self.os_flv_disabled = kwargs.get('OS-FLV-DISABLED:disabled')
        self.vcpus = kwargs.get('vcpus')
        self.swap = kwargs.get('swap')
        self.os_flavor_acces = kwargs.get('os-flavor-access:is_public')
        self.rxtx_factor = kwargs.get('rxtx_factor')
        self.os_flv_ext_data = kwargs.get('OS-FLV-EXT-DATA:ephemeral')
        self.disk = kwargs.get('disk')
        self.kind = self.__tablename__

        """if kwargs is not None:
            for key, value in kwargs.iteritems():
                print ("{} = {}".format(key, value))
                self[key] = value"""


class VM(CloudmeshMixin, db.Base):
    uuid = Column(String)
    diskConfig = Column(String)
    availability_zone = Column(String)
    power_state = Column(String)
    task_state = Column(String)
    vm_state = Column(String)
    launched_at = Column(String)
    terminated_at = Column(String)
    accessIPv4 = Column(String)
    accessIPv6 = Column(String)
    static_ip = Column(String)
    floating_ip = Column(String)
    config_drive = Column(String)
    created = Column(String)
    flavor__id = Column(String)
    hostId = Column(String)
    image__id = Column(String)
    key_name = Column(String)
    name = Column(String)
    volumes_attached = Column(String)
    progress = Column(String)
    security_groups = Column(String)
    status = Column(String)
    tenant_id = Column(String)
    updated = Column(String)
    user_id = Column(String)

    def __init__(self, **kwargs):
        # self.kind = __tablename__
        self.label = kwargs["name"]
        self.cloud = kwargs["cloud"] or "general"
        self.type = kwargs["type"]
        self.name = kwargs["name"]
        self.user = kwargs["user"]
        self.uuid = kwargs["uuid"]

        self.diskConfig = kwargs["OS-DCF:diskConfig"]
        self.availability_zone = kwargs["OS-EXT-AZ:availability_zone"]
        self.power_state = kwargs["OS-EXT-STS:power_state"]
        self.task_state = kwargs["OS-EXT-STS:task_state"]
        self.vm_state = kwargs["OS-EXT-STS:vm_state"]
        self.launched_at = kwargs["OS-SRV-USG:launched_at"]
        self.terminated_at = kwargs["OS-SRV-USG:terminated_at"]
        self.accessIPv4 = kwargs["accessIPv4"]
        self.accessIPv6 = kwargs["accessIPv6"]
        self.static_ip = kwargs["static_ip"]
        self.floating_ip = kwargs["floating_ip"]
        self.config_drive = kwargs["config_drive"]
        self.created = kwargs["created"]
        self.flavor__id = kwargs["flavor__id"]
        self.hostId = kwargs["hostId"]
        self.image__id = kwargs["image__id"]
        self.key_name = kwargs["key_name"]
        self.name = kwargs["name"]
        # self.volumes_attached = kwargs["volumes_attached"] or None
        # self.progress = kwargs["progress"]

        # Expects a comma separated string list of security groups.
        self.security_groups = kwargs["security_ groups"]

        self.status = kwargs["status"]
        self.tenant_id = kwargs["tenant_id"]
        self.updated = kwargs["updated"]
        self.user_id = kwargs["user_id"]

        self.kind = self.__tablename__

        """
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                print ("{} = {}".format(key, value))
                self[key] = value
        """


class VMUSERMAP(CloudmeshMixin, db.Base):
    """
    Table to store mapping of VM and login username.
    """
    vm_uuid = Column(String, primary_key=True)
    username = Column(String)

    def __init__(self, **kwargs):
        self.id = kwargs["vm_uuid"]
        self.vm_uuid = kwargs["vm_uuid"]
        self.username = kwargs["username"]
        self.kind = self.__tablename__


class COUNTER(CloudmeshMixin, db.Base):
    """
    Table to store Prefix Count for VM auto-naming.
    """
    type = Column(String, default="integer")
    value = Column(Integer)

    def __init__(self,
                 name,
                 value,
                 type="string",
                 user=None):
        # self.kind = __tablename__
        self.label = name
        self.type = type
        self.name = name
        self.user = user
        self.value = value
        self.kind = self.__tablename__


# OLD: TODO delete this when done
#
#    def __init__(self, **kwargs):
#        self.id = kwargs["prefix"]
#        self.prefix = kwargs["prefix"]
#        self.count = kwargs["count"]
#        self.kind = self.__tablename__


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


class LAUNCHER(CloudmeshMixin, db.Base):
    """table to store default values

    if the cloud is "global" it is meant to be a global variable

    todo: check if its global or general
    """
    # name defined in mixin
    value = Column(String)
    type = Column(String, default="string")
    parameters = Column(String)  # This is the parameter represented as yaml object

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
    is_default = Column(String)

    def __init__(self,
                 name,
                 value,
                 uri=None,
                 source=None,
                 fingerprint=None,
                 comment=None,
                 type="string",
                 cloud=None,
                 user=None,
                 is_default="False"):
        # self.kind = __tablename__
        self.value = value
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
        self.is_default = is_default


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

    def __init__(self, **kwargs):
        # self.kind = __tablename__
        self.label = kwargs['name']
        self.hosts = kwargs['hosts']
        self.cloud = kwargs['cloud'] or "comet"
        self.start_time = kwargs['start']
        self.end_time = kwargs['end']
        self.description = kwargs['description']
        self.name = kwargs['name']
        self.user = kwargs['user']
        self.project = kwargs['project']
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
                print("{} = {}".format(key, value))
                self[key] = value


class SECGROUPRULE(CloudmeshMixin, db.Base):
    groupid = Column(String)
    fromPort = Column(String)
    toPort = Column(String)
    protocol = Column(String)
    cidr = Column(String)
    uuid = Column(String)

    # noinspection PyPep8Naming
    def __init__(self,
                 uuid,
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
        self.uuid = uuid
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
                print("{} = {}".format(key, value))
                self[key] = value


class BATCHJOB(CloudmeshMixin, db.Base):
    """table to store default values

    if the cloud is "global" it is meant to be a global variable

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

    # cloud = Column(String)

    def __init__(self,
                 name,
                 type="string",
                 user=None,
                 **kwargs
                 ):
        self.label = name
        self.type = type
        self.name = name
        self.user = user

        self.dir = kwargs.get('dir')
        self.nodes = kwargs.get('nodes')
        self.output_file = kwargs.get('output_file')
        self.queue = kwargs.get('queue')
        self.time = kwargs.get('time')
        self.cluster = kwargs.get('cluster')
        self.sbatch_file_path = kwargs.get('sbatch_file_path')
        self.cmd = kwargs.get('cmd')
        self.time = kwargs.get('time')
        self.kind = self.__tablename__

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

    raise ("ERROR: unkown table {}".format(name))


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
