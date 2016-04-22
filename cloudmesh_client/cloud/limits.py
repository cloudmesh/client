import requests
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.Printer import Printer

requests.packages.urllib3.disable_warnings()


class Limits(ListResource):

    @classmethod
    def list(cls, cloud, output="table", tenant=None):
        try:
            provider = CloudProvider(cloud).provider
            # if tenant is None:
            #     tenant = provider.tenant

            result = provider.list_limits(tenant)["absolute"]

            (order, header) = CloudProvider(cloud).get_attributes("limits")

            return Printer.attribute(result,
                                     header=header,
                                     output=output)
        except Exception as e:
            return e
