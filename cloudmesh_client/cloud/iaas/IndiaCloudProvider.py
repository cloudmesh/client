from novaclient import client
from cloudmesh_client.common.ConfigDict import ConfigDict


class IndiaCloudProvider(object):

    def __init__(self):
        self.initialize()

    def initialize(self, cloud_name="india", user=None):
        self.set_os_environ()
        self.cloud = "India"
        version = 2
        self.nova = client.Client(version, self.credentials["OS_USERNAME"], self.credentials["OS_PASSWORD"],
                                  self.credentials["OS_TENANT_NAME"], self.credentials["OS_AUTH_URL"],
                                  self.credentials["OS_CACERT"])

    def set_os_environ(self, cloudname="india"):
        """Set os environment variables on a given cloudname"""
        try:
            d = ConfigDict("cloudmesh.yaml")
            self.credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]
        except Exception, e:
            print(e)

    def boot(self, name, image, flavor, cloud="India", key=None, secgroup=None, meta=None):
        """
        Spawns a VM instance on the cloud.

        :param name: Name of the instance to be started
        :param image: Image id to be used for the instance
        :param flavor: Flavor to be used for the instance
        :param cloud: Cloud on which to spawn the machine. Defaults to 'India'.
        :param key: Key to be used for the instance
        :param secgroup: Security group for the instance
        :param meta: A dict of arbitrary key/value metadata to store for this server
        """
        self.nova.servers.create(name, image, flavor, meta=meta, key_name=key, security_groups=secgroup)

    def delete(self, name_or_id, group=None, force=None):
        """

        :param name_or_id: Name or ID of the instance to be deleted
        :param group: Security group of the instance to be deleted
        :param force: Force delete option
        :return:
        """
        server = self.nova.servers.get(name_or_id)
        server.delete()
