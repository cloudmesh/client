from cloudmesh_client.cloud.iaas.CloudProviderOpenstackAPI import \
    set_os_environ
from cloudmesh_client.common.Printer  import dict_printer
from cloudmesh_base.Shell import Shell
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.TableParser import TableParser
from cloudmesh_client.cloud.nova import Nova


# Note: This command is currently implemented using the nova command as we
# have not yet found how to print it from the api. We may want to do a rest
# call instead?

class Usage(ListResource):
    @classmethod
    def list(cls, cloud, start, end, tenant, format):
    # TODO: consider named arguments
    #def list(cls, cloud, start=None,
    #         end=None, tenant=None, output="table"):
        # set the environment variables
        set_os_environ(cloud)
        try:
            # execute the command
            args = ["usage"]
            if start is not None:
                args.extend(["--start", start])
            if end is not None:
                args.extend(["--end", end])
            if tenant is not None:
                args.extend(["--tenant", tenant])

            result = Shell.execute("nova", args)
            result = Nova.remove_subjectAltName_warning(result)

            lines = result.splitlines()
            dates = lines[0]

            table = '\n'.join(lines[1:])

            dates = dates.replace("Usage from ", "").\
                replace("to", "").replace(" +", " ")[:-1].split()

            #
            # TODO: for some reason the nova command has returned not the
            # first + char, so we could not ignore the line we may set - as
            # additional comment char, but that did not work
            #
            d = TableParser.convert(result, comment_chars="+#")


            d["0"]["start"] = "start"
            d["0"]["end"] = "end"

            d["1"]["start"] = dates[0]
            d["1"]["end"] = dates[1]

            del d['0']

            return dict_printer(d,
                                       order=["start",
                                              "end",
                                              "servers",
                                              "cpu hours",
                                              "ram mb-hours",
                                              "disk gb-hours"],
                                       output=format)

        except Exception, e:
            return e
