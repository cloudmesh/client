import os
from pprint import pprint
from uuid import UUID

from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.common.ConfigDict import Config, ConfigDict
from cloudmesh_client.common.FlatDict import FlatDict
from keystoneclient.auth.identity import v3
from keystoneclient import session
from novaclient import client
import requests
import getpass
from cloudmesh_client.shell.console import Console


class CloudProviderCometAPI(CloudProviderBase):
    cloud_type = "openstack"

    def __init__(self, cloud_name, cloud_details, user=None, flat=True):
        super(CloudProviderCometAPI, self).__init__(cloud_name, user=user)
        self.flat = flat
        self.cloud_type = "comet"
        self.kind = ["image", "flavor", "vm", "key", "group"]

        self.provider = None
        self.default_image = None
        self.default_flavor = None
        self.cloud = None
        self.cloud_details = None

        self.initialize(cloud_name, cloud_details)

    def initialize(self, cloudname, user=None):

        d = ConfigDict("cloudmesh.yaml")

        """
        self.cloud_details = d["cloudmesh"]["clouds"][cloudname]

        # pprint(self.cloud_details)

        self.cloud = cloudname
        self.default_flavor = self.cloud_details["default"]["flavor"]
        self.default_image = self.cloud_details["default"]["image"]
        self.tenant = self.cloud_details['credentials']['OS_TENANT_NAME']
        version = 2
        credentials = self.cloud_details["credentials"]
        cert = False
        if "OS_CACERT" in credentials:
            if credentials["OS_CACERT"] is not False:
                cert = Config.path_expand(credentials["OS_CACERT"])
        auth_url = credentials["OS_AUTH_URL"]
        ksversion = auth_url.split("/")[-1]
        """

        """
        # GitHub issue 101
        # mechanism to interactively ask for password
        # when OS_PASSWORD set as "readline",
        # or read os.environ if set as "env".
        os_password = credentials["OS_PASSWORD"]
        if os_password.lower() in ["readline", "read", "tbd"]:
            os_password = getpass.getpass()
        elif os_password.lower() == "env":
            os_password = os.environ.get("OS_PASSWORD", getpass.getpass())

        if "v2.0" == ksversion:
            self.provider = client.Client(
                version,
                credentials["OS_USERNAME"],
                os_password,
                credentials["OS_TENANT_NAME"],
                credentials["OS_AUTH_URL"],
                cert)
        elif "v3" == ksversion:
            sess = session.Session(auth=self._ksv3_auth(credentials),
                                   verify=cert)
            self.provider = client.Client(2, session=sess)
        """

    def list_flavor(self, cloudname, **kwargs):
        # d = self._to_dict(self.provider.flavors.list())
        return d

    def list_image(self, cloudname, **kwargs):
        # d = self._to_dict(self.provider.images.list())
        return d

    def list_vm(self, cloudname, **kwargs):

        return None

    def rename_vm(self, current_name, new_name):
        pass

    def list_ips(self, **kwargs):
        pass

    def list_console(self, name, length=None):
        server = self.provider.servers.get(name)
        log = server.get_console_output(length=None)
        return log

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

        return None

    def delete_vm(self, name, group=None, force=None):
        """
        Deletes a machine on the target cloud indicated by the id or name
        :param name: Name or ID of the instance to be deleted
        :param group: Security group of the instance to be deleted
        :param force: Force delete option
        :return:
        """
        return None

    def start_vm(self, name, group=None, force=None):
        """
        Starts a suspended machine on the target cloud indicated by the id or name
        :param name: Name or ID of the instance to be deleted
        :param group: Security group of the instance to be deleted
        :param force: Force delete option
        :return:
        """

        if self.isUuid(name):
            server = self.provider.servers.get(name)
        else:
            server = self.provider.servers.find(name=name)

        server.start()

    def stop_vm(self, name, group=None, force=None):
        """
        Stops a machine on the target cloud indicated by the id or name
        :param name: Name or ID of the instance to be deleted
        :param group: Security group of the instance to be deleted
        :param force: Force delete option
        :return:
        """

        if self.isUuid(name):
            server = self.provider.servers.get(name)
        else:
            server = self.provider.servers.find(name=name)

        server.stop()

    def get_ips(self, name, group=None, force=None):
        """
        Returns the ip of the instance indicated by name
        :param name:
        :param group:
        :param force:
        :return: IP address of the instance
        """
        if self.isUuid(name):
            server = self.provider.servers.get(name)
        else:
            server = self.provider.servers.find(name=name)

        return self.provider.servers.ips(server)

    def add_key(self, name, public_key):
        pass

    def delete_key(self, name):
        pass

    def get_image(self, **kwargs):
        pass


    def get_ip(self, **kwargs):
        pass

    def get_flavor(self, **kwargs):
        pass

    def get_vm(self, **kwargs):
        pass

    def attributes(self, kind):

        layout = {}

        if kind in layout:
            order = layout[kind]["order"]
            header = layout[kind]["header"]
        else:
            order = None
            header = None

        return order, header


# CloudProviderBase.register(CloudProviderOpenstackAPI)

if __name__ == "__main__":
    cloudname = 'kilo'
    d = ConfigDict("cloudmesh.yaml")
    cloud_details = d["cloudmesh"]["clouds"][cloudname]

    cp = CloudProviderCometAPI(cloudname, cloud_details)

    d = {'name': '390792c3-66a0-4c83-a0d7-c81e1c787710'}
    pprint(cp.list_quota(cloudname))

    pprint(cp.list_key(cloudname))

