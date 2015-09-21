from __future__ import print_function
from pprint import pprint
from cloudmesh_client.common.ConfigDict import Config
import os
import os.path
from cloudmesh_client.cloud.register import CloudRegister
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.common.tables import dict_printer


from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console


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
              list [--cloud=CLOUD]
              list [--cloud=CLOUD] default
              list [--cloud=CLOUD] vm
              list [--cloud=CLOUD] flavor
              list [--cloud=CLOUD] image

        """
        pprint(arguments)

        def get_kind():
            for k in ["vm", "image", "flavor", "default"]:
                if arguments[k]:
                    return k
            return "help"

        if arguments["--cloud"] is None:
            cloud = "india"

        cm = CloudmeshDatabase()
        kind = get_kind()
        if kind == "help":
            print("HELP HERE")
        else:
            cm.update(kind, "india")
            # result = cm.list(kind, output="flat")
            result = cm.list(kind, output="native")
            header = None
            order = None
            if kind == 'flavor':
                order = [
                    'cm_cloud',
                    'disk',
                    'ephemeral_disk',
                    'id',
                    'name',
                    'ram',
                    'vcpus'
                ]
            elif kind == 'image':
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
            print(dict_printer(result,
                               order=order,
                               header=header,
                               output="table",
                               sort_keys=True,
                               show_none=""))

            # d = cm.get(FLAVOR)
            # print("9999")
            # pprint(d)
            # print("8888")


if __name__ == '__main__':
    command = cm_shell_list()
    command.do_list("flavor")
