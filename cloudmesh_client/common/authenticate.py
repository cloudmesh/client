from novaclient import client
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict
import requests
requests.packages.urllib3.disable_warnings()


class Authenticate(object):

    @classmethod
    def get_environ(cls, cloudname):
        try:
            d = ConfigDict("cloudmesh.yaml")
            cloud = d["cloudmesh"]["clouds"][cloudname]

            if cloud["cm_type"] == "openstack":
                credentials = cloud["credentials"]
                nova = client.Client("2", credentials["OS_USERNAME"],
                                     credentials["OS_PASSWORD"],
                                     credentials["OS_TENANT_NAME"],
                                     credentials["OS_AUTH_URL"],
                                     Config.path_expand(credentials["OS_CACERT"]))
                return nova
        except Exception, e:
            raise Exception("Error in setting OS environment, {}".format(e))