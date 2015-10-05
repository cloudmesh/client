from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudmeshProviderBase
from cloudmesh_client.common.todo import TODO

from novaclient import client


class CloudProviderOpenstack(CloudmeshProviderBase):

    def __init__(self, cloud_name, cloud_details):
        self.initialize(cloud_name, cloud_details)

    def initialize(self, cloud_name, cloud_details):
        self.cloud = cloud_name
        self.default_flavor = cloud_details["default"]["flavor"]
        self.default_image = cloud_details["default"]["image"]
        version = 2
        credentials = cloud_details["credentials"]
        self.nova = client.Client(version, credentials["OS_USERNAME"], credentials["OS_PASSWORD"],
                                  credentials["OS_TENANT_NAME"], credentials["OS_AUTH_URL"],
                                  credentials["OS_CACERT"])

    def mode(self, source):
        """
        Sets the source for the information to be returned. "db" and "cloud"
        :param source: the database can be queried in mode "db",
        the database can be bypassed in mode "cloud"
        """
        TODO.implement()

    def list(self):
        """
        Returns list of all the vm instances.
        :return:List of Servers
        """
        return self.nova.servers.list()

    def boot(self, name, image=None, flavor=None, cloud="India", key=None, secgroup=None, meta=None):
        """
        Spawns a VM instance on the cloud.
        If image and flavor passed as none, it would consider the defaults specified in cloudmesh.yaml.

        :param name: Name of the instance to be started
        :param image: Image id to be used for the instance
        :param flavor: Flavor to be used for the instance
        :param cloud: Cloud on which to spawn the machine. Defaults to 'India'.
        :param key: Key to be used for the instance
        :param secgroup: Security group for the instance
        :param meta: A dict of arbitrary key/value metadata to store for this server
        """
        if image is None:
            image = self.default_image
        if flavor is None:
            flavor = self.default_flavor

        self.nova.servers.create(name, image, flavor, meta=meta, key_name=key, security_groups=secgroup)

    def delete(self, name, group=None, force=None):
        """
        Deletes a machine on the target cloud indicated by the id
        :param id: Name or ID of the instance to be deleted
        :param group: Security group of the instance to be deleted
        :param force: Force delete option
        :return:
        """
        server = self.nova.servers.find(name=name)
        server.delete()

    def get_ips(self, name, group=None, force=None):
        """
        Returns the ip of the instance indicated by name_or_id
        :param name_or_id:
        :param group:
        :param force:
        :return: IP address of the instance
        """
        server = self.nova.servers.find(name=name)
        return self.nova.servers.ips(server)

    # TODO: define this
    def get_image(self, **kwargs):
        """
        finds the image based on a query
        TODO: details TBD
        """
        TODO.implement()

    # TODO: define this
    def get_flavor(self, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        TODO.implement()

    # TODO: define this
    def get_vm(self, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        TODO.implement()





