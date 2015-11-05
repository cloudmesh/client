from __future__ import print_function

from cloudmesh_client.db.models import database, VM, FLAVOR, IMAGE, DEFAULT

from sqlalchemy.orm import sessionmaker
from cloudmesh_base.util import banner
from sqlalchemy import inspect
from cloudmesh_client.iaas.openstack_libcloud import OpenStack_libcloud
from pprint import pprint
from cloudmesh_base.hostlist import Parameter
from datetime import datetime
from cloudmesh_base.hostlist import Parameter
import getpass

class CloudmeshDatabase(object):
    def __init__(self, cm_user=None):
        """
        initializes the CloudmeshDatabase for a specific user.
        The user is used to add entries augmented with it.

        :param cm_user: The username that is used to be added to the objects in teh database
        """

        self.db = database()
        self.db.Base.metadata.create_all()
        self.session = self.connect()
        if cm_user is None:
            self.cm_user = getpass.getuser()
        else:
            self.cm_user = cm_user

    def getID(self, kind, id, cloudname):
        """
        returns a human readable (unique) id
        :param kind: the type of the table flavor, vm, image, default
        :param id: the id
        :param cloudname: the name of the cloud.
        :return: the id

        todo: username is currently not in the id
        """
        result = "{:}_{:}_{:}_{:}".format(
            cloudname,
            self.cm_user,
            kind,
            id)

        return result

    def connect(self):
        """
        before any method is called we need to connect to the database

        :return: the session of the database
        """
        Session = sessionmaker(bind=self.db.engine)
        self.session = Session()
        return self.session

    def find_vm_by_name(self, name):
        """
        finds a vm by the given name and returns the first one that matches it.

        todo: maybe making it a dict

        :param name: the name of the vm
        :return:
        """
        return self.find(VM, name=name).first()

    def find_by_name(self, kind, name):
        """
        find an object by name in the given table.
         If multiple objects have the same name, the first one is returned.

        :param name: the name
        :return: the object
        """
        table_type = kind
        if type(kind) == str:
            table_type = self.get_table_from_name(kind)
        return self.find(table_type, name=name).first()

    def find(self, kind, **kwargs):
        """
        NOT teted
        :param kind:
        :param kwargs:
        :return:
        """
        table_type = kind
        if type(kind) == str:
            table_type = self.db.get_table(kind)
        return self.session.query(table_type).filter_by(**kwargs)

    def delete_by_name(self, kind, name):
        """
        NOTTESTED
        :param kind:
        :param name:
        :return:
        """
        item = self.find(kind, name=name).first()
        self.delete(item)

    def delete(self, item):
        """
        NOTTESTED
        :param item:
        :return:
        """
        result = self.session.delete(item)
        self.save()

    def delete_all(self, kind=None):
        if kind is None:
            clean = ["VM", "DEFAULT"]
            self.delete_all(clean)
        elif isinstance(kind, str):
            clean = [kind]
            self.delete_all(clean)
        else:
            for k in kind:
                t = database.get_table(k)
                if t is not None:
                    for e in self.data.query(t):
                        self.delete(e)

    def merge(self, kind, items):
        self.replace(kind, item, erase=False)

    def replace(self, kind, items, erase=False):
        """
        NOT TESTED

        :param kind:
        :param items:
        :param erase:
        :return:
        """
        table_type = kind
        if type(kind) == str:
            table_type = self.get_table_from_name(kind)
        if erase:
            names = []
            for item in items:
                print("delete", item.name)
                self.delete_by_name(table_type, item.name)
            self.save()
            self.session.add_all(items)
        else:
            # overwrite existing elements
            for item in items:
                existing_item = self.find(table_type, name=item.name).first()
                item.id = existing_item.id
                self.session.merge(item)
            self.save()

    def add(self, items):
        self.session.add_all(items)

    def save(self):
        self.session.commit()
        self.session.flush()

    def name(self, value):
        self.set_default("name", value, "global")

    def get_name(self):
        current = self.find(DEFAULT, name="name").first()
        if current is None:
            print("WARNING: name not set")
            return "namenotset"
        else:
            return current.value

    def next_name(self):
        from cloudmesh_client.cloud.mesh import Mesh
        name = self.get_name()
        return Mesh.next_name(name)

    def update_from_dict(self, d):

        content = dict(d)
        content["update"] = str(datetime.now())

        cm_id = content["cm_id"]
        cm_type = content["cm_type"]

        table = self.db.get_table(cm_type)
        e = self.find(table, cm_id=cm_id).first()
        if e is None:
            e = table()
            self.session.add_all([e])
            self.save()

        self.set(e, content)

    def set(self, element, d):
        for key in d:
            try:
                setattr(element, key, d[key])
            except Exception, e:
                print("WARNING:", key, "in table", element.__table__.name, "does not exist")
                print(e)
        self.save()

    def get_default(self, name, cloud=None):
        if cloud is None:
            cloud = "global"

        cm_id = self.getID("default", name, cloud)
        current = self.session.query(DEFAULT).filter_by(cm_id=cm_id).first()
        if current is None:
            return None
        else:
            result = self.o_to_d(current)
            return result["value"]

    def default(self, name, value, cloud=None):
        # find
        # deprecated, will be set_default in future
        # todo: Paulo find the default methoods, and replace with set_default

        self.set_default(name, value, cloud=cloud)

    def set_default(self, name, value, cloud=None):
        """
        sets a default variable

        :param name: name of the variable
        :param value:  the value
        :param cloud: the cloud, if no name is specified the name "global" is used
        :return:
        """
        if cloud is None:
            cloud = "global"

        element_id = self.getID("default", name, cloud)
        d = {
            "cm_cloud": cloud,
            "cm_type": "default",
            "cm_id": element_id,
            "name": name,
            "value": value
        }

        self.update_from_dict(d)

        """
        d = [DEFAULT(cloud=cloud, value=value)]
        current = self.session.query(DEFAULT).filter_by(name=key).first()
        if current is None:
            self.session.add_all(d)
        else:
            current.value = value
            current.cloud = cloud
            self.save()
        self.save()
        """

    @property
    def data(self):
        """
        returns the database session
        it is introduced as a compatiblity function
        it may be deprecated
        """
        return self.session

    def _convert_to_lists(self, **kwargs):
        args = {}
        for k in kwargs:
            arg = kwargs[k]
            print(arg, type(arg))
            if isinstance(arg, str):
                arg = [arg]
            args[k] = arg
        return args

    def _find_obj_from_clouds(self, table, clouds=None, cm_user=None):
        """
        returns all the servers from all clouds
        """
        arg = self._convert_to_lists(clouds=clouds, cm_user=cm_user)
        print(arg)
        result = {}
        for cloud in arg['clouds']:
            d = self.session.query(table).all()
            result[cloud] = self.object_to_dict(d)
        return dict(result)

    def servers(self, clouds=None, cm_user=None):
        """
        returns all the servers from all clouds

        :param clouds:
        :param cm_user:
        :return:
        """
        return self._find_obj_from_clouds(VM, clouds=clouds, cm_user=cm_user)

    def flavors(self, clouds=None, cm_user=None):
        """
        returns all the flavors from the various clouds

        :param clouds:
        :param cm_user:
        :return:
        """
        return self._find_obj_from_clouds(FLAVOR, clouds=clouds, cm_user=cm_user)

    def images(self, clouds=None, cm_user=None):
        """
        returns all the images from various clouds

        :param clouds:
        :param cm_user:
        :return:
        """
        return self._find_obj_from_clouds(IMAGE, clouds=clouds, cm_user=cm_user)

    def get_by_filter(self, table, **kwargs):
        """
        returns the database object that matches the filters submitted with kwargs

        :param table:
        :param kwargs:
        :return:
        """
        if len(kwargs) == 1:
            return self.session.query(table).filter_by(kwargs).all()
        else:
            print("YYYY", kwargs)

    def get(self, table):
        """
        returns the dict of the table
        :param table:
        :return:
        """
        return self.dict(table)

    def o_to_d(self, element):
        """
        converts a single object to a dictionary

        :param element:
        :return:
        """
        d = {}
        for column in element.__table__.columns:
            d[column.name] = getattr(element, column.name)
        return d

    def object_to_dict(self, obj):
        """
        converst the object to dict

        :param obj:
        :return:
        """
        result = dict()
        for u in obj:
            _id = u.cm_id
            values = {}
            for key in u.__dict__.keys():
                if not key.startswith("_sa"):
                    values[key] = u.__dict__[key]
            result[_id] = values
        return result

    def convert_query_to_dict(self, table):
        """
        tbd

        :param table:
        :return:
        """
        return self.object_to_dict(self.session.query(table).all())

    def all(self, table):
        d = {}
        elements = self.session.query(table).all()
        for element in elements:
            d[element.cm_id] = {}
            for key in element.__dict__.keys():
                if not key.startswith("_sa"):
                    d[element.cm_id][key] = str(element.__dict__[key])
        return d

    def dict(self, table):
        """
        returns a dict from all elements in the table

        :param table:
        :return:
        """
        return self.object_to_dict(self.session.query(table).all())

    def json(self, table):
        """
        returns a json representation from all elements in the table

        :param table:
        :return:
        """
        d = self.dict(table)
        return json.dumps(d)

    def list(self, kind, cloud=None, output=None):
        """

        :param kind:
        :param cloud:
        :return:
        """
        if cloud is None:
            # find all clouds
            clouds = ["india"]
        else:
            clouds = Parameter.expand(cloud)

        if type(kind) == str:
            table = database.get_table(kind)
        else:
            table = kind

        result = {}
        if cloud is None:
            result = self.session.query(table).all()
            result = self.object_to_dict(result)
        else:
            # TODO

            for cloud in clouds:
                result[cloud] = self.session.query(table).filter_by(cloud=cloud).all()
                result[cloud] = self.object_to_dict(result[cloud])
        return result

    def update(self, kinds, clouds):
        """
        GREGOR WORKS ON THIS
        updates the data in the database

        :param kind: vm, image, flavor
        :param cloud: name of the cloud
        :return:
        """
        if type(kinds) == str:
            kinds = Parameter.expand(kinds)
        if type(clouds) == str:
            clouds = Parameter.expand(clouds)

        for cloud in clouds:
            cloudname = cloud.lower()
            cloud = OpenStack_libcloud(cloud, cm_user=self.cm_user)

            for k in kinds:
                kind = k.lower()
                results = cloud.list(kind, output="flat")

                for element in results:
                    result = results[element]

                    result["cm_id"] = self.getID(kind, str(result["id"]), cloudname)
                    result["cm_type"] = kind
                    self.update_from_dict(result)
        self.save()

        '''
            group = "default"
            lister = None
            inserter = None

            if kind.lower() == "vm":
                inserter = Insert.vm
            elif kind.lower() in ["image"]:
                inserter = Insert.image
            elif kind.lower() in ["flavor", "size"]:
                inserter = Insert.flavor
            else:
                return


            for element in result:
                try:
                   existing = self.find_by_name(result[element]['name'])
                except:
                    existing = None

                print("XXXXX", result[element]['name'])
                r = inserter("india", self.cm_user, group, result[element], existing)

            self.save()
            # banner(kind, c="-")
            # pprint (result)

            # current = self.session.query(FLAVOR).filter_by(group="default").first()
            # print("UUUUU", current)
        '''

    """
    def get_flavor(self, cloud, name):
        cloud = OpenStack_libcloud(cloud, cm_user=self.cm_user)
        f = cloud.get_flavor(name, kind='libcloud')
    """

    def info(self, what=None, kind=None):
        """
        prints information about the database
        """
        count_result = {}
        if kind is None:
            kinds = "VM,FLAVOR,IMAGE,DEFAULT"
        else:
            kinds = Parameter.expand(kind)
        if what is None:
            infos = "table,count"
        else:
            infos = Parameter.expand(what)

        banner("Databse table information", c="-")
        inspector = inspect(self.db.engine)

        if "table" in infos:
            for table_name in inspector.get_table_names():
                if table_name.upper() in kinds:
                    print(table_name + ":")
                    for column in inspector.get_columns(table_name):
                        print("  ", column['name'], column['type'])

        sum = 0
        if "count" in infos:
            for table in [VM, FLAVOR, IMAGE, DEFAULT]:
                rows = self.session.query(table).count()
                name = str(table.name).replace(".name", "")
                count_result[name] = rows
                if name in kinds:
                    print("Count {:}: {:}".format(name, rows))
                sum = sum + rows
            count_result['sum'] = sum

        return count_result

    """
    def boot(self, cloud, cm_user, name, image, flavor, key, meta):
        cloud = OpenStack_libcloud(cloud, cm_user=self.cm_user)
        return cloud.boot(cloud, cm_user, name, image, flavor, key, meta)
    """


class CloudType:
    openstack = "openstack"
    azure = "azure"
    aws = "aws"
    eucalyptus = "eucalyptus"


class CloudObject:
    vm = "vm"
    image = "image"
    flavor = "flavor"


class KeyMapper(object):
    """
    stores a list of key tuples that are used to find matches in originating dicts
    """

    def __init__(self):
        self.db_keys = {}
        self.cloud_keys = {}

    def get_key_for_db(self, cloudobject, key_cloud):
        i = self.cloud_keys[cloudobject].index(key_cloud)
        return self.db_keys[cloudobject][i]

    def get_key_for_cloud(self, cloudobject, db):
        i = self.db_keys[cloudobject].index(db)
        return self.cloud_keys[cloudobject][i]

    def add_mapping(self, cloudobject, tupels):
        self.db_keys[cloudobject], self.cloud_keys[cloudobject] = zip(*tubels)

    def add_mapping_from_dict(self, cloudobject, d):
        tupels = [(k, v) for k, v in d.iteritems()]
        self.add_mapping(cloudobject, tupels)

    """
    def add(self, cloudobject, key_db, key_cloud):
        self.cloud_keys[cloudobject].append(key_cloud)
        self.db_keys[cloudobject].append(key_db)
    """

    def add_mapping_from_yaml(self, cloudobject, stream):
        d = yaml.load_all(stream)
        self.add_mapping_from_dict(cloudobject, d)


class Insert(object):
    @classmethod
    def undefined_keys(cls, element, d):
        """
        checks if in d are keys that are not in the database table element
        returns first a list with the defined and than a list with the undefined keys

        :param element: an instantiation of a database table element
        :param d: teh dict
        :return: list, list
        """
        defined = []
        undefined = []
        for key, value in d.iteritems():
            if hasattr(element, key):
                defined.append(key)
            else:
                undefined.append(key)
        return defined, undefined

    @classmethod
    def merge_dict(cls, element, d, mapping=None):
        if mapping is None:
            for key, value in d.iteritems():
                if hasattr(element, key):
                    setattr(element, key, value)
                else:
                    print("Warnnig: dict has d[{:}]: {:}, but key is not in the table {:}. Ignoring key"
                          .format(key, d[key], type(element).__name__))
        elif mapping:
            print("not yet implemented")
        return element

    @staticmethod
    def merge_two_dicts(a, b):
        """
        mergers the two dictionaries and returns a merged one

        :param a: dict
        :param b: dict
        :return: dict
        """
        c = a.copy()
        c.update(b)
        return c

    @staticmethod
    def merge_into(a, b, mapping, erase=False):
        """
        mergers the two dictionaries and returns a merged one

        :param a: dict
        :param b: dict
        :return: dict
        """
        if erase:
            result = {}
        else:
            result = dict(a)
        print(result)
        for key_to in mapping:
            try:
                key_from = mapping[key_to]
                result[key_to] = b[key_from]
            except:
                pass
        return result

    @classmethod
    def _data(cls, table, cloud, user, group, d, existing):
        """

        :type d: dict
        """
        print("_data", str(table), cloud, user, group)
        pprint(d)
        # this creates new object inseatd of mergin it into existing one
        if existing is None:
            f = table(d["name"])
        else:
            f = existing
        f = cls.merge_dict(f, d)
        f.cm_cloud = str(cloud)
        f.cm_user = user
        f.group = group
        cm = CloudmeshDatabase(cm_user="gregor")
        cm.add([f])
        cm.save()

    @classmethod
    def flavor(cls, cloud, user, group, d, existing):
        """

        :type d: dict
        """
        cls._data(database.get_table('flavor'), cloud, user, group, d, existing)

    @classmethod
    def image(cls, cloud, user, group, d, existing):
        """

        :type d: dict
        """
        cls._data(database.get_table('image'), cloud, user, group, d, existing)

    @classmethod
    def vm(cls, cloud, user, group, d, existing):
        """

        :type d: dict
        """
        cls._data(database.get_table('vm'), cloud, user, group, d, existing)


def main():
    cm = CloudmeshDatabase(cm_user="gregor")

    cm.info()
    print(cm.list(VM))


if __name__ == "__main__":
    main()
