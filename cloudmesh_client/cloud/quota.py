from cloudmesh_client.common.Printer import Printer
import requests
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider

requests.packages.urllib3.disable_warnings()


class Quota(ListResource):

    @classmethod
    def list(cls, cloud, tenant, output="table"):
        try:

            provider = CloudProvider(cloud).provider

            result = provider.list_quota(cloud)

            (order, header) = CloudProvider(cloud).get_attributes("quota")

            return Printer.attribute(result,
                                     header=header,
                                     output=output)
        except Exception as e:
            import sys
            print(sys.exc_info()[0])
            return e
