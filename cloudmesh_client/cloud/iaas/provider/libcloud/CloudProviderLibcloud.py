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
from cloudmesh_client.shell.console import Console


class CloudProviderLibcloud(CloudProviderBase):
    debug = True

    def _print(self, o):
        if self.debug:

            pprint(o)
            for element in o:
                pprint(element.__dict__)

    def __init__(self, cloud_name, cloud_details, user=None, flat=True):
        super(CloudProviderLibcloud, self).__init__(cloud_name, user=user)
        self.flat = flat
        self.cloud_type = "libcloud"
        self.kind = ["image", "flavor", "vm", "key"]
        self.dbobject = ["libcloud_image", "libcloud_flavor", "libcloud_vm", "key"]

        self.default_image = None
        self.default_flavor = None
        self.cloud = None
        self.config = None
        self.provider = None

    def _list(self, f, cloudname, **kwargs):
        nodes = self.provider.f()
        self._print(nodes)
        d = self._to_dict(nodes)
        return d

    def list_key(self, cloudname, **kwargs):
        print("In list_key")
        print(self.provider)
        keys = self.provider.list_key_pairs()
        print(keys)
        self._print(keys)
        keys_dict = self._to_dict(keys)
        return keys_dict

    def list_vm(self, cloudname, **kwargs):
        # return self.list(self.provider.list_nodes, cloudnames, kwargs)
        pprint("In list_vm")
        nodes = self.provider.list_nodes()
        self._print(nodes)
        vm_dict = self._to_dict(nodes)
        return vm_dict

    def list_image(self, cloudname, **kwargs):
        # return self.list(self.provider.list_images, cloudnames, kwargs)
        print("In list_images of libcloud")
        images = self.provider.list_images()
        self._print(images)
        image_dict = self._to_dict(images)
        return image_dict

    def list_flavor(self, cloudname, **kwargs):
        # return self.list(self.provider.list_sizes, cloudnames, kwargs)
        print("In list_flavor of libcloud")
        sizes = self.provider.list_sizes()
        self._print(sizes)
        sizes_dict = self._to_dict(sizes)
        return sizes_dict

    # TODO: deprecated
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
            print("RRRR", name)

            if name in ["Node", "NodeImage", "NodeSize"]:
                result_type = name
                Console.info("{} type object received".format(name))
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
                    'cpu',
                    'ram',
                    'bandwidth',
                    'price',
                    'category',
                    'uuid',
                    'updated_at'
                ],
                'header': [
                    'Id',
                    'Name',
                    'User',
                    'cpu',
                    'RAM',
                    'bandwidth',
                    'price',
                    'Cloud',
                    'UUID',
                    'Updated'
                ]
            },
            'image': {
                'order': [
                    'id',
                    'name',
                    'category',
                    'image_type',
                    'state',
                    'uuid',
                    'updated_at',
                    'owner_id'
                ],
                'header': [
                    'id',
                    'name',
                    'cloud',
                    'image_type',
                    'state',
                    'uuid',
                    'updated_at',
                    'owner_id'
                ]
            },
            'vm': {
                'order': [
                    'id',
                    'uuid',
                    'label',
                    'status',
                    'public_ips',
                    'private_ips',
                    'image_name',
                    'key',
                    'availability',
                    'instance_type',
                    'user',
                    'category',
                    'updated_at'
                ],
                'header': [
                    'id',
                    'uuid',
                    'label',
                    'status',
                    'public_ips',
                    'private_ips',
                    'image_name',
                    'key',
                    'availability',
                    'instance_type',
                    'user',
                    'cloud',
                    'updated'
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
                    'cloud',
                    'updated'
                ],
                'header': [
                    "instance_name",
                    "floating_ip",
                    "floating_ip_pool",
                    "fixed_ip",
                    "floating_ip_id",
                    "instance_id",
                    'cloud',
                    'updated'
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
                    'created',
                    'updated'
                ],
            }
        }
        # TODO: bug, this only returns some og the attributes, but not all
        if kind in ["vm", "image", "flavor"]:
            order = layout[kind]['order']
            header = layout[kind]['header']
        else:
            order = None
            header = None

        return order, header

    def boot_vm(self,
                name,
                image=None,
                flavor=None,
                cloud=None,
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
        if cloud is None:
            Console.error("Cloud is not specified")
            return

        auth = NodeAuthPassword('mysecretpassword')
        # self.provider.create_node("test_node", auth=auth)
        if image is not None:
            image = self.get_image_by_id(image)
            pprint("Image Id")
            pprint(image)
        else:
            Console.error("Image Id not found")

        if flavor is not None:
            flavor = self.get_size_by_id(flavor)
            pprint("FLAVOR::")
            pprint(flavor)
        else:
            Console.error("valid Flavor Id not found")
        # flavor = self.provider.list_sizes()[2]
        # location = self.provider.list_locations()[0]
        # pprint(self.provider.features['create_node'])
        # create_args = dict()
        # create_args['image'] = image

        # Console.info("Demo start a VM:")
        # Console.info("Image selected :"+image.name)
        # Console.info("Flavor selected :"+flavor.name)
        # Console.info("Key :")
        # pprint(key)
        self.provider.create_node(name=name, image=image, size=flavor, ex_keyname=key)
        Console.info("VM boot up success.ok.")

    def delete_vm(self, name, group=None, force=None):
        """
            Delete a VM instance whose instance name is given by name
        :param name:
        :param group:
        :param force:
        :return:
        """
        pprint("Delete VM for "+name)
        nodes_list = self.provider.list_nodes()
        node_obj = None
        for node in nodes_list:
            if node.name == name:
                node_obj = node
                break
        if node_obj is not None:
            self.provider.destroy_node(node_obj)
            Console.info("VM delete success.ok.")
        else:
            Console.error("No valid node found with the name "+name)

    def add_key_to_cloud(self, name, public_key):
        """
        Method to add key to libcloud based clouds, typically a keypair for AWS EC2.
        :param name: Name of the keypair.
        :param public_key: public key string.
        :return:
        """

        keypair = self.provider.import_key_pair_from_string(name, key_material=public_key)
        Console.info("Uploading the key to libcloud. ok.")
        return keypair

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

    def create_sec_group(self, cloud, secgroup_name='default'):
        try:
            self.provider.ex_create_security_group(secgroup_name, "Default Security Group")
        except Exception as e:
            Console.info("create_sec_group exception." + e.args[0])

    def enable_ssh(self, cloud, secgroup_name='default'):
        if cloud == "aws":
            params = {'Action': 'AuthorizeSecurityGroupIngress',
                      'GroupName': secgroup_name,
                      'IpProtocol': 'tcp',
                      'FromPort': '22',
                      'ToPort': '22',
                      'CidrIp': '0.0.0.0/0'}
            try:
                self.provider.connection.request(self.provider.path, params=params).object
                Console.info("Permission added.ok")
            except Exception as e:
                if e.args[0].find("InvalidPermission.Duplicate") == -1:
                    Console.info("Permission already exists.ok")
        else:
            Console.error("Enable SSH not implemented for others")
