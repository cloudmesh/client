from __future__ import print_function
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy import update, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect
from prettytable import PrettyTable
from cloudmesh_client.common.tables import dict_printer
import uuid
import os
import getpass
import json
from pprint import pprint
import sys
from cloudmesh_client.cloud.clouds import Cloud
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_base.util import banner
# from cloudmesh_client.iaas.openstack_libcloud import OpenStack_libcloud


class database(object):

    __monostate = None

    def __init__(self):
        if not database.__monostate:
            database.__monostate = self.__dict__
            self.activate()

        else:
            self.__dict__ = database.__monostate

    def activate(self):
        print("INIT")
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
        return table

db = database()

def set_cm_data(table,
                cm_name=None,
                label=None,
                cloud='india',
                cm_user=None):
    table.cm_type = table.__tablename__
    table.cm_name = cm_name
    table.label = label
    if cm_user is None:
        table.cm_user = getpass.getuser()
    else:
        table.cm_user = cm_user
    table.cm_uuid = str(uuid.uuid4())
    table.cm_id = "{:}_{:}_{:}_{:}".format(table.__tablename__, table.cm_user, cloud, cm_name)


class DEFAULT(db.Base):
    __tablename__ = 'default'
    id = Column(Integer)

    cm_name  = Column(String)
    cm_uuid = Column(String)
    cm_cloud = Column(String)
    cm_update = Column(String)
    cm_user = Column(String)
    cm_id = Column(String,primary_key=True)
    cm_type = Column(String)

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
    #volumes_attached []
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

