from cloudmesh_client.common.tables import attribute_printer, list_printer
from cloudmesh_client.cloud.limits import Limits
import requests
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.tables import print_list
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.iaas.CloudProviderOpenstack import convert_to_dict

requests.packages.urllib3.disable_warnings()


class Quota(ListResource):

    @classmethod
    def list(cls, cloud, tenant, output="table"):
        try:
            # set the environment variables
            nova = CloudProvider.get_environ(cloud)

            # execute the command
            result = nova.quotas.defaults(tenant)._info
            return attribute_printer(result, output=output)
        except Exception, e:
            import sys
            print(sys.exc_info()[0])
            return e
