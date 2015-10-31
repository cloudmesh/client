from cloudmesh_client.common.Printer import attribute_printer
import requests
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider

requests.packages.urllib3.disable_warnings()


class Quota(ListResource):

    @classmethod
    def list(cls, cloud, tenant, output="table"):
        try:
            nova = CloudProvider.set(cloud)
            result = nova.quotas.defaults(tenant)._info
            return attribute_printer(result, output=output)
        except Exception, e:
            import sys
            print(sys.exc_info()[0])
            return e
