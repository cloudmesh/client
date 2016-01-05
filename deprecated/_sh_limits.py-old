from cloudmesh_base.Shell import Shell
from cloudmesh_client.common.Printer  import dict_printer
from cloudmesh_client.cloud._sh_quota import Quota


class Limits(object):
    @classmethod
    def convert_to_dict(cls, openstack_result):
        filtered_lines = filter(lambda x:
                                x.startswith("|") and ("URI" not in x) and ("Name" not in x),
                                openstack_result.splitlines())
        d = {}
        for i, line in enumerate(filtered_lines):
            d[i] = {}
            value_name = line.split("|")[1]  # for key Name
            d[i]["Name"] = value_name.strip()

            value_used = line.split("|")[2]  # for key Used
            d[i]["Used"] = value_used.strip()

            value_max = line.split("|")[3]  # for key Max
            d[i]["Max"] = value_max.strip()
        return d

    @classmethod
    def list_limits(cls, cloud, format, tenant=" "):
        # set the environment variables
        Quota.set_os_environment(cloud)

        # execute the command
        args = ["limits","--tenant", tenant]
        result = Shell.execute("nova",args)

        # print results in a format
        if "ERROR" in result:
            return result
        else:
            d = Limits.convert_to_dict(result)
            return dict_printer(d, order=['Name',
                                                 'Used',
                                                 'Max'],
                                       output=format)