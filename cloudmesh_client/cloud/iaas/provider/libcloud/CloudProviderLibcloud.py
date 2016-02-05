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

        for key, vm in enumerate(vm_dict):
            pprint("VM !!!!")
            pprint(vm)
        return vm_dict

    def _to_dict(self, libcloud_result):
        d = {}
        pprint("Before To Dict")
        pprint(libcloud_result[0])

        for index, nodeObj in enumerate(libcloud_result):
            d = {}
            d[index] = LibcloudDict.convert_libcloud_vm_to_dict(nodeObj)
            # pprint("Id:"+result.id)
            # d['uuid'] = result.id
            # pprint("name:"+result.name)
            # d['name'] = result.name
            # for private_ip in result.private_ips:
            #     pprint("private ip:"+private_ip)
            #     d['private_ips'] = result.name
        return d


