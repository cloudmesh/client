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
        cls = get_driver(Provider.EC2_US_EAST)

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
