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

mapping_yaml = """
    vm:
        tbd: tbd
    image:    
        base_image_ref: base_image_ref
        cm_cloud: cm_cloud
        cm_update: cm_update
        cm_user: cm_user
        created: created
        description: description
        cloud_id: id
        image_location: image_location
        image_state: image_state
        image_type: image_type
        instance_type_ephemeral_gb: instance_type_ephemeral_gb
        instance_type_flavorid: instance_type_flavorid
        instance_type_id: instance_type_id
        instance_type_memory_mb: instance_type_memory_mb
        instance_type_name: instance_type_name
        instance_type_root_gb: instance_type_root_gb
        instance_type_rxtx_factor: instance_type_rxtx_factor
        instance_type_swap: instance_type_swap
        instance_type_vcpus: instance_type_vcpus
        instance_uuid: instance_uuid
        kernel_id: kernel_id
        minDisk: minDisk
        minRam: minRam
        name: name
        network_allocated: network_allocated
        owner_id: owner_id
        progress: progress
        ramdisk_id: ramdisk_id
        serverId: serverId
        status: status
        updated: updated
        user_id: user_id
    flavor:
        bandwidth: bandwidth
        cloud: cloud
        cm_id: cm_id
        cm_update: cm_update
        cm_user: cm_user
        cm_uuid: cm_uuid
        disk: disk
        ephemeral_disk: ephemeral_disk
        extra: extra
        group: group
        cloud_id: id
        internal_id: internal_id
        label: label
        name: name
        price: price
        ram: ram
        update: update
        uuid: uuid
        vcpus: vcpus
        swap: swap
    vm:
       access_ip: access_ip
       access_ipv6: access_ipv6
       availability_zone: availability_zone
       cm_cloud: cm_cloud
       cm_update: cm_update
       cm_user: cm_user
       config_drive: config_drive
       created: created
       disk_config: disk_config
       flavorId: flavorId
       hostId: hostId
       cloud_id: id
       image: image
       imageId: imageId
       key_name: key_name
       name: name
       password: password
       power_state: power_state
       private_ips: private_ips
       progress: progress
       public_ips: public_ips
       size: size
       state: state
       task_state: task_state
       tenantId: tenantId
       updated: updated
       uri: uri
       userId: userId
       vm_state: vm_state
       volumes_attached: volumes_attached
      """

class OpenStack_libcloud(object):
    def __init__(self, cloudname, cm_user=None):
        self.nodes = None
        self.flavors = None
        self.data = None
        self.images = None
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
