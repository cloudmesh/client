from abc import ABCMeta, abstractmethod
from cloudmesh_base.hostlist import Parameter

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