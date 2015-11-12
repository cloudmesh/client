import requests
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.Printer import attribute_printer

requests.packages.urllib3.disable_warnings()


class Limits(ListResource):

    @classmethod
    def list(cls, cloud, output="table", tenant=None):
        try:
            provider = CloudProvider(cloud).provider
            result = provider.list_limits(tenant)["absolute"]
            return attribute_printer(result,
                                     header=["Name", "Value"],
                                     output=output)
        except Exception, e:
            return e
