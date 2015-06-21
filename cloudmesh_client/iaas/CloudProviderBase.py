from abc import ABCMeta, abstractmethod
from cloudmesh_base.hostlist import Parameter
from cloudmesh_client.db.models import *

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
        if mapping == None:
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
        cm = cloudmesh_client.db.CloudmeshDatabase(cm_user="gregor")
        cm.add([f])
        cm.save()

    @classmethod
    def flavor(cls, cloud, user, group, d):
        """

        :type d: dict
        """
        cls._data(cloudmesh_client.db.models.FLAVOR, cloud, user, group, d)

    @classmethod
    def image(cls, cloud, user, group, d):
        """

        :type d: dict
        """
        cls._data(cloudmesh_client.db.models.IMAGE, cloud, user, group, d)

    @classmethod
    def vm(cls, cloud, user, group, d):
        """

        :type d: dict
        """
        cls._data(cloudmesh_client.db.models.VM, cloud, user, group, d)



class CloudProviderBase:

    __metaclass__ = ABCMeta

    def __init(self, mapping, user, cloudname, credentials):
        self.mapper = self.setmap(mapping)
        self.cloudname = cloudname

    def setmap(self, mapping):
        """

        :param mapping: dict with mapping
        """
        for cloudobject in mapping:
            self.mapper.add_mappping(cloudobject, mapping[cloudobject])
        return self.mapper

    def getkey_for_cloud(self, key_from_db):
        return self.mapper.get_key_for_cloud(key_form_db)

    @abstractmethod
    def getkey_for_db(self, key_from_cloud):
        return self.mapper.get_key_for_db(key_form_cloud)

    @abstractmethod
    def boot(self, cloud, names, goup, label, image, flavor, key):
        return {}

    def delete(self, names):
        pass

    def images(self, clouds, query, mode="db"):
        return {}

    def flavors(self, clouds, query, mode="db"):
        return {}

    def vms(self, clouds, query, mode="db"):
        return {}

    def update(self, clouds, cloudobject):
        """

        :param clouds: cloudnames from which the update is called either as Parameter string or list
        :type clouds: Parameter of cloud names
        :param cloudobject:  vm, images, or flavors specified in as Parameter string or list
        :type cloudobject: Parameter of CloudObjects

        :return:
        """
        pass

    def update_images(self, cloud):
        pass

    def update_flavors(self, cloud):
        pass

    def update_vms(self, cloud):
        pass

    @abstractmethod
    def get_images(self, cloud):
        return {}

    @abstractmethod
    def get_flavors(self, cloud):
        return {}

    @abstractmethod
    def get_vms(self, cloud):
        return{}