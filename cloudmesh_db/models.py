from __future__ import print_function
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect
from prettytable import PrettyTable
from cloudmesh_common.tables import dict_printer
import uuid
import os
import getpass
import json
from pprint import pprint
import sys
from cloudmesh_cloud.clouds import Cloud
from cloudmesh_common.ConfigDict import ConfigDict
from cloudmesh_common.ConfigDict import Config

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

class IMAGE(BASE):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    label = Column(String)
    group = Column(String)
    uuid = Column(String)
    cloud = Column(String)
    user = Column(String)
    cloud_uuid = Column(String)

class FLAVOR(BASE):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    label = Column(String)
    group = Column(String)
    uuid = Column(String)
    cloud = Column(String)
    user = Column(String)
    cloud_uuid = Column(String)

class VM(Base):
    __tablename__ = 'vm'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    label = Column(String)
    group = Column(String)
    uuid = Column(String)
    cloud = Column(String)
    user = Column(String)
    cloud_uuid = Column(String)
    cloud_user = Column(String)
    cloud_meta = Column(String)
    cloud_image = Column(String)
    cloud_flavor = Column(String)
    cloud_status = Column(String)
    cloud_power_state = Column(String)
    cloud_task_state = Column(String)
    cloud_networks = Column(String)

    def __init__(self,
                 name,
                 label=None,
                 group='default',
                 cloud='india',
                 user=None):

        self.name = name
        self.label = label

        if label is None:
            self.label = name
        if user is None:
            self.user = getpass.getuser()

        self.uuid = str(uuid.uuid4())


class CloudmeshDatabase(object):

    def __init__(self):
        Base.metadata.create_all()
        self.session = self.connect()

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
