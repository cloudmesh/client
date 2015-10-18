from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.vm import Vm
from cloudmesh_client.cloud.group import Group
from cloudmesh_client.cloud.default import Default
from cloudmesh_client.common.tables import dict_printer
from cloudmesh_client.common.ConfigDict import ConfigDict
import json
import pyaml
import inspect


class VmCommand(object):

    topics = {"vm": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command vm")

    @command
    def do_vm(self, args, arguments):
        """
        ::

            Usage:
                vm start [--name=NAME]
                         [--count=COUNT]
                         [--cloud=CLOUD]
                         [--image=IMAGE_OR_ID]
                         [--flavor=FLAVOR_OR_ID]
                         [--group=GROUP]
                         [--secgroup=SECGROUP]
                vm delete [NAME...]
                          [--group=GROUP]
                          [--cloud=CLOUD]
                          [--force]
                vm ip_assign [NAME...]
                             [--cloud=CLOUD]
                vm ip_show [NAME...]
                           [--group=GROUP]
                           [--cloud=CLOUD]
                           [--format=FORMAT]
                           [--refresh]
                vm login NAME [--user=USER]
                         [--ip=IP]
                         [--cloud=CLOUD]
                         [--key=KEY]
                         [--command=COMMAND]
                vm list [--cloud=CLOUD|--all]
                        [--group=GROUP]
                        [--format=FORMAT]

            Arguments:
                COMMAND   positional arguments, the commands you want to
                          execute on the server(e.g. ls -a) separated by ';',
                          you will get a return of executing result instead of login to
                          the server, note that type in -- is suggested before
                          you input the commands
                NAME      server name

            Options:
                --ip=IP          give the public ip of the server
                --cloud=CLOUD    give a cloud to work on, if not given, selected
                                 or default cloud will be used
                --count=COUNT    give the number of servers to start
                --detail         for table print format, a brief version
                                 is used as default, use this flag to print
                                 detailed table
                --flavor=FLAVOR_OR_ID  give the name or id of the flavor
                --group=GROUP          give the group name of server
                --secgroup=SECGROUP    security group name for the server
                --image=IMAGE_OR_ID    give the name or id of the image
                --key=KEY        specify a key to use, input a string which
                                 is the full path to the public key file
                --user=USER      give the user name of the server that you want
                                 to use to login
                --name=NAME      give the name of the virtual machine
                --force          delete vms without user's confirmation
                --command=COMMAND
                                 specify the commands to be executed



            Description:
                commands used to start or delete servers of a cloud

                vm start [options...]       start servers of a cloud, user may specify
                                            flavor, image .etc, otherwise default values
                                            will be used, see how to set default values
                                            of a cloud: cloud help
                vm delete [options...]      delete servers of a cloud, user may delete
                                            a server by its name or id, delete servers
                                            of a group or servers of a cloud, give prefix
                                            and/or range to find servers by their names.
                                            Or user may specify more options to narrow
                                            the search
                vm ip_assign [options...]   assign a public ip to a VM of a cloud
                vm ip_show [options...]     show the ips of VMs
                vm login [options...]       login to a server or execute commands on it
                vm list [options...]        same as command "list vm", please refer to it

            Tip:
                give the VM name, but in a hostlist style, which is very
                convenient when you need a range of VMs e.g. sample[1-3]
                => ['sample1', 'sample2', 'sample3']
                sample[1-3,18] => ['sample1', 'sample2', 'sample3', 'sample18']

        """

        def _print_dict(d, header=None, format='table'):
            if format == "json":
                return json.dumps(d, indent=4)
            elif format == "yaml":
                return pyaml.dump(d)
            elif format == "table":
                return dict_printer(d,
                                    order=["id",
                                           "name",
                                           "status"],
                                    output="table",
                                    sort_keys=True)
            else:
                return d

        def _print_dict_ip(d, header=None, format='table'):
            if format == "json":
                return json.dumps(d, indent=4)
            elif format == "yaml":
                return pyaml.dump(d)
            elif format == "table":
                return dict_printer(d,
                                    order=["version",
                                           "addr"],
                                    output="table",
                                    sort_keys=True)
            else:
                return d

        def list_vms_on_cloud(cloud="india", group=None, format="table"):
            """
            Utility reusable function to list vms on the cloud.
            :param cloud:
            :param group:
            :param format:
            :return:
            """
            _cloud = cloud
            _group = group
            _format = format

            cloud_provider = Vm.get_cloud_provider(_cloud)
            servers = cloud_provider.list()

            server_list = {}
            index = 0
            # TODO: Improve the implementation to display more fields if required.
            for server in servers:
                server_list[index] = {}
                server_list[index]["name"] = server.name
                server_list[index]["id"] = server.id
                server_list[index]["status"] = server.status
                index += 1

            print(_print_dict(server_list, format=_format))

        # pprint(arguments)
        if arguments["start"]:
            try:
                name = arguments["--name"]
                # TODO: use count
                count = arguments["--count"]
                image = arguments["--image"]
                flavor = arguments["--flavor"]
                group = arguments["--group"] or \
                    Default.get("group")
                secgroup = arguments["--secgroup"]
                cloud = arguments["--cloud"] or \
                    Default.get("cloud")

                # if default cloud not set, return error
                if not cloud:
                    Console.error("Default cloud not set!")
                    return

                # if default group not set, return error
                if not group:
                    Console.error("Default group not set!")
                    return

                cloud_provider = Vm.get_cloud_provider(cloud)
                vm_id = cloud_provider.boot(name, image, flavor, secgroup=secgroup)
                print("Machine {:} is being booted on {:} Cloud...".format(name, cloud_provider.cloud))

                # Add to group
                Group.add(name=group, type="vm", id=vm_id, cloud=cloud)

            except Exception, e:
                import traceback
                print(traceback.format_exc())
                print (e)
                Console.error("Problem starting instance {:}".format(name))

        elif arguments["delete"]:
            try:
                id = arguments["NAME"]
                group = arguments["--group"]
                force = arguments["--force"]
                cloud = arguments["--cloud"] or \
                    Default.get("cloud")

                # if default cloud not set, return error
                if not cloud:
                    Console.error("Default cloud not set!")
                    return

                cloud_provider = Vm.get_cloud_provider(cloud)
                for server in id:
                    cloud_provider.delete(server)
                    print("Machine {:} is being deleted on {:} Cloud...".format(server, cloud_provider.cloud))
            except Exception, e:
                import traceback
                print(traceback.format_exc())
                print (e)
                Console.error("Problem deleting instance {:}".format(id))

        elif arguments["ip_assign"]:
            id = arguments["NAME"]
            cloud = arguments["--cloud"] or \
                Default.get("cloud")

            # if default cloud not set, return error
            if not cloud:
                Console.error("Default cloud not set!")
                return

            print("To be implemented")

        elif arguments["ip_show"]:
            id = arguments["NAME"]
            group = arguments["--group"]
            output_format = arguments["--format"] or "table"
            refresh = arguments["--refresh"]
            cloud = arguments["--cloud"] or \
                Default.get("cloud")

            # if default cloud not set, return error
            if not cloud:
                Console.error("Default cloud not set!")
                return

            try:
                cloud_provider = Vm.get_cloud_provider(cloud)
                for server in id:
                    ip_addr = cloud_provider.get_ips(server)

                    ipaddr = {}
                    print("IP Addresses of instance {:} are as follows:-".format(server))
                    for network in ip_addr:
                        ipaddr[network] = {}
                        index = 0
                        print("Network: {:}:-".format(network))
                        for ip in ip_addr[network]:
                            ipaddr[network][index] = {}
                            ipaddr[network][index]["version"] = ip["version"]
                            ipaddr[network][index]["addr"] = ip["addr"]
                            index += 1
                        print(_print_dict_ip(ipaddr[network], format=output_format))

            except Exception, e:
                import traceback
                print(traceback.format_exc())
                print (e)
                Console.error("Problem getting ip addresses for instance {:}".format(id))

        elif arguments["login"]:
            name = arguments["NAME"]
            user = arguments["--user"]
            ip = arguments["--ip"]
            key = arguments["--key"]
            commands = arguments["--command"]
            commands = commands.split(';')
            cloud = arguments["--cloud"] or \
                Default.get("cloud")

            # if default cloud not set, return error
            if not cloud:
                Console.error("Default cloud not set!")
                return

            print("To be implemented")

        elif arguments["list"]:
            if arguments["--all"]:
                try:
                    _format = arguments["--format"] or "table"
                    d = ConfigDict("cloudmesh.yaml")
                    for cloud in d["cloudmesh"]["clouds"]:
                        print("Listing VMs on Cloud: {:}".format(cloud))
                        list_vms_on_cloud(cloud, format=_format)
                except Exception, e:
                    import traceback
                    print(traceback.format_exc())
                    print (e)
                    Console.error("Problem listing all instances")
            else:
                cloud = arguments["--cloud"] or \
                        Default.get("cloud")

                # if default cloud not set, return error
                if not cloud:
                    Console.error("Default cloud not set!")
                    return

                try:
                    group = arguments["--group"]
                    _format = arguments["--format"] or "table"

                    list_vms_on_cloud(cloud, group, _format)

                except Exception, e:
                    import traceback
                    print(traceback.format_exc())
                    print (e)
                    Console.error("Problem listing instances on cloud {:}".format(cloud))
        pass


if __name__ == '__main__':
    command = cm_shell_vm()
    command.do_vm("list")
    command.do_vm("a=x")
    command.do_vm("x")
