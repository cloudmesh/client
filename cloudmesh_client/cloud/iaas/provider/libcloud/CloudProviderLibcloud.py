import os
from pprint import pprint
from uuid import UUID
import re

from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.common.ConfigDict import Config, ConfigDict
from cloudmesh_client.common.FlatDict import FlatDict

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
        vm_dict=self._to_dict(nodes)

        for vm in vm_dict:
            pprint("VM "+vm)

    def _to_dict(self, libcloud_result):
        d = {}
        for index, value in enumerate(libcloud_result):
            # print "---"
            d[index] = dict(value.__dict__["_info"])
            if 'links' in d[index]:
                del d[index]['links']
            if 'server_links' in d[index]:
                del d[index]['server_links']

            # If flat dict flag set, convert to flatdict
            if self.flat is True:
                d[index] = dict(FlatDict(d[index]).dict)
            else:
                ValueError("TODO: we only support flat for now")
        return d

