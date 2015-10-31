from __future__ import print_function
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy import update, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect
from prettytable import PrettyTable
from cloudmesh_client.common.Printer import dict_printer
import uuid
import os
import getpass
import json
from pprint import pprint
import sys

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_base.util import banner
# from cloudmesh_client.iaas.openstack_libcloud import OpenStack_libcloud


class database(object):
    """
    A simple class with all the details to create and
    provide some elementary methods for the database.

    This class is a state sharing class also known as Borg Pattern.
    Thus, multiple instantiations will share the same sate.

    An import to the model.py will instantiate the db object.
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

    @classmethod
    def get_table_from_name(cls, name):
        """based on the name of the table it returns the table class"""
        name_lower = name.lower()
        table = None
        if name_lower == "vm":
            table = VM
        elif name_lower == "default":
            table = DEFAULT
        elif name_lower == "image":
            table = IMAGE
        elif name_lower == "flavor":
            table = FLAVOR
        elif name_lower == "group":
            table = FLAVOR
        elif name_lower == "key":
            table = KEY
        return table


db = database()


def set_cm_data(table,
                cm_name=None,
                label=None,
                cloud='india',
                cm_user=None):
    """This method is used to initialize an object from a table. This includes

    ::

        cm_type   - vm, flavor, image, default, same as __tablename__
        cm_name   - a name/id to identify the object (it is comming typically from the source)
        label     - a label
        cm_user   - the user that uses this object
        cm_uuid   - a uuid
        cm_id     - a unique human readable id based on the cm_type,
                    tye_user_cloud_name
        cloud     - name of the cloud

        todo: cm_update
    """
    table.cm_type = table.__tablename__
    table.cm_name = cm_name
    table.cm_cloud = cloud
    table.label = label
    if cm_user is None:
        table.cm_user = getpass.getuser()
    else:
        table.cm_user = cm_user
    table.cm_uuid = str(uuid.uuid4())
    table.cm_id = "{:}_{:}_{:}_{:}".format(table.__tablename__, table.cm_user, cloud, cm_name)


class KEY(db.Base):
    """table to stor defualt values

    if the cloud is "global" it is ment to be a global variable

    todo: check if its global or general
    """
    __tablename__ = 'key'
    id = Column(Integer)

    cm_name = Column(String)
    cm_uuid = Column(String)
    cm_cloud = Column(String)
    cm_update = Column(String)
    cm_user = Column(String)
    cm_id = Column(String, primary_key=True)
    cm_type = Column(String)
    cm_command = Column(String)  # TODO what is this for
    cm_parameter = Column(String) # TODO what is this for

    default = Column(String, default='False')
    name = Column(String)
    value = Column(String)
    fingerprint = Column(String)
    source = Column(String)    
    comment = Column(String)
    label = Column(String)
    uri = Column(String)    
    
    def __init__(self,
                 cm_name=None,
                 label=None,
                 cloud='india',
                 cm_user=None):
        print ("ADD {:} {:} {:} {:}".format(cm_name, label, cloud, cm_user))
        set_cm_data(self,
                    cm_name=cm_name,
                    label=label,
                    cloud=cloud,
                    cm_user=cm_user)


class GROUP(db.Base):
    """table to stor defualt values

    if the cloud is "global" it is ment to be a global variable

    todo: check if its global or general
    """
    __tablename__ = 'group'
    id = Column(Integer)

    cm_name = Column(String)
    cm_uuid = Column(String)
    cm_cloud = Column(String) # not used in group
    cm_update = Column(String)
    cm_user = Column(String)
    cm_id = Column(String, primary_key=True)
    cm_type = Column(String)
    cm_command = Column(String) # TODO not used
    cm_parameter = Column(String) # TODO not used

    type = Column(String)
    name = Column(String)

    def __init__(self,
                 cm_name=None,
                 label=None,
                 cloud='india',
                 cm_user=None,
                 value=None):
        set_cm_data(self,
                    cm_name=cm_name,
                    label=label,
                    cloud=cloud,
                    cm_user=cm_user)
        self.value = value


class DEFAULT(db.Base):
    """table to stor defualt values

    if the cloud is "global" it is ment to be a global variable

    todo: check if its global or general
    """
    __tablename__ = 'default'
    id = Column(Integer)

    cm_name = Column(String)
    cm_uuid = Column(String)
    cm_cloud = Column(String)
    cm_update = Column(String)
    cm_user = Column(String)
    cm_id = Column(String, primary_key=True)
    cm_type = Column(String)
    cm_command = Column(String)   # TODO what is this for
    cm_parameter = Column(String) # TODO what is this for

    name = Column(String)
    value = Column(String)
    user = Column(String)
    cloud = Column(String)

    def __init__(self,
                 cm_name=None,
                 label=None,
                 cloud='india',
                 cm_user=None,
                 value=None):
        set_cm_data(self,
                    cm_name=cm_name,
                    label=label,
                    cloud=cloud,
                    cm_user=cm_user)
        self.value = value


class IMAGE(db.Base):
    """
    image of clouds
    """
    __tablename__ = 'image'
    id = Column(Integer)

    cm_id = Column(String, primary_key=True)
    cm_cloud = Column(String)
    cm_update = Column(String)
    cm_uuid = Column(String)
    cm_user = Column(String)
    cm_type = Column(String)
    cm_name = Column(String)

    name = Column(String)
    label = Column(String)
    group = Column(String)
    cloud = Column(String)
    cloud_uuid = Column(String)
    created = Column(String)
    base_image_ref = Column(String)
    description = Column(String)
    image_location = Column(String)
    image_state = Column(String)
    image_type = Column(String)
    instance_type_ephemeral_gb = Column(String)
    instance_type_flavorid = Column(String)
    instance_type_id = Column(String)
    instance_type_memory_mb = Column(String)
    instance_type_name = Column(String)
    instance_type_root_gb = Column(String)
    instance_type_rxtx_factor = Column(String)
    instance_type_swap = Column(String)
    instance_type_vcpus = Column(String)
    instance_uuid = Column(String)
    kernel_id = Column(String)
    network_allocated = Column(String)
    owner_id = Column(String)
    ramdisk_id = Column(String)
    user_id = Column(String)
    minDisk = Column(Integer)
    minRam = Column(Integer)
    progress = Column(Integer)
    serverId = Column(String)
    status = Column(String)
    updated = Column(String)
    # id = Column(String)
    # name = Column(String)

    def __init__(self,
                 cm_name=None,
                 label=None,
                 cloud='india',
                 cm_user=None):
        set_cm_data(self,
                    cm_name=cm_name,
                    label=label,
                    cloud=cloud,
                    cm_user=cm_user)


class FLAVOR(db.Base):
    """
    flavors and sizes of clouds
    """
    __tablename__ = 'flavor'

    cm_uuid = Column(String)
    cm_id = Column(String, primary_key=True)
    cm_cloud = Column(String)
    cm_update = Column(String)
    cm_user = Column(String)
    cm_type = Column(String)
    cm_name = Column(String)

    id = Column(Integer)
    name = Column(String)
    label = Column(String)
    group = Column(String)
    cloud = Column(String)
    uuid = Column(String)
    bandwidth = Column(String)
    update = Column(String)
    disk = Column(String)
    internal_id = Column(String)
    price = Column(String)
    ram = Column(String)
    vcpus = Column(String)
    ephemeral_disk = Column(Integer)
    # extra = Column(String)

    def __init__(self,
                 cm_name=None,
                 label=None,
                 cloud='india',
                 cm_user=None):
        set_cm_data(self,
                    cm_name=cm_name,
                    label=label,
                    cloud=cloud,
                    cm_user=cm_user)


class VM(db.Base):
    """
    virtual machines of clouds
    """
    __tablename__ = 'vm'
    id = Column(Integer)

    cm_cloud = Column(String)
    cm_id = Column(String, primary_key=True)
    cm_update = Column(String)
    cm_user = Column(String)
    cm_uuid = Column(String)
    cm_type = Column(String)
    cm_name = Column(String)

    # private_ips [10.23.1.35],
    # public_ips [149.165.158.100],
    # volumes_attached []
    access_ip = Column(String)
    access_ipv6 = Column(String)
    availability_zone = Column(String)
    cloud = Column(String)

    config_drive = Column(String)
    created = Column(String)
    disk_config = Column(String)
    flavor = Column(String)
    flavorId = Column(Integer)
    group = Column(String)
    hostId = Column(String)
    image = Column(String)
    imageId = Column(String)
    key_name = Column(String)
    label = Column(String)
    meta = Column(String)
    name = Column(String)
    networks = Column(String)
    password = Column(String)
    power_state = Column(Integer)
    progress = Column(Integer)
    size = Column(Integer)
    state = Column(Integer)
    status = Column(String)
    task_state = Column(String)
    tenantId = Column(String)
    updated = Column(String)
    uri = Column(String)
    user = Column(String)
    userId = Column(String)
    uuid = Column(String)
    vm_state = Column(String)

    def __init__(self,
                 cm_name=None,
                 label=None,
                 cloud='india',
                 cm_user=None):
        set_cm_data(self,
                    cm_name=cm_name,
                    label=label,
                    cloud=cloud,
                    cm_user=cm_user)
