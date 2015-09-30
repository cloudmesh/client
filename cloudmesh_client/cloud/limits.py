from cloudmesh_client.common import tables
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict
from novaclient import client
import requests
requests.packages.urllib3.disable_warnings()


class Limits(object):
    @classmethod
    def convert_to_dict(cls, openstack_result):
        d = {}
        for i, obj in enumerate(openstack_result.absolute):
            d[i] = {}
            d[i]["Name"], d[i]["Value"] = obj.name, obj.value
        return d

    @classmethod
    def set_os_environment(cls, cloudname):
        try:
            d = ConfigDict("cloudmesh.yaml")
            credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]
            nova = client.Client("2", credentials["OS_USERNAME"],
                                 credentials["OS_PASSWORD"],
                                 credentials["OS_TENANT_NAME"],
                                 credentials["OS_AUTH_URL"],
                                 Config.path_expand(credentials["OS_CACERT"]))
            return nova
        except Exception, e:
            raise Exception("Error in setting OS environment, {}".format(e))

    @classmethod
    def list_limits(cls, cloud, format, tenant):
        try:
            # set the environment variables
            nova = Limits.set_os_environment(cloud)

            # execute the command
            result = nova.limits.get(tenant_id=tenant)

            # print results in a format
            d = Limits.convert_to_dict(result)
            return tables.dict_printer(d, order=['Name',
                                                 'Value'],
                                       output=format)
        except Exception, e:
            return e
