from __future__ import print_function
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security
import os
from pprint import pprint
from uuid import UUID
import re
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.common.ConfigDict import Config, ConfigDict
from cloudmesh_client.common.FlatDict import FlatDict
from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase

from cloudmesh_client.cloud.iaas.provider.libcloud.CloudProviderLibcloud import CloudProviderLibcloud

from cloudmesh_client.shell.console import Console


class CloudProviderLibcloudEC2(CloudProviderLibcloud):
    def __init__(self, cloud_name, cloud_details, user=None, flat=True):
        super(CloudProviderLibcloudEC2, self).__init__(cloud_name, cloud_details, user=user)
        self.flat = flat
        self.cloud_type = "libcloud"
        self.kind = ["image", "vm", "flavor", "key"]
        self.cloudname = cloud_name
        self.initialize(cloud_name)

    def initialize(self, cloudname, user=None):

        Console.info("Initializing libcloud-ec2 for " + cloudname)
        cls = get_driver(Provider.EC2)

        d = ConfigDict("cloudmesh.yaml")
        self.config = d["cloudmesh"]["clouds"][cloudname]
        credentials = self.config["credentials"]
        cm_type = self.config["cm_type"]

        ec2_access_key = credentials['EC2_ACCESS_KEY']
        ec2_secret_key = credentials['EC2_SECRET_KEY']
        if not cloudname == "aws":
            auth_url = credentials["EC2_URL"]
            searchobj = re.match(r'^http[s]?://(.+):([0-9]+)/([a-zA-Z/]*)',
                                 auth_url,
                                 re.M | re.I)
            path = None
            host = None
            port = None
            if searchobj:
                host = searchobj.group(1)
                port = searchobj.group(2)
                path = searchobj.group(3)

                Console.info("url : " + searchobj.group())
                Console.info("host: " + host)
                Console.info("port: " + port)
                Console.info("path: " + path)

                extra_args = {'path': path}
            else:
                Console.error("Authentication url incorrect: {}".format(auth_url))

            self.provider = cls(ec2_access_key,
                                ec2_secret_key,
                                host=host,
                                port=port,
                                **extra_args)
        else:
            Console.info("AWS INIT")
            self.provider = cls(ec2_access_key, ec2_secret_key)

    def create_node(self, **kwargs):
        """
        Create a VM instance.

        Reference: https://libcloud.readthedocs.io/en/latest/_modules/libcloud/compute/drivers/ec2.html#BaseEC2NodeDriver.create_node

        :keyword    name: the name of VM
        :type       name: ``str``

        :keyword    image: the name of vm image
        :type       name: :class:`NodeImage`

        :keyword    size: the size of vm instance
        :type       size: :class:`NodeSize`

        :keyword    ex_keyname: the keyname
        :type       name: ``str``
        """

        pprint("create_node call in aws")
        self.provider.create_node(name=kwargs['name'], image=kwargs['image'], size=kwargs['size'])

    def get_ips(self, name):

        vlist = self.provider.list_nodes()

        for vm in vlist:
            # [<Node: uuid=3793375fbc6577391486b0ae43b1d1fb303aa0c1, name=TBD-001, state=RUNNING, public_ips=['54.205.149.43'], private_ips=['10.164.162.29'], provider=Amazon EC2 ...>]
            if name == vm.uuid:
                return vm.public_ips[0]
        for vm in vlist:
            if name == vm.name:
                return vm.public_ips[0]
        return NULL
        
