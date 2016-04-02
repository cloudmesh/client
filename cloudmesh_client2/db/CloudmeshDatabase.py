from __future__ import print_function
import os
from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

from cloudmesh_client.common.dotdict import dotdict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pprint import pprint
from sqlalchemy import update
from cloudmesh_client.shell.console import Console

class CloudmeshMixin(object):
    __mapper_args__ = {'always_refresh': True}

    category = Column(String, default="undefined")
    kind = Column(String, default="undefined")
    type = Column(String, default="undefined")

    provider = Column(String, default="undefined")

    cm_id = Column(Integer, primary_key=True)
    # created_at = Column(DateTime, default=datetime.now)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    created_at = Column(String,
                        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = Column(String,
                        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    label = Column(String, default="undefined")
    name = Column(String, default="undefined")
    user = Column(String, default="undefined")
    project = Column(String, default="undefined")

    def set_defaults(self, **kwargs):
        self.user = kwargs.get('user', CloudmeshDatabase.user)
        self.name = kwargs.get('name', 'undefined')
        self.label = kwargs.get('name', 'undefined')
        self.category = kwargs.get('category', 'undefined')
        self.kind = self.__kind__
        self.provider = self.__provider__

    def __repr__(self):
        try:
            print("{} {} {} {}".format(self.id, self.name, self.kind, self.category))
        except:
            Console.error("could not print object")

    def __str__(self):
        s = None
        try:
            s = dict(self.__dict__)
            del s['_sa_instance_state']
        except:
            pass
        return str(s)


class CloudmeshDatabase(object):
    '''

    def __init__(self, user=None):
        self.__dict__ = self.__shared_state

        if self.initialized is None:
            self.user = ConfigDict("cloudmesh.yaml")["cloudmesh.profile.username"]
            self.filename = Config.path_expand(os.path.join("~", ".cloudmesh", "cloudmesh.db"))
            self.engine = create_engine('sqlite:///{}'.format(self.filename), echo=False)
            self.data = {"filename": self.filename}

            if user is None:
                self.user = ConfigDict("cloudmesh.yaml")["cloudmesh.profile.username"]
            else:
                self.user = user
            CloudmeshDatabase.create()
            CloudmeshDatabase.create_tables()
            CloudmeshDatabase.start()

    #
    # MODEL
    #
    @classmethod
    def create(cls):
        # cls.clean()
        filename = Config.path_expand(os.path.join("~", ".cloudmesh", "cloudmesh.db"))
        if not os.path.isfile(filename):
            cls.create_model()


    '''
    __shared_state = {}
    data = {"filename": "data.db"}
    initialized = None
    engine = create_engine('sqlite:///{filename}'.format(**data), echo=False)
    Base = declarative_base()
    session = None
    tables = None
    user = "gvonlasz"

    def __init__(self):
        self.__dict__ = self.__shared_state

        if self.initialized is None:
            self.create()
            self.create_tables()
            self.start()

    #
    # MODEL
    #
    @classmethod
    def create(cls):
        # cls.clean()
        if not os.path.isfile("{filename}".format(**cls.data)):
            cls.create_model()

    @classmethod
    def create_model(cls):
        cls.Base.metadata.create_all(cls.engine)
        print("Model created")

    @classmethod
    def clean(cls):
        os.system("rm -f {filename}".format(**cls.data))

    @classmethod
    def create_tables(cls):
        """
        :return: the list of tables in model
        """
        cls.tables = [c for c in cls.Base.__subclasses__()]

    @classmethod
    def info(cls, kind=None):
        print()
        print("Info")
        print()
        print("{:<20} {:<15} {:<15} {:<4}".format("tablename", "provider", "kind", "count"))
        print(70 * "=")

        for t in cls.tables:
            if kind is None or t.__kind__ in kind:
                count = cls.session.query(t).count()
                print("{:<20} {:<15} {:<15} {:<4}".format(t.__tablename__, t.__provider__, t.__kind__, count))
        print()

    @classmethod
    def table(cls, category=None, provider=None, kind=None):
        """

        :param category:
        :param kind:
        :return: the table class based on a given table name.
                 In case the table does not exist an exception is thrown
        """
        def valid(category, check):
            if category is None:
                return True
            else:
                return check == category

        for t in cls.tables:
            test_provider = valid(provider, t.__provider__)
            test_kind = valid(kind, t.__kind__)

            if test_provider and test_kind:
                return t
        ValueError("ERROR: unkown table {} {}".format(provider, kind))

    #
    # SESSION
    #
    # noinspection PyPep8Naming
    @classmethod
    def start(cls):
        if cls.session is None:
            print("start session")
            Session = sessionmaker(bind=cls.engine)
            cls.session = Session()

    @classmethod
    def all(cls,
            provider='general',
            kind=None,
            table=None):

        t = table

        if provider is not None and kind is not None:
            t = cls.table(provider=provider, kind=kind)
            data = {
                "provider": provider,
                "kind": kind,
            }

        elif provider is None and kind is not None:
            t = cls.table(kind=kind)
            data = {
                "kind": kind,
            }

        else:
            ValueError("find is improperly used provider={provider} kind={kind}"
                       .format(**data))
        result = cls.session.query(t).all()
        return cls.to_list(result)

    @classmethod
    def find(cls,
             scope='first',
             provider=None,
             kind=None,
             output='dict',
             table=None,
             **kwargs
             ):
        """
        find (category="openstack", kind="vm", name="vm_002")
        find (VM_OPENSTACK, kind="vm", name="vm_002") # do not use this one its only used internally

        :param category:
        :param kind:
        :param table:
        :param kwargs:
        :return:
        """
        t = table

        if provider is not None and kind is not None:
            t = cls.table(provider=provider, kind=kind)
        else:
            data = {
                "provider": provider,
                "kind": kind,
                "table": table,
                "args": kwargs
            }
        elements = cls.session.query(t).filter_by(**kwargs)

        if scope == 'first':
            result = elements.first()
            if result is None:
                return None
            if output == 'dict':
                result = dotdict(cls.to_list([result])[0])
        elif output == 'dict':
            result =  cls.to_list(elements)

        return result

    @classmethod
    def x_find(cls, **kwargs):
        """
        This method returns either
        a) an array of objects from the database in dict format, that match a particular kind.
           If the kind is not specified vm is used. one of the arguments must be scope="all"
        b) a single entry that matches the first occurance of the query specified by kwargs,
           such as name="vm_001"

        :param kwargs: the arguments to be matched, scope defines if all or just the first value
               is returned. first is default.
        :return: a list of objects, if scope is first a single object in dotdict format is returned
        """
        kind = kwargs.pop("kind", "vm")
        scope = kwargs.pop("scope", "first")

        result = []

        for t in cls.tables:
            if (t.__kind__ == kind):
                part = cls.session.query(t).filter_by(**kwargs)
                result.extend(cls.to_list(part))

        objects = result
        if scope == "first" and objects is not None:
            objects = dotdict(result[0])

        return objects

    @classmethod
    def filter_by(cls, **kwargs):
        """
        This method returns either
        a) an array of objects from the database in dict format, that match a particular kind.
           If the kind is not specified vm is used. one of the arguments must be scope="all"
        b) a single entry that matches the first occurance of the query specified by kwargs,
           such as name="vm_001"

        :param kwargs: the arguments to be matched, scope defines if all or just the first value
               is returned. first is default.
        :return: a list of objects, if scope is first a single object in dotdict format is returned
        """
        scope = kwargs.pop("scope", "first")

        result = []

        for t in cls.tables:
            part = cls.session.query(t).filter_by(**kwargs)
            result.extend(cls.to_list(part))

        objects = result
        if scope == "first" and objects is not None:
            objects = dotdict(result[0])

        return objects

    @classmethod
    def add(cls, o, replace=True):

        if o is None:
            return
        if replace:
            current = cls.find(
                scope='first',
                provider=o.provider,
                kind=o.kind,
                output='object',
                name=o.name
            )

            if current is not None:
                for key in o.__dict__.keys():
                    current.__dict__[key] = o.__dict__[key]
                cls.save()
            else:
                cls.session.add(o)
        else:
            cls.session.add(o)
        cls.save()

    @classmethod
    def save(cls):
        cls.session.commit()
        cls.session.flush()

    @classmethod
    def to_list(cls, obj):
        """
        convert the object to dict

        :param obj:
        :return:
        """
        result = list()
        for u in obj:
            if u is not None:
                values = {}
                for key in list(u.__dict__.keys()):
                    if not key.startswith("_sa"):
                        values[key] = u.__dict__[key]
                result.append(values)
        return result

    #
    # DELETE
    #

    def delete(cls,
               provider=None,
               kind=None,
               **kwargs):
        """
        :param kind:
        :return:
        """
        #
        # BUG does not look for user related data
        # user = self.user or Username()
        #
        if provider is not None and kind is not None:
            t = cls.table(provider=provider, kind=kind)
        else:
            data = {
                "provider": provider,
                "kind": kind,
            }
            ValueError("find is improperly used provider={provider} kind={kind}"
                       .format(**data))
        if len(kwargs) == 0:
            cls.session.query(t).delete()
        else:
            cls.session.query(t).filter_by(**kwargs).delete()
        cls.save()

    @classmethod
    def update(cls,
               provider=None,
               kind=None,
               **kwargs):
        """

        :param kind:
        :param kwargs:
        :return:
        """
        # bug: user = self.user or Username()
        if provider is not None and kind is not None:
            t = cls.table(provider=provider, kind=kind)
        else:
            data = {
                "provider": provider,
                "kind": kind,
            }
            ValueError("find is improperly used provider={provider} kind={kind}"
                       .format(**data))
        filter = kwargs['filter']
        values = kwargs['update']

        cls.session.query(t).filter_by(**filter).update(values)
        cls.save()

    @classmethod
    def set(cls,
            name,
            attribute,
            value,
            provider=None,
            kind=None,
            ):
        if provider is None or kind is None:
            o = cls.filter_by(name=name)

            cls.update(kind=o.kind,
                       provider=o.provider,
                       filter={'name': name},
                       update={'label': 'x',
                               attribute: value}
                       )

