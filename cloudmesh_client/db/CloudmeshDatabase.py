from __future__ import print_function

from cloudmesh_client.db.models import database, VM, FLAVOR, IMAGE, DEFAULT

from sqlalchemy.orm import sessionmaker
from cloudmesh_base.util import banner
from sqlalchemy import inspect
from cloudmesh_client.iaas.openstack_libcloud import OpenStack_libcloud
from cloudmesh_client.cloud.clouds import Cloud
from pprint import pprint

class CloudmeshDatabase(object):

    def __init__(self, cm_user=None):

        self.db = database()
        self.db.Base.metadata.create_all()
        self.session = self.connect()
        if cm_user is None:
            self.cm_user = getpass.getuser()
        else:
            self.cm_user = cm_user

    def connect(self):
        """

        :return:
        """
        Session = sessionmaker(bind=self.db.engine)
        self.session = Session()
        return self.session

    def find_vm_by_name(self, name):
        """

        :param name:
        :return:
        """
        return self.find(VM, name=name).first()

    def find(self, kind, **kwargs):
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
                t = database.get_table_from_name(k)
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
        if erase:
            names = []
            for item in items:
                print("delete", item.name)
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
        """
        return self._find_obj_from_clouds(VM, clouds=clouds, cm_user=cm_user)

    def flavors(self, clouds=None, cm_user=None):
        """
        returns all the flavors from the various clouds
        """
        return self._find_obj_from_clouds(FLAVOR, clouds=clouds, cm_user=cm_user)

    def images(self, clouds=None, cm_user=None):
        """
        returns all the images from various clouds
        """
        return self._find_obj_from_clouds(IMAGE, clouds=clouds, cm_user=cm_user)

    def get_by_filter(self, table, **kwargs):
        print("ZZZZ", kwargs)
        if len(kwargs) == 1:
            return self.session.query(table).filter_by(kwargs).all()
        else:
            print("YYYY", kwargs)

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

    def list(self, kind, cloud=None):
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
            table = database.get_table_from_name(kind)
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
        inserter = None

        if kind.lower() == "vm":
            inserter = Insert.vm
        elif kind.lower() in ["image"]:
            inserter = Insert.image
        elif kind.lower() in ["flavor", "size"]:
            inserter = Insert.flavor
        else:
            return

        result = cloud.list(kind.lower(), output="flat")

        for element in result:
            r = inserter("india", self.cm_user, group, result[element])

        self.save()
        # banner(kind, c="-")
        # pprint (result)

        # current = self.session.query(FLAVOR).filter_by(group="default").first()
        # print("UUUUU", current)

    """
    def get_flavor(self, cloud, name):
        cloud = OpenStack_libcloud(cloud, cm_user=self.cm_user)
        f = cloud.get_flavor(name, kind='libcloud')
    """

    def info(self, what=None, kind=None):

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

        if "count" in infos:
            for table in [VM, FLAVOR, IMAGE, DEFAULT]:
                rows = self.session.query(table).count()
                name = str(table.name).replace(".name", "")
                if name in kinds:
                    print("Count {:}: {:}".format(name, rows))

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

    def add(self, cloudobject, key_db, key_cloud):
        self.cloud_keys[cloudobject].append(key_cloud)
        self.db_keys[cloudobject].append(key_db)

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

                    if key == "id":
                        setattr(element, "cm_id", value)
                    else:
                        setattr(element, key, value)
                else:
                    print("Warnnig: dict has d[{:}]: {:}, but key is not in the table {:}. Ignoring key"
                          .format(key, d[key], type(element).__name__))
        elif mapping:
            print("not yet implemented")
        return element

    @classmethod
    def _data(cls, table, cloud, user, group, d):
        """

        :type d: dict
        """
        print("_data", str(table), cloud, user, group)
        pprint(d)
        f = table(d["name"])
        f = cls.merge_dict(f, d)
        f.cm_cloud = str(cloud)
        f.cm_user = user
        f.group = group
        cm = CloudmeshDatabase(cm_user="gregor")
        cm.add([f])
        cm.save()

    @classmethod
    def flavor(cls, cloud, user, group, d):
        """

        :type d: dict
        """
        cls._data(database.get_table_from_name('flavor'), cloud, user, group, d)

    @classmethod
    def image(cls, cloud, user, group, d):
        """

        :type d: dict
        """
        cls._data(database.get_table_from_name('image'), cloud, user, group, d)

    @classmethod
    def vm(cls, cloud, user, group, d):
        """

        :type d: dict
        """
        cls._data(database.get_table_from_name('vm'), cloud, user, group, d)


def main():
    cm = CloudmeshDatabase(cm_user="gregor")

    cm.info()
    print(cm.list(VM))



if __name__ == "__main__":
    main()

