from __future__ import print_function

import json
import getpass
from pprint import pprint

from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

from cloudmesh_client.util import banner
from cloudmesh_client.common.hostlist import Parameter
from cloudmesh_client.db.db import database
from cloudmesh_client.db import \
    GROUP, RESERVATION, COUNTER, \
    BATCHJOB, SECGROUP, SECGROUPRULE, \
    VAR, DEFAULT, KEY, \
    FLAVOR_OPENSTACK, IMAGE_OPENSTACK, VM_OPENSTACK, \
    FLAVOR_LIBCLOUD, IMAGE_LIBCLOUD, VM_LIBCLOUD

from cloudmesh_client.common.todo import TODO
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import Username
from cloudmesh_client.common.LibcloudDict import LibcloudDict
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.dotdict import dotdict



# noinspection PyBroadException,PyPep8Naming
class CloudmeshDatabase(object):
    # TODO: see also common/VMname

    __shared_state = {}
    # ###################################
    # INIT
    # ###################################
    def __init__(self, user=None):
        """
        initializes the CloudmeshDatabase for a specific user.
        The user is used to add entries augmented with it.

        :param user: The username that is used to be added to the
                        objects in teh database
        """

        self.__dict__ = self.__shared_state

        self.connected = False
        self.db = database()
        self.db.Base.metadata.create_all()
        self.session = self.connect()

        if user is None:
            self.user = ConfigDict("cloudmesh.yaml")["cloudmesh.profile.username"]
        else:
            self.user = user


    def connect(self):
        """
        before any method is called we need to connect to the database

        :return: the session of the database
        """
        try:
            connected = self.connected
        except:
            connected = False
        if not connected:
            Session = sessionmaker(bind=self.db.engine,
                                   autoflush=False)
            self.session = Session()
            self.connected = True
        return self.session

    def save(self):
        self.session.commit()
        self.session.flush()
        pass

    def close(self):
        #self.session.close()
        #self.connected = False
        pass

    # ###################################
    # COUNTER
    # ###################################

    def counter_incr(self, name="counter", user=None):

        if user is None:
            user = self.user

        count = self.counter_get(name=name, user=user)

        count += 1

        self.counter_set(name=name, user=self.user, value=count)
        self.save()

    def counter_get(self, name="counter",user=None):
        """
        Function that returns the prefix username and count for vm naming.
        If it is not present in db, it creates a new entry.
        :return:
        """
        if user is None:
            user = self.user


        try:
            count = self.query("COUNTER", name=name, user=user).first().value
        except:
            count = 1
            c = COUNTER(name=name, value=count, user=user)
            self.add(c)

        return count

    def counter_set(self, name=None, value=None, user=None):
        """
        Special function to update vm prefix count.

        :param name:
        :param value:
        :param user:
        :return:
        """

        if user is None:
            user = self.user


        if type(value) != int:
            raise ValueError("counter must be integer")
        if value is None:
            value = 0

        element = self.find(COUNTER, output="object", name=name, user=user)
        element.first().value = value
        self.save()

    # ###################################
    # CLEAR, CONNECT, SAVE
    # ###################################

    def clear(self, kind, category, user=None):
        """
        This method deletes all 'kind' entries
        from the cloudmesh database
        :param category: the category name
        """
        if user is None:
            user = self.user

        try:
            elements = self.find(kind,
                                 output='object',
                                 scope="all",
                                 category=category,
                                 user=user)
            # pprint(elements)
            for element in elements:
                # pprint(element)
                self.delete(element)

        except Exception as ex:
            Console.error(ex.message, ex)



    def delete(self, item):
        """
        :param item:
        :return:
        """
        self.session.delete(item)
        self.save()

    def delete_all(self, kind):
        """
        :param kind:
        :return:
        """
        #
        # BUG does not look for user related data
        # user = self.user or Username()
        #
        self.session.query(kind).delete()
        self.save()

    def first(self, result):
        if len(result) == 0:
            return None
        else:
            return result[list(result.keys())[0]]

    # ####################################
    # QUERY, FIND
    # ####################################

    def find_by_name(self, kind, **kwargs):
        """
        find an object by name in the given table.
         If multiple objects have the same name, the first one is returned.

        :param name: the name
        :return: the object
        """
        # bug: user = self.user or Username()
        if 'name' not in kwargs:
            raise ValueError("name not specified in find_by_name")

        table_type = self.get_table(kind)

        result = self.first(self.find(table_type, **kwargs))

        return result

    def find_by_attributes(self, kind, **kwargs):
        """
        find an object by name in the given table.
         If multiple objects have the same name, the first one is returned.

        :param name: the name
        :return: the object
        """
        # bug: user = self.user or Username()
        table_type = self.get_table(kind)
        result = self.first(self.find(table_type, **kwargs))

        return result

    def x_find(self, **kwargs):
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
        kind = kwargs.get("kind", "vm")
        scope = kwargs.pop("scope", "first")

        object_tables = self.db.tables(kind="vm")
        print ("TTT", object_tables)

        result = []
        for t in self.db.tables(kind=kind):
            part = self.session.query(t).filter_by(**kwargs)
            print ("PPP", self.to_list(part))
            result.extend(self.to_list(part))

        objects = result

        if scope == "first" and result is not None:
            objects = dotdict(result[0])

        return objects


    def find(self, kind, scope="all", output="dict", **kwargs):
        """
        NOT tested
        :param kind:
        :param kwargs:
        :return:
        """
        # bug: user = self.user or Username()
        if "category" in kwargs:
            kind = self.cloud_to_kind_mapper(kwargs["category"], kind)
        result = self.query(kind, **kwargs)
        # print("LLL", result)
        if output == 'dict' and result is not None:
            result = self.object_to_dict(result)
            if scope == "first":
                if len(list(result)) > 0:
                    first = list(result)[0]
                    result = result[first]
                else:
                    result = None
        # if result == {}:
        #    return None

        return result

    def cloud_to_kind_mapper(self, cloud, kind):
        # bug: this should be done differently
        if cloud in LibcloudDict.Libcloud_category_list:
            if kind in ["image", "vm", "flavor"]:
                kind = "libcloud_"+kind
        return kind

    def query(self, kind, **kwargs):
        """
        NOT tested
        :param kind:
        :param kwargs:
        :return:
        """
        # bug: user = self.user or Username()
        # print("AAA")
        table = self.get_table(kind)
        # print(table)

        result = self.session.query(table).filter_by(**kwargs)
        # print("OK")
        # print(result.__dict__)
        return result

    def all(self, table):
        # bug: user = self.user or Username()
        table_type = self.get_table(table)
        elements = self.session.query(table_type).all()
        d = self.parse_objs(elements)
        return d

    def update(self, kind, **kwargs):
        """

        :param kind:
        :param kwargs:
        :return:
        """
        # bug: user = self.user or Username()
        self.find(kind, output="object", name=kwargs["name"]).update(kwargs)
        self.save()

    def update_vm_username(self, **kwargs):
        """
        Special function to update vm prefix count.
        :param kwargs:
        :return:
        """
        # what is this
        print ("SET USERNAME", kwargs)
        ValueError("Setting the username is not yet supported")
        # self.find(VMUSERMAP, output="object", vm_uuid=kwargs["vm_uuid"]).update(kwargs)
        # self.save()

    def delete_by_name(self, kind, name):
        """
        NOT TESTED
        :param kind:
        :param name:
        :return:
        """
        # bug user = self.user or Username()
        item = self.find(kind, name=name, output="item").first()
        self.delete(item)

    def to_list(self, obj):
        """
        convert the object to dict

        :param obj:
        :return:
        """
        result = list()
        for u in obj:
            _id = u.id
            print ("ID", u.id)
            values = {}
            for key in list(u.__dict__.keys()):
                if not key.startswith("_sa"):
                    values[key] = u.__dict__[key]
            result.append(values)
        # pprint(result)
        return result

    def object_to_dict(self, obj):
        """
        convert the object to dict

        :param obj:
        :return:
        """
        result = dict()
        for u in obj:
            _id = u.id
            values = {}
            for key in list(u.__dict__.keys()):
                if not key.startswith("_sa"):
                    values[key] = u.__dict__[key]
            result[_id] = values
        # pprint(result)
        return result

    def parse_objs(self, elements):
        # bug: replicates above function
        d = {}
        for element in elements:
            d[element.id] = {}
            for key in list(element.__dict__.keys()):
                if not key.startswith("_sa"):
                    d[element.id][key] = str(element.__dict__[key])
        return d

    def db_obj_dict(self, kind, obj_dict=None, **kwargs):
        """
        This method is a generic method to populate an object dict.
        The object dict can then be passed to database layer to add/ modify
        objects.
        :param dict: Dict to add object to
        :param kind: The table name in the db.
        :param kwargs: object parameters
        :return: Dict with object added
        """
        if obj_dict is None:
            obj_dict = dict()

        dict_length = len(obj_dict)

        obj_dict[dict_length] = dict()
        obj_dict[dict_length][kind] = kwargs

        # print(obj_dict)
        return obj_dict

    def dict(self, table):
        """
        returns a dict from all elements in the table

        :param table:
        :return:
        """
        # bug : user = self.user or Username()
        return self.object_to_dict(self.session.query(table).all())

    def json(self, table):
        """
        returns a json representation from all elements in the table

        :param table:
        :return:
        """
        d = self.dict(table)
        return json.dumps(d)

    def info(self, what=None, kind=None, output='dict'):
        """
        prints information about the database
        """
        result = {}
        if kind is None:
            kinds = self.db.tablenames()
        else:
            kinds = Parameter.expand(kind)
        if what is None:
            infos = "table,count"
        else:
            infos = Parameter.expand(what)

        banner("Databse table information", c="-")
        inspector = inspect(self.db.engine)

        result["username"] = self.user
        if "table" in infos:
            result['table'] = dict()
            for table_name in inspector.get_table_names():
                if table_name in kinds:
                    result['table'][table_name] = {}
                    for column in inspector.get_columns(table_name):
                        result['table'][table_name][column['name']] = column['type']

        counter = 0
        if "count" in infos:
            result['count'] = {}
            for table_name in inspector.get_table_names():
                if table_name in kinds:
                    t = self.db.table(table_name)
                    rows = self.session.query(t).count()
                    result['count'][table_name] = rows
                    # print("Count {:}: {:}".format(table_name, rows))
                    counter = counter + rows
            # result['count']['sum'] = counter

        return result



    def add(self, o):
        o.user = self.user
        self.session.add(o)
        self.session.commit()
        self.session.flush()

    def add_obj(self, obj_dict):
        # print("Inside add_obj")
        # print("Object Dict to add: {}".format(obj_dict))

        for obj in list(obj_dict.values()):
            # print(obj)
            for key in list(obj.keys()):
                table_name = self.get_table(key)
                obj_to_persist = table_name(**obj[key])
                self.add(obj_to_persist)

    def get(self, table, **kwargs):
        return self.session.query(table).filter_by(**kwargs).first()


    # ###################################
    # ATTRIBUTES
    # ###################################
    def attributes(self, kind, name):
        provider = CloudProvider(name).provider
        return provider.attributes(kind)

    def db_table(self, kind):
        _type = kind
        if type(kind) == str:
            _type = self.get_table(kind)
        return _type

    def get_table(self, kind):
        if type(kind) == str:
            if kind.lower() in ["flavor"]:
                return FLAVOR_OPENSTACK
            elif kind.lower() in ["libcloud_flavor"]:
                return FLAVOR_LIBCLOUD
            elif kind.lower() in ["default"]:
                return DEFAULT
            elif kind.lower() in ["var"]:
                return VAR
            elif kind.lower() in ["image"]:
                return IMAGE_OPENSTACK
            elif kind.lower() in ["libcloud_image"]:
                return IMAGE_LIBCLOUD
            elif kind.lower() in ["vm"]:
                return VM_OPENSTACK
            elif kind.lower() in ["libcloud_vm"]:
                return VM_LIBCLOUD
            elif kind.lower() in ["key"]:
                return KEY
            elif kind.lower() in ["group"]:
                return GROUP
            elif kind.lower() in ["reservation"]:
                return RESERVATION
            elif kind.lower() in ["counter"]:
                return COUNTER
            elif kind.lower() in ["vmusermap"]:
                return VMUSERMAP
            elif kind.lower() in ["batchjob"]:
                return BATCHJOB
            elif kind.lower() in ["secgroup"]:
                return SECGROUP
            elif kind.lower() in ["secgrouprule"]:
                return SECGROUPRULE
            else:
                TODO.implement("wrong table type: `{}`".format(kind))
        else:
            return kind

    # ###################################
    # REFRESH
    # ###################################
    # noinspection PyUnusedLocal
    def refresh(self, kind, name, **kwargs):
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
            user = self.user

            if kind in ["flavor", "image", "vm", "secgroup"]:

                # get provider for specific cloud
                provider = CloudProvider(name).provider

                # clear local db records for kind
                self.clear(kind, name)

                # for secgroup, clear rules as well
                if kind == "secgroup":
                    self.clear("secgrouprule", name)

                if kind in ["flavor", "image"]:

                    # flavors = provider.list_flavor(name)
                    elements = provider.list(kind, name)
                    for element in list(elements.values()):
                        element["uuid"] = element['id']
                        element['type'] = 'string'
                        element["category"] = name
                        element["cloud"] = name
                        element["user"] = user

                        db_obj = {0: {kind: element}}
                        self.add_obj(db_obj)
                        self.save()

                    return True

                elif kind in ["vm"]:

                    # flavors = provider.list_flavor(name)
                    elements = provider.list(kind, name)

                    for element in list(elements.values()):
                        element[u"uuid"] = element['id']
                        element[u'type'] = 'string'
                        element[u"category"] = name
                        element[u"cloud"] = name
                        element[u"user"] = user
                        vm_name = element["name"]

                        g = self.find_by_attributes("group", member=vm_name)

                        if g is not None:
                            element[u"group"] = g["name"]
                        else:
                            element[u"group"] = "undefined"

                        db_obj = {0: {kind: element}}

                        self.add_obj(db_obj)
                        self.save()
                    return True

                elif kind == "secgroup":
                    secgroups = provider.list_secgroup(name)
                    # pprint(secgroups)
                    for secgroup in list(secgroups.values()):
                        secgroup_db_obj = self.db_obj_dict("secgroup",
                                                           name=secgroup['name'],
                                                           uuid=secgroup['id'],
                                                           category=name,
                                                           project=secgroup['tenant_id'],
                                                           user=user
                                                           )

                        for rule in secgroup['rules']:
                            rule_db_obj = self.db_obj_dict("secgrouprule",
                                                           uuid=rule['id'],
                                                           name=secgroup['name'],
                                                           groupid=rule['parent_group_id'],
                                                           category=name,
                                                           user=user,
                                                           project=secgroup['tenant_id'],
                                                           fromPort=rule['from_port'],
                                                           toPort=rule['to_port'],
                                                           protocol=rule['ip_protocol'])

                            if bool(rule['ip_range']) is not False:
                                rule_db_obj[0]['secgrouprule']['cidr'] = rule['ip_range']['cidr']

                            self.add_obj(rule_db_obj)
                            self.save()
                        # rule-for-loop ends

                        self.add_obj(secgroup_db_obj)
                        self.save()
                    return True

            elif kind in ["batchjob"]:

                # provider = BatchProvider(name).provider
                # provider = BatchProvider(name)

                from cloudmesh_client.cloud.hpc.BatchProvider import BatchProvider
                provider = BatchProvider(name)

                vms = provider.list_job(name)
                for vm in list(vms.values()):
                    vm[u'uuid'] = vm['id']
                    vm[u'type'] = 'string'
                    vm[u'category'] = name
                    vm[u'user'] = user
                    db_obj = {0: {kind: vm}}

                    self.add_obj(db_obj)
                    self.save()
                return True

            else:
                Console.error("refresh not supported for this kind: {}".format(kind))

        except Exception as ex:
            Console.error(ex.message)
            return False

def main():
    cm = CloudmeshDatabase()

    #    m = DEFAULT("hallo", "world")
    #    m.newfield__hhh = 13.9
    #    cm.add(m)

    #    n = cm.query(DEFAULT).filter_by(name='hallo').first()

    #    print("\n\n")

    #    pprint(n.__dict__)

    #    o = cm.get(DEFAULT, 'hallo')

    #    print("\n\n")

    #    pprint(o.__dict__)

    #    m = DEFAULT("other", "world")
    #    m.other = "ooo"
    #    cm.add(m)

    #    print("\n\n")
    #    pprint(cm.get(DEFAULT, 'other').__dict__)

    cm.info()

    m = COUNTER("counter", 2, user="gregor")
    cm.add(m)

    o = cm.get(COUNTER, name='counter', user="gregor")

    print("\n\n")

    pprint(o.__dict__)

    cm.counter_set(name="counter", user="gregor", value=0)

    for i in range(0, 10):
        cm.counter_incr(name="counter", user="gregor")

    print(cm.counter_get(name="counter", user="gregor"))
    """



    cm.info()
    # print(cm.list(VM))
    """


if __name__ == "__main__":
    main()
