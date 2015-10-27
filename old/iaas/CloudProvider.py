__author__ = 'Gregor von Laszewski'

from cloudmesh_base.hostlist import Parameter
from cloudmesh_client.db.models import VM
from cloudmesh_client.db.models import DEFAULT
from cloudmesh_client.db.models import FLAVOR
from cloudmesh_client.db.models import IMAGE
from cloudmesh_client.db.models import database
from pprint import pprint
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase


class CloudProvider:
    # __metaclass__ = ABCMeta

    def __init(self, mapping, user, cloudname, credentials):
        self.mapper = self.setmap(mapping)
        self.cloudname = cloudname

    # ------------------------
    # KEY MAPPING
    # ------------------------

    def setmap(self, mapping):
        """

        :param mapping: dict with mapping
        """
        for cloudobject in mapping:
            self.mapper.add_mappping(cloudobject, mapping[cloudobject])
        return self.mapper

    def getkey_for_cloud(self, key_from_db):
        return self.mapper.get_key_for_cloud(key_form_db)

    def getkey_for_db(self, key_from_cloud):
        return self.mapper.get_key_for_db(key_form_cloud)

    # ------------------------
    # KEY MAPPING
    # ------------------------

    # @abstractmethod
    @classmethod
    def flatten_image(cls, d):
        """
        flattens the data from a single image returned with libcloud.

        :param d: the data for that image
        :type d: dict
        :return: the flattened dict
        :rtype: dict
        """
        n = key_prefix_replace(flatten(d), ["extra__metadata__", "extra__"], "")
        return n

    # @abstractmethod
    @classmethod
    def flatten_vm(cls, d):
        """
        flattens the data from a single vm returned by libloud

        :param d: the data for that vm
        :type d: dict
        :return: the flattened dict
        :rtype: dict
        """
        n = key_prefix_replace(flatten(d), ["extra__"], "")
        return n

    @classmethod
    def flatten_vms(cls, d):
        return cls.flatten(cls.flatten_vm, d)

    @classmethod
    def flatten_images(cls, d):
        return cls.flatten(cls.flatten_image, d)

    @classmethod
    def flatten(cls, transform, d):
        result = {}
        for element in d:
            n = transform(d[element])
            result[element] = dict(n)
        return result

    # ------------------------
    # LIST MANAGEMENT
    # ------------------------

    def _list(self, nodetype, nodes, kind=dict):
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + " UTC"
        result = None
        if kind == list:
            result = []
        elif kind in [dict, "flat"]:
            result = {}
        for node in nodes:
            values = dict(node.__dict__)
            del values["_uuid"]
            del values["driver"]
            values["cm_cloud"] = self.cloudname
            values["cm_update"] = now
            values["cm_user"] = self.user
            if kind == list:
                result.append(values)
            elif kind in [dict, "flat"]:
                result[values["id"]] = values

        if kind == "flat":
            if nodetype == "vm":
                result = OpenStack_libcloud.flatten_vms(result)
            elif nodetype == "image":
                result = OpenStack_libcloud.flatten_images(result)
            elif nodetype == "flavor":
                result = OpenStack_libcloud.flatten_flavor(result)
        return result

    def get_servers(self, clouds=None, cm_user=None):
        """
        returns all the servers from all clouds
        """
        return self._find_obj_from_clouds(VM, clouds=clouds, cm_user=cm_user)

    def get_flavors(self, clouds=None, cm_user=None):
        """
        returns all the flavors from the various clouds
        """
        return self._find_obj_from_clouds(FLAVOR, clouds=clouds, cm_user=cm_user)

    def get_images(self, clouds=None, cm_user=None):
        """
        returns all the images from various clouds
        """
        return self._find_obj_from_clouds(IMAGE, clouds=clouds, cm_user=cm_user)

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

    def list(self, kind, clouds, query, output="flat", mode="db"):
        result = {}
        if mode == "db":
            # get data from db
            pass
        else:
            self.images = self.driver.list()
            result = self._list(kind, self.images, output=output)
        return result

    def list_images(self, clouds, query, mode="db"):
        result = {}
        if mode == "db":
            # get data from db
            pass
        else:
            self.images = self.driver.list()
            result = self._list("image", self.images, kind)
        return result

    def list_flavors(self, clouds, query, mode="db"):
        result = {}
        if mode == "db":
            # get data from db
            pass
        else:
            self.flavors = self.driver.list_sizes()
            result = self._list("flavor", self.flavors, kind)
        return result

    def list_vms(self, clouds, query, mode="db"):
        result = {}
        if mode == "db":
            # get data from db
            pass
        else:
            self.nodes = self.driver.list_nodes()
            result = self._list("vm", self.nodes, kind)
        return result

    # @abstractmethod
    # def get_images(self, cloud):
    #    return {}

    # @abstractmethod
    # def get_flavors(self, cloud):
    #    return {}

    # @abstractmethod
    # def get_vms(self, cloud):
    #    return {}

    # ------------------------
    # UPDATE MANAGEMENT
    # ------------------------

    def update(self, clouds, cloudobject):
        """

        :param clouds: cloudnames from which the update is called either as Parameter string or list
        :type clouds: Parameter of cloud names
        :param cloudobject:  vm, images, or flavors specified in as Parameter string or list
        :type cloudobject: Parameter of CloudObjects

        :return:
        """
        kinds = Parameter.expand(cloudobject)
        for kind in kinds:
            if kind == "vm":
                pass
            elif kind == "flavor":
                pass
            elif kind == "image":
                pass

    def update_images(self, cloud):
        pass

    def update_flavors(self, cloud):
        pass

    def update_vms(self, cloud):
        pass

    # ------------------------
    # VM MANAGEMENT
    # ------------------------

    # @abstractmethod
    def boot(self, cloud, names, goup, label, image, flavor, key):
        return {}

    def delete(self, names):
        # find vms from names in db
        vms = none
        for vm in vms:
            # delete vm, pass multiple vms instead
            pass
        pass
