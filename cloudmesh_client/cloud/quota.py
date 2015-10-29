from cloudmesh_client.common import tables
from cloudmesh_client.cloud.limits import Limits
import requests
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.tables import print_list
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.iaas.CloudProviderOpenstack import convert_to_dict

requests.packages.urllib3.disable_warnings()


class Quota(ListResource):

    @classmethod
    def list(cls, cloud, tenant, format):
        try:
            # set the environment variables
            nova = Limits.set_os_environment(cloud)

            # execute the command
            result = nova.quotas.defaults(tenant)._info

            # print results in a format
            d = convert_to_dict(result)
            return print_list(d, output=format)
        except Exception, e:
            return e
