from cloudmesh_client.cloud.iaas.CloudProvider import set_os_environ
from cloudmesh_client.common import tables
from cloudmesh_base.Shell import Shell
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.TableParser import TableParser
from cloudmesh_client.cloud.nova import  Nova

# Note: This command is currently implemented using the nova command as we
# have not yet found how to print it from the api. We may want to do a rest
# call instead?

class Usage(ListResource):

    @classmethod
    def list(cls, cloud, start, end, tenant, format):
        # set the environment variables
        set_os_environ(cloud)
        print "HHHHHH"
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
            result = Nova.remove_subjectAltName_warning(result)

            #
            # TODO: for some reason the nova command has returned not the
            # first + char, so we could not ignore the line we may set - as
            # additional comment char, but that did not work
            #
            result = "\n".join(result.splitlines()[1:])
            parser = TableParser(comment_chars="+#-")
            d = parser.parse_to_dict(result)

            for line in result:
                if line.__contains__("Usage from"):
                    print(line)

            return tables.dict_printer(d, output=format)
        except Exception, e:
            return e