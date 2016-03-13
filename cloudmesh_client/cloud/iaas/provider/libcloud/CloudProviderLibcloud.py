import os
from pprint import pprint
from uuid import UUID
import re

from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.common.ConfigDict import Config, ConfigDict
from cloudmesh_client.common.LibcloudDict import LibcloudDict
from libcloud.compute.base import NodeAuthPassword, NodeAuthSSHKey
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security


class CloudProviderLibcloud(CloudProviderBase):

    debug = True

    def _print(self, o):
        if self.debug:

            pprint (o)
            for element in o:
                pprint (element.__dict__)

    def __init__(self, cloud_name, cloud_details, user=None, flat=True):
        super(CloudProviderLibcloud, self).__init__(cloud_name, user=user)
        self.flat = flat
        self.cloud_type = "libcloud"
        self.kind = ["image", "flavor", "vm", "key"]
        self.default_image = None
        self.default_flavor = None
        self.cloud = None
        self.cloud_details = None
        self.provider = None

    def list_key(self, cloudname, **kwargs):
        pprint("In list_key")
        print (self.provider)
        keys = self.provider.list_key_pairs()
        print (keys)
        self._print(keys)
        keys_dict = self._to_dict(keys)
        return keys_dict

    def list_vm(self, cloudname, **kwargs):
        pprint("In list_vm")
        nodes = self.provider.list_nodes()
        self._print(nodes)
        vm_dict = self._to_dict(nodes)
        return vm_dict

    def list_image(self, cloudname, **kwargs):
        pprint("In list_images of libcloud")
        images = self.provider.list_images()
        self._print(images)
        image_dict = self._to_dict(images)
        return image_dict

    def list_flavor(self, cloudname, **kwargs):
        pprint("In list_flavor of libcloud")
        sizes = self.provider.list_sizes()
        self._print(sizes)
        sizes_dict = self._to_dict(sizes)
        return sizes_dict

    def list_size(self, cloudname, **kwargs):
        pprint("In list_sizes of libcloud")
        sizes = self.provider.list_sizes()
        self._print(sizes)
        sizes_dict = self._to_dict(sizes)
        return sizes_dict

    def _to_dict(self, libcloud_result):
        d = {}
        result_type = ""
        if len(libcloud_result) > 0:
            name = libcloud_result[0].__class__.__name__
            print ("RRRR", name)
            if  name == "Node":
                result_type = "Node"
                pprint("Node type object received")
            elif name == "NodeImage":
                result_type = "NodeImage"
                pprint("NodeImage type object received")
            elif name == "NodeSize":
                result_type = "NodeSize"
                pprint("NodeSize type object received")
        # pprint(libcloud_result[0])

        for index, obj in enumerate(libcloud_result):
            if result_type == "Node":
                d[index] = dict(LibcloudDict.convert_libcloud_vm_to_dict(obj))
            elif result_type == "NodeImage":
                d[index] = dict(LibcloudDict.handle_vm_image_details(obj))
            elif result_type == "NodeSize":
                d[index] = dict(LibcloudDict.handle_vm_size_details(obj))
            # pprint("Index:"+str(index))
        return d

    def attributes(self, kind):
        layout = {
            'flavor': {
                'order': [
                    'id',
                    'name',
                    'user',
                    'ram',
                    'os_flv_disabled',
                    'vcpus',
                    'swap',
                    'os_flavor_acces',
                    'rxtx_factor',
                    'os_flv_ext_data',
                    'disk',
                    'category',
                    'uuid'
                ],
                'header': [
                    'Id',
                    'Name',
                    'User',
                    'RAM',
                    'Disabled',
                    'vCPUs',
                    'Swap',
                    'Access',
                    'rxtx_factor',
                    'os_flv_ext_data',
                    'Disk',
                    'Cloud',
                    'UUID'
                ]
            },
            'image': {
                'order': [
                    'id',
                    'name',
                    'os_image_size',
                    'metadata__description',
                    'minDisk',
                    'minRam',
                    'progress',
                    'status',
                    'updated',
                    'uuid',
                    'category'
                ],
                'header': [
                    'id',
                    'name',
                    'size',
                    'description',
                    'minDisk',
                    'minRam',
                    'progress',
                    'status',
                    'updated',
                    'uuid',
                    'cloud'
                ]
            },
            'vm': {
                'order': [
                    'id',
                    'uuid',
                    'label',
                    'state',
                    'public_ips',
                    'private_ips',
                    'image_name',
                    'key_name',
                    'user',
                    'category'],
                'header': [
                    'id',
                    'uuid',
                    'label',
                    'status',
                    'public_ips',
                    'private_ips',
                    'image_name',
                    'key_name',
                    'user',
                    'cloud'
                ]
            },
            'floating_ip': {
                'order': [
                    "instance_name",
                    "ip",
                    "pool",
                    "fixed_ip",
                    "id",
                    "instance_id",
                    'cloud'
                ],
                'header': [
                    "instance_name",
                    "floating_ip",
                    "floating_ip_pool",
                    "fixed_ip",
                    "floating_ip_id",
                    "instance_id",
                    'cloud'
                ],
            },
            'floating_ip_pool': {
                'order': [
                    "name"
                ],
                'header': [
                    "floating_ip_pool"
                ],
            },
            'clouds': {
                'order': [
                    "cloud",
                    "status"
                ],
                'header': [
                    "cloud",
                    "status"
                ],
            },
            'limits': {
                'order': [
                    'Name',
                    'Value'
                ],
                'header': [
                    'Name',
                    'Value'
                ]
            },
            'quota': {
                'order': [
                    'Quota',
                    'Limit'
                ],
                'header': [
                    'Quota',
                    'Limit'
                ]
            },
            'secgroup': {
                'order': [
                    'id',
                    'name',
                    'category',
                    'user',
                    'project',
                    'uuid'
                ],
                'header': [
                    'id',
                    'secgroup_name',
                    'category',
                    'user',
                    'tenant_id',
                    'secgroup_uuid'
                ]
            },
            'default': {
                'order': [
                    'user',
                    'cloud',
                    'name',
                    'value',
                    'created_at',
                    'updated_at'
                     ],
                'header': [
                    'user',
                    'cloud',
                    'name',
                    'value',
                    'created_at',
                    'updated_at'
                     ],
            }
        }

        if kind == "vm":
            order = layout[kind]['order']
            header = layout[kind]['header']
        else :
            order = None
            header = None

        return order, header

    def boot_vm(self,
                name,
                image=None,
                flavor=None,
                cloud="kilo",
                key=None,
                secgroup=None,
                meta=None,
                nics=None,
                **kwargs):
        """
        Spawns a VM instance on the cloud.
        If image and flavor passed as none, it would consider the defaults specified in cloudmesh.yaml.

        :param name: Name of the instance to be started
        :param image: Image id to be used for the instance
        :param flavor: Flavor to be used for the instance
        :param cloud: Cloud on which to spawn the machine. Defaults to 'India'.
        :param key: Key to be used for the instance
        :param secgroup: Security group for the instance
        :param nics: TODO: fixme
        :param meta: A dict of arbitrary key/value metadata to store for this server
        """
        pprint("BOOTING UP THE VM")
        auth = NodeAuthPassword('mysecretpassword')
        # self.provider.create_node("test_node", auth=auth)
        if image:
            pprint("Image Id")
            pprint(image)
            image = self.get_image_by_id(image)
        else:
            pprint("valid Image Id not found")

        if flavor:
            flavor = self.get_size_by_id(flavor)

            if flavor:
                pprint("FLAVOR::")
                pprint(flavor)
        else:
            pprint("valid Flavor Id not found")
        # flavor = self.provider.list_sizes()[2]
        # location = self.provider.list_locations()[0]
        # pprint(self.provider.features['create_node'])
        # create_args = dict()
        # create_args['image'] = image

        self.provider.create_node(name=name, ex_iamprofile=name, image=image, size=flavor)

    def get_image_by_id(self, image_id):
        image_list = self.provider.list_images()
        for image in image_list:
            if image.id == image_id:
                return image
        raise ValueError("image id not found")
        return None

    def get_size_by_id(self, size_id):
        size_list = self.provider.list_sizes()
        for size in size_list:
            if size.id == size_id:
                return size
        raise ValueError("flavor id not found")
        # return None
