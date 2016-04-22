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
from cloudmesh_client.common.ConfigDict import ConfigDict, Config
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.shell.console import Console


class CloudmeshMixin(object):
    __mapper_args__ = {'always_refresh': True}

    category = Column(String, default=None)
    kind = Column(String, default=None)
    type = Column(String, default=None)

    provider = Column(String, default=None)

    cm_id = Column(Integer, primary_key=True)
    created_at = Column(String,
                        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = Column(String,
                        default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        onupdate=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    label = Column(String, default=None)
    name = Column(String, default=None)
    user = Column(String, default=None)
    project = Column(String, default=None)

    def set_user(self):
        self.user = ConfigDict("cloudmesh.yaml")["cloudmesh.profile.user"]

    def set_defaults(self, **kwargs):
        # self.user = kwargs.get('user', CloudmeshDatabase.user)
        # TODO: for now hardcode user
        # self.user = Default.user#'gvonlasz'
        self.name = kwargs.get('name', None)
        self.label = kwargs.get('name', None)
        self.category = kwargs.get('category', None)
        self.type = kwargs.get('type', 'str')
        self.kind = self.__kind__
        self.provider = self.__provider__

    def __repr__(self):
        try:
            return ("<{}> id={} name={} category={}: dict={}".format(self.kind, self.cm_id, self.name, self.category,
                                                                     self.__dict__))
        except:
            Console.error("could not print object")
            return None

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
            self.user = ConfigDict("cloudmesh.yaml")["cloudmesh.profile.user"]
            self.filename = Config.path_expand(os.path.join("~", ".cloudmesh", "cloudmesh.db"))
            self.engine = create_engine('sqlite:///{}'.format(self.filename), echo=False)
            self.data = {"filename": self.filename}

            if user is None:
                self.user = ConfigDict("cloudmesh.yaml")["cloudmesh.profile.user"]
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
    data = {"filename": Config.path_expand(os.path.join("~", ".cloudmesh", "cloudmesh.db"))}
    initialized = None
    engine = create_engine('sqlite:///{filename}'.format(**data), echo=False)
    Base = declarative_base()
    session = None
    tables = None
    # user = "gvonlasz"
    # user = ConfigDict("cloudmesh.yaml")["cloudmesh.profile.user"]
    user = None

    def __init__(self):
        self.__dict__ = self.__shared_state

        if self.initialized is None:
            self.filename = Config.path_expand(os.path.join("~", ".cloudmesh", "cloudmesh.db"))
            self.create()
            self.create_tables()
            self.start()
            self.user = ConfigDict(filename="cloudmesh.yaml")["cloudmesh.profile.user"]

    @classmethod
    def refresh_new(cls, kind, name, **kwargs):
        """
        This method refreshes the local database
        with the live cloud details
        :param kind:
        :param name:
        :param kwargs:
        :return:
        """

        try:
            # print(cloudname)
            # get the user
            # TODO: Confirm user

            # user = cls.user

            purge = kwargs.get("purge", True)

            if kind in ["flavor", "image", "vm"]:

                # get provider for specific cloud
                provider = CloudProvider(name).provider

                current_elements = cls.find_new(category=name, kind=kind, output='dict', key='name')

                #returns the following:
                #current_elements = {}
                #for element in elements:
                #    current_elements[element["name"]] = element

                # pprint(current_elements)

                if purge:
                    cls.clear(kind=kind, category=name)

                elements = provider.list(kind, name)
                #
                # image, flavor, username, group, ...
                #

                for element in list(elements.values()):
                    element["uuid"] = element['id']
                    element['type'] = 'string'
                    element["category"] = name

                    # element["user"] = user
                    element["kind"] = kind
                    element["provider"] = provider.cloud_type
                    if current_elements is not None:
                        for index in current_elements:
                            current = current_elements[index]
                            for attribute in ["username", "image", "flavor", "group"]:
                                if attribute in current and current[attribute] is not None:
                                    element[attribute] = current[attribute]
                    print("CCC", index, element["name"], element["flavor"])
                    cls.add(element)

                return True

            elif kind in ["batchjob"]:

                # provider = BatchProvider(name).provider
                # provider = BatchProvider(name)

                from cloudmesh_client.cloud.hpc.BatchProvider import BatchProvider
                provider = BatchProvider(name)

                vms = provider.list_job(name)
                for job in list(vms.values()):
                    job[u'uuid'] = job['id']
                    job[u'type'] = 'string'
                    job[u'category'] = name
                    # job[u'user'] = user

                    cls.add(job)
                    cls.save()
                return True

            elif kind not in ["secgroup"]:
                Console.error("refresh not supported for this kind: {}".format(kind))

        except Exception as ex:
            Console.error("Problem with secgroup")
            return False

    @classmethod
    def find_new(cls, **kwargs):
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

        """

        parameters:
            output="dict"
            key="name"

        output:
            name1:    element["name"]
              attribute
              ...
            name2:
               ....

        parameters:
            output="dict"
            key="id"

        output:
            "0":  index in the list of elements
              attribute
              ...
            "1":
               ....

        parameters:
            output="list"
            key="id"

        output:
            [element0, element1, element2] each of which is a dot dict

        other things
            scope = "first" -> one elemnet only as dotdict  (not an list)
            scope = "all" -> any of the above but each element is a dotdict returns either list or dict


        find -> list

        to_dict(list, key="name")

        to_dict(find(...), key="name") - dict of dotdicts  <-- or None if we do not find

        ??? too complex to implement, find(...).dict(key="name") - dict of dotdicts


        Default.purge = True  -> when delete vm it deletes vm from db, if not keep the vm

        Vm.names -> list names of all vms in db

            if newvmname in Vm.names:
                error vm already exists

        cls.replace

        cls.add -> cls.upsert
             just keep add for now but introduce new upser that just calls current add?
             or do refactor on add and replaces with upsert

        """



        scope = kwargs.pop("scope", "all")
        output = kwargs.pop("output", "dict")

        table = kwargs.pop("table", None)

        result = []

        if table is not None:
            part = cls.session.query(table).filter_by(**kwargs)
            result.extend(cls.to_list(part))

        else:
            category = kwargs.get("category", None)
            provider = kwargs.get("provider", None)
            kind = kwargs.get("kind", None)

            if provider is not None and kind is not None:

                t = cls.table(provider, kind)
                part = cls.session.query(t).filter_by(**kwargs)
                if output == 'dict':
                    result.extend(cls.to_list(part))
                else:
                    result.extend(part)
            elif provider is None:
                for t in cls.tables:
                    # print ("CCCC", t.__kind__, t.__provider__, kwargs)
                    if (t.__kind__ == kind):
                        part = cls.session.query(t).filter_by(**kwargs)
                        if output == 'dict':
                            result.extend(cls.to_list(part))
                        else:
                            result.extend(part)
            else:
                Console.error("nothing searched {}".format(kwargs))

        objects = result

        if len(objects) == 0:
            return None
        elif scope == "first":
            if output == 'dict':
                objects = dotdict(result[0])
            else:
                objects = result[0]

        return objects

    @classmethod
    def add_new(cls, d, replace=True):
        """
        o dotdict

            if o is a dict an object of that type is created. It is checked if another object in the db already exists,
            if so the attributes of the object will be overwritten with the once in the database

            provider, kind, category, name must be set to identify the object


        o is in CloudmeshDatabase.Base

            this is an object of a table has been created and is to be added. It is checked if another object in the db
            already exists. If so the attributes of the existing object will be updated.


        """

        if d is None:
            return

        if type(d) in [dict, dotdict]:

            if "provider" in d:
                t = cls.table(kind=d["kind"], provider=d["provider"])
                provider = d["provider"]
            else:
                t = cls.table(kind=d["kind"])

                provider = t.__provider__
            d["provider"] = provider

            element = t(**d)

        else:
            element = d

        if replace:

            element.provider = element.__provider__

            current = cls.find(
                provider=element.provider,
                kind=element.kind,
                name=element.name,
                category=element.category
            )

            if current is not None:
                for key in element.__dict__.keys():
                    current[0][key] = element.__dict__[key]
                    # current[0]['user'] = element.__dict__["user"]
            else:
                cls.session.add(element)
        else:
            cls.session.add(element)
        cls.save()

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
        for table in cls.tables:
            cls.delete(kind=table.__kind__, provider=table.__provider__)

    @classmethod
    def create_tables(cls):
        """
        :return: the list of tables in model
        """
        cls.tables = [c for c in cls.Base.__subclasses__()]

    @classmethod
    def info(cls, kind=None):
        result = []

        for t in cls.tables:
            entry = dict()
            if kind is None or t.__kind__ in kind:
                entry = {
                    "count": cls.session.query(t).count(),
                    "tablename": t.__tablename__,
                    "provider": t.__provider__,
                    "kind": t.__kind__
                }
                result.append(entry)
        return result

    @classmethod
    def table(cls, provider=None, kind=None, name=None):
        """

        :param category:
        :param kind:
        :return: the table class based on a given table name.
                 In case the table does not exist an exception is thrown
        """

        t = None
        if name is not None:
            for t in cls.tables:
                if t.__tablename__ == name:
                    return t

        if provider is None and kind is not None:
            t = cls.get_table_from_kind(kind)
            return t

        if provider is None and kind is None:
            Console.error("No Kind specified")
            return None

        for t in cls.tables:
            if t.__kind__ == kind and t.__provider__ == provider:
                return t

        Console.error("No table found for name={}, provider={}, kind={}".format(name, provider, kind))

    @classmethod
    def get_table_from_kind(cls, kind):
        providers = set()
        for t in cls.tables:
            if t.__kind__ == kind:
                providers.add(t)
        providers = list(providers)
        if len(providers) == 1:
            return providers[0]
        elif len(providers) > 1:
            Console.error("Providers for kind={} are not unique. Found={}".format(kind, providers))
        else:
            Console.error("Providers for kind={} nor found".format(kind))
        return None

    #
    # SESSION
    #
    # noinspection PyPep8Naming
    @classmethod
    def start(cls):
        if cls.session is None:
            # print("start session")
            Session = sessionmaker(bind=cls.engine)
            cls.session = Session()

    @classmethod
    def all(cls,
            provider='general',
            kind=None,
            table=None):

        t = table
        data = {
            "provider": provider,
            "kind": kind,
        }

        if provider is not None and kind is not None:
            t = cls.table(provider=provider, kind=kind)

        elif provider is None and kind is not None:
            t = cls.table(kind=kind)
        else:
            Console.error("find is improperly used provider={provider} kind={kind}"
                          .format(**data))
        result = cls.session.query(t).all()
        return cls.to_list(result)

    @classmethod
    def _find(cls,
              scope='all',
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

        if table is None:

            if provider is None and kind is None:
                Console.error("No provider or kind specified in find")
            else:
                t = cls.table(provider=provider, kind=kind)

        elements = cls.session.query(t).filter_by(**kwargs)

        if scope == 'first':
            result = elements.first()
            if result is None:
                return None
            if output == 'dict':
                result = dotdict(cls.to_list([result])[0])
        elif output == 'dict':
            result = cls.to_list(elements)
        elif output == 'namedict':
            result = cls.to_dict(elements)
        return result

    @classmethod
    def find(cls, **kwargs):
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

        scope = kwargs.pop("scope", "all")
        output = kwargs.pop("output", "dict")

        table = kwargs.pop("table", None)

        result = []

        if table is not None:
            part = cls.session.query(table).filter_by(**kwargs)
            result.extend(cls.to_list(part))

        else:
            category = kwargs.get("category", None)
            provider = kwargs.get("provider", None)
            kind = kwargs.get("kind", None)

            if provider is not None and kind is not None:

                t = cls.table(provider, kind)
                part = cls.session.query(t).filter_by(**kwargs)
                if output == 'dict':
                    result.extend(cls.to_list(part))
                else:
                    result.extend(part)
            elif provider is None:
                for t in cls.tables:
                    # print ("CCCC", t.__kind__, t.__provider__, kwargs)
                    if (t.__kind__ == kind):
                        part = cls.session.query(t).filter_by(**kwargs)
                        if output == 'dict':
                            result.extend(cls.to_list(part))
                        else:
                            result.extend(part)
            else:
                Console.error("nothing searched {}".format(kwargs))

        objects = result

        '''
        if len(objects) == 0 and scope == "first":
            objects = None
        elif len(objects) != 0:
            if scope == "first":
                if output == 'dict':
                    objects = dotdict(result[0])
                else:
                    objects = result[0]
        '''

        if len(objects) == 0:
            return None
        elif scope == "first":
            if output == 'dict':
                objects = dotdict(result[0])
            else:
                objects = result[0]

        return objects

    @classmethod
    def add(cls, d, replace=True):
        """
        o dotdict

            if o is a dict an object of that type is created. It is checked if another object in the db already exists,
            if so the attributes of the object will be overwritten with the once in the database

            provider, kind, category, name must be set to identify the object


        o is in CloudmeshDatabase.Base

            this is an object of a table has been created and is to be added. It is checked if another object in the db
            already exists. If so the attributes of the existing object will be updated.


        """

        if d is None:
            return

        if type(d) in [dict, dotdict]:

            if "provider" in d:
                t = cls.table(kind=d["kind"], provider=d["provider"])
                provider = d["provider"]
            else:
                t = cls.table(kind=d["kind"])

                provider = t.__provider__
            d["provider"] = provider

            element = t(**d)

        else:
            element = d

        if replace:

            element.provider = element.__provider__

            current = cls.find(
                provider=element.provider,
                kind=element.kind,
                name=element.name,
                category=element.category,
                scope="first" # this ensures the returned result is object/dict, not list
            )
            if current is not None:
                for key in element.__dict__.keys():
                    # update based on the keys that exist in the db model
                    if key in current:
                        current[key] = element.__dict__[key]
                # current['user'] = element.__dict__["user"]

                # update on the db
                cls.update(provider=current["provider"],
                           kind=current["kind"],
                           filter={"name":current["name"]},
                           update=current)
            else:
                cls.session.add(element)
        else:
            cls.session.add(element)
        cls.save()

    @classmethod
    def add_obj(cls, objects):
        for obj in list(objects.values()):
            for key in list(obj.keys()):
                t = cls.table(kind=key)
                o = t(**obj[key])
                cls.add(o)

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
        scope = kwargs.pop("scope", "all")

        result = []

        for t in cls.tables:
            part = cls.session.query(t).filter_by(**kwargs)
            result.extend(cls.to_list(part))

        objects = result
        if scope == "first" and objects is not None:
            objects = dotdict(result[0])

        return objects

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

    @classmethod
    def to_dict(cls, obj, key="name"):
        """
        convert the object to dict

        :param obj:
        :return:
        """
        result = dict()
        for u in obj:
            if u is not None:
                values = {}
                for attribute in list(u.__dict__.keys()):
                    if not attribute.startswith("_sa"):
                        values[attribute] = u.__dict__[attribute]
                result[values[key]] = values
        return result

    #
    # DELETE
    #
    @classmethod
    def delete(cls, **kwargs):
        """
        :param kind:
        :return:
        """
        #
        # BUG does not look for user related data
        # user = self.user or Username()
        #
        result = False
        provider = kwargs.get("provider", None)
        kind = kwargs.get("kind")
        if provider is None:
            t = cls.get_table_from_kind(kind)

        if provider is None or kind is None:
            data = {
                "provider": provider,
                "kind": kind,
            }
            ValueError("find is improperly used provider={provider} kind={kind}"
                       .format(**data))

        t = cls.table(provider=provider, kind=kind)

        if len(kwargs) == 0:
            result = cls.session.query(t).delete()
        else:
            result = cls.session.query(t).filter_by(**kwargs).delete()
        cls.save()

        return result != 0

    @classmethod
    def update(cls, **kwargs):
        """

        :param kind:
        :param kwargs:
        :return:
        """
        provider = kwargs.get("provider", None)
        kind = kwargs.get("kind", None)

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

        # print (t, filter, values)

        cls.session.query(t).filter_by(**filter).update(values)
        cls.save()

    @classmethod
    def set(cls,
            name,
            attribute,
            value,
            provider=None,
            kind=None,
            scope="all"
            ):

        if scope == "first" and provider is None:
            elements = cls.filter_by(name=name, kind=kind)[0]
            # pprint(elements)

            o = dotdict(elements)
            # print("PPPP", kind, name, attribute, value, o)

            if o[attribute] != value:
                cls.update(kind=o["kind"],
                           provider=o["provider"],
                           filter={'name': name},
                           update={attribute: value}
                           )
        elif scope == "first":
            o = dotdict(cls.filter_by(name=name, provider=provider, kind=kind)[0])
            # print("PPPP", provider, kind, name, attribute, value, o)

            if o[attribute] != value:
                cls.update(kind=o["kind"],
                           provider=o["provider"],
                           filter={'name': name},
                           update={attribute: value}
                           )
        elif provider is None or kind is None or scope == "all":
            o = cls.filter_by(name=name)
            cls.update(kind=o["kind"],
                       provider=o["provider"],
                       filter={'name': name},
                       update={attribute: value}
                       )
        else:
            Console.error("Problem setting attributes")

    @classmethod
    def clear(cls, kind, category, user=None):
        """
        This method deletes all 'kind' entries
        from the cloudmesh database
        :param category: the category name
        """
        # if user is None:
        #    user = cls.user

        try:
            elements = cls.find(kind=kind,
                                output='object',
                                scope="all",
                                category=category,
                                user=user)
            # pprint(elements)
            if elements is None:
                return
            for element in elements:
                # pprint(element)
                cls.session.delete(element)

        except Exception as ex:
            Console.error(ex.message)

    # ###################################
    # REFRESH
    # ###################################
    # noinspection PyUnusedLocal
    @classmethod
    def refresh(cls, kind, name, **kwargs):
        """
        This method refreshes the local database
        with the live cloud details
        :param kind:
        :param name:
        :param kwargs:
        :return:
        """

        try:
            # print(cloudname)
            # get the user
            # TODO: Confirm user

            # user = cls.user
            purge = kwargs.get("purge", True)

            if kind in ["flavor", "image", "vm"]:

                # get provider for specific cloud
                provider = CloudProvider(name).provider

                elements = cls.find(category=name, kind=kind, output='dict')

                current_elements = {}
                if elements:
                    for element in elements:
                        current_elements[element["name"]] = element

                    # pprint(current_elements)

                # if purge:
                #     cls.clear(kind=kind, category=name)

                elements = provider.list(kind, name)

                for element in list(elements.values()):
                    element["uuid"] = element['id']
                    element['type'] = 'string'
                    element["category"] = name

                    # element["user"] = user
                    element["kind"] = kind
                    element["provider"] = provider.cloud_type
                    if current_elements is not None:
                        for index in current_elements:
                            current = current_elements[index]
                            for attribute in ["username", "image", "flavor", "group"]:
                                if attribute in current and current[attribute] is not None:
                                    element[attribute] = current[attribute]
                    # print ("CCC", index, element["name"], element["flavor"])
                    cls.add(element)

                return True

            elif kind in ["batchjob"]:

                # provider = BatchProvider(name).provider
                # provider = BatchProvider(name)

                from cloudmesh_client.cloud.hpc.BatchProvider import BatchProvider
                provider = BatchProvider(name)

                vms = provider.list_job(name)
                for job in list(vms.values()):
                    job[u'uuid'] = job['id']
                    job[u'type'] = 'string'
                    job[u'category'] = name
                    # job[u'user'] = user

                    cls.add(job)
                    cls.save()
                return True

            elif kind not in ["secgroup"]:
                Console.error("refresh not supported for this kind: {}".format(kind))

        except Exception as ex:
            Console.error("Problem with secgroup")
            return False
