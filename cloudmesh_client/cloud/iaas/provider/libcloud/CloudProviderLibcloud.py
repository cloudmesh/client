import os
from pprint import pprint
from uuid import UUID
import re

from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.common.ConfigDict import Config, ConfigDict
from cloudmesh_client.common.LibcloudDict import LibcloudDict

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security


class CloudProviderLibcloud(CloudProviderBase):

    def __init__(self, cloud_name, cloud_details, user=None, flat=True):
        super(CloudProviderLibcloud, self).__init__(cloud_name, user=user)
        self.flat = flat
        self.kind = "libcloud"
        self.default_image = None
        self.default_flavor = None
        self.cloud = None
        self.cloud_details = None
        self.provider = None

    def list_vm(self, cloudname, **kwargs):
        pprint("In list_vm")
        nodes = self.provider.list_nodes()
        vm_dict = self._to_dict(nodes)

        # for key, vm in enumerate(vm_dict):
            # pprint("VM !!!!")
            # pprint(vm)
        return vm_dict

    def list_image(self, cloudname, **kwargs):
        pprint("In list_images of libcloud")
        images = self.provider.list_images()
        image_dict = self._to_dict(images)

        # for key, image in enumerate(image_dict):
        #     # pprint("Images !!!!")
        #     pprint(vm)
        return image_dict

    def list_size(self, cloudname, **kwargs):
        pprint("In list_sizes of libcloud")
        sizes = self.provider.list_sizes()
        sizes_dict = self._to_dict(sizes)

        # for key, vm in enumerate(sizes_dict):
            # pprint("Images !!!!")
            # pprint(vm)
        return sizes_dict

    def _to_dict(self, libcloud_result):
        d = {}
        pprint("Before To Dict")
        result_type = ""
        if libcloud_result[0]:
            if libcloud_result[0].__class__.__name__ == "Node":
                result_type = "Node"
                pprint("Node type object received")
            elif libcloud_result[0].__class__.__name__ == "NodeImage":
                result_type = "NodeImage"
                pprint("NodeImage type object received")
            elif libcloud_result[0].__class__.__name__ == "NodeSize":
                result_type = "NodeSize"
                pprint("NodeSize type object received")
        # pprint(libcloud_result[0])

        for index, obj in enumerate(libcloud_result):
            d = {}
            if result_type == "Node":
                d[index] = dict(LibcloudDict.convert_libcloud_vm_to_dict(obj))
            elif result_type == "NodeImage":
                d[index] = dict(LibcloudDict.handle_vm_image_details(obj))
            elif result_type == "NodeSize":
                d[index] = dict(LibcloudDict.handle_vm_size_details(obj))
            pprint("Index:"+str(index))
            # pprint("Id:"+result.id)
            # d['uuid'] = result.id
            # pprint("name:"+result.name)
            # d['name'] = result.name
            # for private_ip in result.private_ips:
            #     pprint("private ip:"+private_ip)
            #     d['private_ips'] = result.name
        return d


