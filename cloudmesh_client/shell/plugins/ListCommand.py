from __future__ import print_function

from cloudmesh_client.cloud.list import List
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.default import Default


class ListCommand(object):
    topics = {"list": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command list")

    @command
    def do_list(self, args, arguments):
        """
        ::

            Usage:
                list [--cloud=CLOUD] [--format=FORMAT] [--user=USER] [--tenant=TENANT] default
                list [--cloud=CLOUD] [--format=FORMAT] [--user=USER] [--tenant=TENANT] vm
                list [--cloud=CLOUD] [--format=FORMAT] [--user=USER] [--tenant=TENANT] flavor
                list [--cloud=CLOUD] [--format=FORMAT] [--user=USER] [--tenant=TENANT] image

            List the items stored in the database

            Options:
                --cloud=CLOUD    the name of the cloud
                --format=FORMAT  the output format
                --tenant=TENANT     Name of the tenant, e.g. fg82.

            Description:
                List command prints the values stored in the database
                for [default/vm/flavor/image].
                Result can be filtered based on the cloud, user & tenant arguments.
                If these arguments are not specified, it reads the default

            Examples:
                $ list --cloud india default
                $ list --cloud india --format table flavor
                $ list --cloud india --user albert --tenant fg82 flavor
        """
        # pprint(arguments)

        # Method to get the kind from args
        #
        # TODO: the kind are defined in the provider,
        # TODO: keep the kind lower case
        # why is there a reason to make the gind upper case
        def get_kind():
            for k in ["vm", "image", "flavor", "default"]:
                if arguments[k]:
                    # kinds are all uppercase in model.py
                    return k.upper()
            return "help"

        # Read commandline arguments
        output_format = arguments['--format']
        cloud = arguments['--cloud']
        user = arguments['--user']
        tenant = arguments['--tenant']

        # If format is not specified, read default
        if output_format is None:
            output_format = Default.get("format") or "table"

        # If cloud is not specified, get default
        if cloud is None:
            cloud = Default.get("cloud") or "india"

        # If user is not specified, get default
        if user is None:
            user = Default.get("user")

        # If tenant is not specified, get default
        if tenant is None:
            tenant = Default.get("tenant")

        # Get the kind
        kind = get_kind()
        header = None
        order = None

        # print help message
        if kind == 'help':
            Console.ok("Print help!")
            return

        # Prepare the order & header based on kind
        # TODO: use lower case so we have a convention thats easy to follow
        # TODO: add quota
        # TODO: add limits
        # TODO: add usage
        if kind == 'FLAVOR':
            order = [
                'cm_cloud',
                'disk',
                'ephemeral_disk',
                'id',
                'name',
                'ram',
                'vcpus'
            ]
        elif kind == 'DEFAULT':
            order = ['user',
                     'cloud',
                     'name',
                     'value',
                     'created_at',
                     'updated_at'
                     ]
        elif kind == 'IMAGE':
            order = [
                'cm_cloud',
                'cm_user',
                'instance_type_ephemeral_gb',
                'instance_type_flavorid',
                'instance_type_id',
                'instance_type_memory_mb',
                'instance_type_name',
                'instance_type_root_gb',
                'instance_type_rxtx_factor',
                'instance_type_swap',
                'instance_type_vcpus',
                'minDisk',
                'minRam',
                'name',
            ]
            header = [
                'cloud',
                'user',
                'ephemeral_gb',
                'flavorid',
                'id',
                'memory_mb',
                'flavor',
                'root_gb',
                'rxtx_factor',
                'swap',
                'vcpus',
                'minDisk',
                'minRam',
                'name',
            ]

        # Get the result & print it
        result = List.list(kind,
                           cloud,
                           user,
                           tenant,
                           order,
                           header,
                           output_format)
        if result:
            print(result)
        else:
            Console.error("List empty for [{}] in the database!"
                          .format(kind))
        return


if __name__ == '__main__':
    command = cm_shell_list()
    command.do_list("flavor")
