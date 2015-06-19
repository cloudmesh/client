from __future__ import print_function
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security
import datetime
import cloudmesh_client.db
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.ConfigDict import Config
from time import sleep
from pprint import pprint

from cloudmesh_client.common.FlatDict import key_prefix_replace, flatten
import cloudmesh_client.db.models

class Insert(object):

    @classmethod
    def merge_dict(cls, element, d):
        for key, value in d.iteritems():
            setattr(element, key, value)
        print ("CCCC", element.__dict__)
        return element

    @classmethod
    def _data(cls, table, cloud, user, group, d):
        """

        :type d: dict
        """
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



        # f.uuid =
        # f.cm_user =
        # f.cloud =
        # f.group =

        # id = Column(Integer, primary_key=True)
        # name = Column(String)
        # label = Column(String)
        # group = Column(String)
        # cm_uuid = Column(String)
        # cloud = Column(String)
        # cm_user = Column(String)
        # cm_update = Column(String)
        # uuid = Column(String)
        # bandwidth = Column(String)
        # update = Column(String)
        # disk = Column(String)
        # extra = Column(String)
        # internal_id = Column(String)
        # price = Column(String)
        # ram = Column(String)
        # vcpus = Column(String)

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


class OpenStack_libcloud(object):

    def __init__(self, cloudname, cm_user=None):
        self.cloudname = cloudname
        self.user = cm_user

        OpenStack = get_driver(Provider.OPENSTACK)
        self.credential = \
            ConfigDict("cloudmesh.yaml")['cloudmesh']['clouds'][cloudname]['credentials']

        libcloud.security.CA_CERTS_PATH = [Config.path_expand(self.credential['OS_CACERT'])]
        libcloud.security.VERIFY_SSL_CERT = True

        auth_url = "%s/tokens/" % self.credential['OS_AUTH_URL']

        self.driver = OpenStack(
            self.credential['OS_USERNAME'],
            self.credential['OS_PASSWORD'],
            ex_force_auth_url=auth_url,
            ex_tenant_name=self.credential['OS_TENANT_NAME'],
            ex_force_auth_version='2.0_password',
            ex_force_service_region='regionOne')

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
        print ("OOOOOO")
        pprint (result)
        print ("OOOOOO")

        if kind == "flat":
            if nodetype == "vm":
                result = OpenStack_libcloud.flatten_vms(result)
            elif nodetype == "images":
                result = OpenStack_libcloud.flatten_images(result)
        return result

    def list_nodes(self, kind=dict):
        self.nodes = self.driver.list_nodes()
        return self._list("vm", self.nodes, kind)

    def list_images(self, kind=dict):
        self.images = self.driver.list_images()
        return self._list("images", self.images, kind)

    def list_flavors(self, kind=dict):
        self.flavors = self.driver.list_sizes()
        return self._list("flavors", self.flavors, kind)

    def boot(self, cloud, user, name, image, flavor, key, meta):
        self.images = self.driver.list_images()
        self.flavors = self.driver.list_sizes()

        size = [s for s in self.flavors if s.name == flavor][0]
        image = [i for i in self.images if i.name == image][0]

        name = "{:}-{:}".format(user, "cm_test")
        node = dict(self.driver.create_node(name=name, image=image, size=size).__dict__)
        del node["_uuid"]
        del node["driver"]
        return node

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
