from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_base.Shell import Shell
from cloudmesh_client.common.Printer  import dict_printer
import os


class Quota(object):
    @classmethod
    def convert_to_dict(cls, openstack_result):
        d = {}
        count = 0
        for line in openstack_result.splitlines():
            if line.startswith("|") and ("Quota" and "Limit" not in line):
                d[count] = {}
                # for key Quota
                value_quota = line.strip().split("|")[1].strip()
                d[count]["Quota"] = value_quota
                # for key Limit
                value_limit = line.strip().split("|")[2].strip()
                d[count]["Limit"] = value_limit
            count += 1
        return d

    @classmethod
    def set_os_environment(cls, cloudname):
        try:
            d = ConfigDict("cloudmesh.yaml")
            credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]
            for key in credentials.keys():
                if key == "OS_CACERT":
                    os.environ[key] = Config.path_expand(credentials[key])
                else:
                    os.environ[key] = credentials[key]
        except Exception, e:
            print(e)

    @classmethod
    def list_quotas(cls, cloud, format):
        Quota.set_os_environment(cloud)
        result = Shell.execute("nova", "quota-show")
        d = Quota.convert_to_dict(result)
        return dict_printer(d, order=['Quota',
                                             'Limit'],
                                   output=format)
