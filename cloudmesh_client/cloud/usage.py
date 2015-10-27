from cloudmesh_client.common import tables
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_base.Shell import Shell
import os
# Note: This command would be implemented using the shell since openstack list isn't available as yet


class Usage(object):
    @classmethod
    def convert_to_dict(cls, openstack_result):
        filtered_lines = filter(lambda x:
                                x.startswith("|"),
                                openstack_result.splitlines())
        d = {0: {}}
        for key, value in zip(filtered_lines[0].split("|"), filtered_lines[1].split("|")):
            d[0][key] = value
        del d[0][""]
        return d

    @classmethod
    def set_os_environment(cls, cloudname):
        """Set os environment variables on a given cloudname"""
        try:
            d = ConfigDict("cloudmesh.yaml")
            credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]
            for key, value in credentials.iteritems():
                if key == "OS_CACERT":
                    os.environ[key] = Config.path_expand(value)
                else:
                    os.environ[key] = value
        except Exception, e:
            print(e)

    @classmethod
    def list(cls, cloud, start, end, tenant, format):
        # set the environment variables
        Usage.set_os_environment(cloud)
        try:
            # execute the command
            args = ["list"]
            if start:
                args.extend(["--start", start])
            if end:
                args.extend(["--end", end])
            if tenant:
                args.extend(["--tenant", tenant])

            result = Shell.execute("nova", args)

            d = Usage.convert_to_dict(result)

            for line in result.splitlines():
                if line.__contains__("Usage from"):
                    print(line)

            return tables.dict_printer(d, output=format)
        except Exception, e:
            return e