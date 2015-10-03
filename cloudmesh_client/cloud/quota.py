from cloudmesh_client.common import tables
from cloudmesh_client.cloud.limits import Limits
import requests
requests.packages.urllib3.disable_warnings()


class Quota(object):
    @classmethod
    def convert_to_dict(cls, openstack_result):
        d = {}
        for i, key in enumerate(openstack_result.keys()):
            d[i] = {}
            if "id" not in key:
                d[i]["Quota"], d[i]["Limit"] = key, openstack_result[key]
        return d

    @classmethod
    def list_quotas(cls, cloud, tenant, format):
        try:
            # set the environment variables
            nova = Limits.set_os_environment(cloud)

            # execute the command
            result = nova.quotas.defaults(tenant)._info

            # print results in a format
            d = Quota.convert_to_dict(result)
            return tables.dict_printer(d, order=['Quota',
                                                 'Limit'],
                                       output=format)
        except Exception, e:
            return e