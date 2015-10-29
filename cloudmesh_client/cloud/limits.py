import requests
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.tables import print_list
from cloudmesh_client.cloud.iaas.CloudProviderOpenstack import convert_to_dict
requests.packages.urllib3.disable_warnings()


class Limits(ListResource):

    @classmethod
    def list(cls, cloud, format, tenant):
        print ("AAAAAAXS")
        try:
            # set the environment variables
            nova = CloudProvider(cloud)

            # execute the command
            result = nova.limits.get(tenant_id=tenant)
            d= convert_to_dict(result)
            return print_list(d, output=format)
        except Exception, e:
            return e
