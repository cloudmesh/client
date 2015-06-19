from __future__ import print_function
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy import update
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
from cloudmesh_client.iaas.openstack_libcloud import OpenStack_libcloud, Insert
from cloudmesh_base.util import banner
debug = False

# engine = create_engine('sqlite:////tmp/test.db', echo=debug)

filename = Config.path_expand("~/.cloudmesh/cloudmesh.db")
endpoint = 'sqlite:///{:}'.format(filename)
engine = create_engine(endpoint)
Base = declarative_base(bind=engine)


class DEFAULT(Base):
    __tablename__ = 'default'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)
    user = Column(String)
    cloud = Column(String)
    cm_uuid = Column(String)

class IMAGE(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    label = Column(String)
    group = Column(String)
    cm_uuid = Column(String)
    cloud = Column(String)
    cm_user = Column(String)
    cloud_uuid = Column(String)

    def __init__(self,
                 name,
                 label=None,
                 group='default',
                 cloud='india',
                 cm_user=None):

        self.name = name
        self.label = label

        if label is None:
            self.label = name
        if cm_user is None:
            self.cm_user = getpass.getuser()
        else:
            self.cm_user = cm_user
        self.cm_uuid = str(uuid.uuid4())
        
class FLAVOR(Base):
    __tablename__ = 'flavor'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    label = Column(String)
    group = Column(String)
    cm_uuid = Column(String)
    cm_user = Column(String)
    cm_update = Column(String)
    cloud = Column(String)
    uuid = Column(String)
    bandwidth = Column(String)
    update = Column(String)
    disk = Column(String)
    internal_id = Column(String)
    price = Column(String)
    ram = Column(String)
    vcpus = Column(String)
    # extra = Column(String)


    def __init__(self,
                 name,
                 label=None,
                 group='default',
                 cloud='india',
                 cm_user=None):

        self.name = name
        self.label = label

        if label is None:
            self.label = name
        if cm_user is None:
            self.cm_user = getpass.getuser()
        else:
            self.cm_user = cm_user
        self.cm_uuid = str(uuid.uuid4())


class VM(Base):
    __tablename__ = 'vm'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    label = Column(String)
    group = Column(String)
    cm_uuid = Column(String)
    cloud = Column(String)
    cm_user = Column(String)
    uuid = Column(String)
    user = Column(String)
    meta = Column(String)
    image = Column(String)
    flavor = Column(String)
    status = Column(String)
    power_state = Column(String)
    task_state = Column(String)
    networks = Column(String)

    def __init__(self,
                 name,
                 label=None,
                 group='default',
                 cloud='india',
                 cm_user=None):


        self.name = name
        self.label = label

        if label is None:
            self.label = name
        if cm_user is None:
            self.cm_user = getpass.getuser()
        else:
            self.cm_user = cm_user
        self.cm_uuid = str(uuid.uuid4())


class CloudmeshDatabase(object):

    def __init__(self, cm_user=None):

        Base.metadata.create_all()
        self.session = self.connect()
        if cm_user is None:
            self.cm_user = getpass.getuser()
        else:
            self.cm_user = cm_user

    def connect(self):
        """

        :return:
        """
        Session = sessionmaker(bind=engine)
        self.session = Session()
        return self.session

    def find_vm_by_name(self, name):
        """

        :param name:
        :return:
        """
        return self.find(VM, name=name).first()

    def find (self, kind, **kwargs):
        """
        NOT TESTED
        :param kind:
        :param kwargs:
        :return:
        """
        return self.session.query(kind).filter_by(**kwargs)

    def delete_by_name(self, kind, name):
        """
        NOTTESTED
        :param kind:
        :param name:
        :return:
        """
        item = self.find (kind, name=name).first()
        self.delete(item)

    def delete(self, item):
        """
        NOTTESTED
        :param item:
        :return:
        """
        result = self.session.delete(item)
        self.save()

    def get_kind_from_str(self, str):
        if str == "VM":
            t = VM
        elif str == "DEFAULT":
            t = DEFAULT
        elif str == "IMAGE":
            t = IMAGE
        elif str == "FLAVOR":
            t = FLAVOR
        else:
            None
        return t

    def delete_all(self, kind=None):
        if kind == None:
            clean = ["VM", "DEFAULT"]
            self.delete_all(clean)
        elif isinstance(kind, str):
            clean =  [kind]
            self.delete_all(clean)
        else:
            for k in kind:
                t = self.get_kind_from_str(k)
                if t is not None:
                    for e in self.data.query(t):
                        self.delete(e)


    def merge(self, kind, items):
        self.replace(kind, item, erase_type=False)

    def replace(self, kind, items, erase=False):
        """
        NOT TESTED

        :param kind:
        :param items:
        :param erase:
        :return:
        """
        if erase:
            names = []
            for item in items:
                print ("delete", item.name)
                self.delete_by_name(kind, item.name)
            self.save()
            self.session.add_all(items)
        else:
            # overwrite existing elements
            for item in items:
                existing_item = self.find(kind, name=item.name).first()
                item.id = existing_item.id
                self.session.merge(item)
            self.save()

    def add(self, items):
        self.session.add_all(items)

    def save(self):
        self.session.commit()

    def name(self, value):
        self.default("name", value, "global")

    def get_name(self):
        current = self.session.query(DEFAULT).filter_by(name="name", cloud="global").first()
        return current.value

    def next_name(self):
        name = self.get_name()
        return Cloud.next_name(name)

    def default(self, key, value, cloud):
        # find
        d = [DEFAULT(cloud=cloud, name=key, value=value)]
        current = self.session.query(DEFAULT).filter_by(name=key).first()
        if current is None:
            self.session.add_all(d)
        else:
            current.value = value
            current.cloud = cloud
            self.save()
        self.save()

    @property
    def data(self):
        return self.session

    def _convert_to_lists(self, **kwargs):
        args = {}
        for k in kwargs:
            arg = kwargs[k]
            print (arg, type(arg))
            if isinstance(arg, str):
                arg = [arg]
            args[k] = arg
        return args

    def _find_obj_from_clouds(self, table, clouds=None, cm_user=None):
        '''
        returns all the servers from all clouds
        '''
        arg = self._convert_to_lists(clouds=clouds, cm_user=cm_user)
        print (arg)
        result = {}
        for cloud in arg['clouds']:
            d = self.session.query(table).all()
            result[cloud] = self.object_to_dict(d)
        return dict(result)

    def servers(self, clouds=None, cm_user=None):
        '''
        returns all the servers from all clouds
        '''
        return self._find_obj_from_clouds(VM, clouds=clouds, cm_user=cm_user)


    def flavors(self, clouds=None, cm_user=None):
        '''
        returns all the flavors from the various clouds
        '''
        return self._find_obj_from_clouds(FLAVOR, clouds=clouds, cm_user=cm_user)

    def images(self, clouds=None, cm_user=None):
        '''
        returns all the images from various clouds
        '''
        return self._find_obj_from_clouds(IMAGE, clouds=clouds, cm_user=cm_user)


    def get_by_filter(self, table, **kwargs):
        print ("ZZZZ", kwargs)
        if len(kwargs) == 1:
            return self.session.query(table).filter_by(kwargs).all()
        else:
            print ("YYYY", kwargs)

    def get(self, table):
        return self.dict(table)

    def object_to_dict(self, obj):
        result = dict()
        for u in obj:
            _id = u.id
            values = {}
            for key in u.__dict__.keys():
                if not key.startswith("_sa"):
                    values[key] = u.__dict__[key]
            result[_id] = values
        return result

    def convert_query_to_dict(self, table):
        return self.object_to_dict(self.session.query(table).all())

    def dict(self, table):
        return self.object_to_dict(self.session.query(table).all())

    def json(self, table):
        d = self.dict(table)
        return json.dumps(d)

    def update(self, kind, cloud):
        """
        GREGOR WORKS ON THIS        
        updates the data in the database

        :param kind: vm, image, flavor
        :param cloud: name of the cloud
        :return:
        """
        cloud = OpenStack_libcloud(cloud, cm_user=self.cm_user)

        group = "default"
        lister = None
        inserter  = None

        if kind.lower() == "vm":
            lister =  cloud.list_nodes
            inserter = Insert.vm
        elif kind.lower() in ["images", "image"]:
            lister = cloud.list_images
            inserter = Insert.image
        elif kind.lower() in ["flavor", "size"]:
            lister = cloud.list_flavors
            inserter = Insert.flavor
        else:
            return

        result = lister(kind="flat")
        for element in result:
            r = inserter("india", self.cm_user, group, result[element])

        self.save()
        # banner(kind, c="-")
        # pprint (result)

        # current = self.session.query(FLAVOR).filter_by(group="default").first()
        # print("UUUUU", current)

    def get_flavor(self, cloud, name):
        cloud = OpenStack_libcloud(cloud, cm_user=self.cm_user)
        f = cloud.get_flavor(name, kind='libcloud')
        print ("XXXX", f)

    def info(self, kind, name):
        """

        :param kind: vm, image, flavor
        :param name: name of the object or id
        :return: dict
        """
        pass

    def boot(self, cloud, cm_user, name, image, flavor, key, meta):
        cloud = OpenStack_libcloud(cloud, cm_user=self.cm_user)
        return cloud.boot(cloud, cm_user, name, image, flavor, key, meta)
