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
            cert = None
            print (cloud)

            if cloud["cm_type"] == "openstack":
                credentials = cloud["credentials"]

                if "OS_CACERT" in credentials:
                    cert = Config.path_expand(credentials["OS_CACERT"])

                if cert is not None:
                    nova = client.Client("2", credentials["OS_USERNAME"],
                                         credentials["OS_PASSWORD"],
                                         credentials["OS_TENANT_NAME"],
                                         credentials["OS_AUTH_URL"],
                                         cert)
                else:
                    nova = client.Client("2", credentials["OS_USERNAME"],
                                         credentials["OS_PASSWORD"],
                                         credentials["OS_TENANT_NAME"],
                                         credentials["OS_AUTH_URL"])


                return nova
        except Exception, e:
            raise Exception("Error in getting environment"
                            " for cloud: {}, {}".format(cloudname, e))