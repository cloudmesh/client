import requests
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.tables import attribute_printer

requests.packages.urllib3.disable_warnings()


class Limits(ListResource):

    @classmethod
    def list(cls, cloud, output="table", tenant=None):
        try:
            nova = CloudProvider.get_environ(cloud)
            result = nova.limits.get(tenant_id=tenant)._info["absolute"]
            return attribute_printer(result, output=output)
        except Exception, e:
            return e
