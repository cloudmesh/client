from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase

class CloudProviderOpenstackAPI(CloudProviderBase):
    cloud_type = "openstack"

    def __init__(self, cloud_name, cloud_details, user=None):
        super(CloudProviderOpenstackAPI, self).__init__(cloud_name, user=user)

        self.cloud_type = "openstack"
        self.kind = ["image", "flavor", "vm"]

        self.provider = None
        self.default_image = None
        self.default_flavor = None
        self.cloud = None
        self.cloud_details = None

        self.initialize(cloud_name, cloud_details)

    def initialize(self, cloudname, user=None):
        """
        reads the details for the initialization from the cloudname defined in the yaml file
        :param cloudname:
        :param user:
        :return:
        """
        Console.TODO("not yet implemented")

    def list_flavor(self, cloudname, **kwargs):
        Console.TODO("not yet implemented")

    def list_image(self, cloudname, **kwargs):
        Console.TODO("not yet implemented")

    def list_vm(self, cloudname, **kwargs):
        Console.TODO("not yet implemented")

    def list_secgroup_rules(self, cloudname):
        Console.TODO("not yet implemented")

    def list_secgroup(self, cloudname):
        Console.TODO("not yet implemented")

    def boot_vm(self,
                name,
                group=None,
                image=None,
                flavor=None,
                cloud=None,
                key=None,
                secgroup=None,
                meta=None,
                nics=None,
                **kwargs):
        Console.TODO("not yet implemented")

    def delete_vm(self, name, group=None, force=None):
        Console.TODO("not yet implemented")

    def assign_ip(self, name):
        Console.TODO("not yet implemented")

    #
    # All other must methods defined bellow so we can discuss
    #
