from __future__ import print_function
import json
import os
import getpass
import socket

import pyaml

from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.vm import Vm
from cloudmesh_client.cloud.secgroup import SecGroup
from cloudmesh_client.cloud.group import Group
from cloudmesh_client.cloud.counter import Counter
from cloudmesh_client.default import Default
from cloudmesh_client.common.Printer import dict_printer, attribute_printer
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.ConfigDict import Username
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand


class VmCommand(PluginCommand, CloudPluginCommand):
    topics = {"vm": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command vm")

    # noinspection PyUnusedLocal
    @command
    def do_vm(self, args, arguments):
        """
        ::

            Usage:
                vm default [--cloud=CLOUD][--format=FORMAT]
                vm refresh [--cloud=CLOUD]
                vm boot [--name=NAME]
                        [--cloud=CLOUD]
                        [--image=IMAGE_OR_ID]
                        [--flavor=FLAVOR_OR_ID]
                        [--group=GROUP]
                        [--secgroup=SECGROUP]
                        [--key=KEY]
                        [--dryrun]
                vm start [NAME]...
                         [--group=GROUP]
                         [--cloud=CLOUD]
                         [--force]
                vm stop [NAME]...
                        [--group=GROUP]
                        [--cloud=CLOUD]
                        [--force]
                vm delete [NAME]...
                          [--group=GROUP]
                          [--cloud=CLOUD]
                          [--force]
                vm ip assign [NAME]...
                          [--cloud=CLOUD]
                vm ip show [NAME]...
                           [--group=GROUP]
                           [--cloud=CLOUD]
                           [--format=FORMAT]
                           [--refresh]
                vm login [NAME] [--user=USER]
                         [--ip=IP]
                         [--cloud=CLOUD]
                         [--key=KEY]
                         [--command=COMMAND]
                vm rename [NAME]...
                          [--new=NEWNAME]
                          [--cloud=CLOUD]
                vm list [NAME_OR_ID]
                        [--cloud=CLOUD|--all]
                        [--group=GROUP]
                        [--format=FORMAT]
                        [--refresh]
                vm status [--cloud=CLOUD]
                vm info [--cloud=CLOUD]
                        [--format=FORMAT]

            Arguments:
                COMMAND        positional arguments, the commands you want to
                               execute on the server(e.g. ls -a) separated by ';',
                               you will get a return of executing result instead of login to
                               the server, note that type in -- is suggested before
                               you input the commands
                NAME           server name. By default it is set to the name of last vm from database.
                NAME_OR_ID     server name or ID
                KEYPAIR_NAME   Name of the openstack keypair to be used to create VM. Note this is not a path to key.
                NEWNAME        New name of the VM while renaming.

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
                                 is the full path to the private key file
                --keypair_name=KEYPAIR_NAME   Name of the openstack keypair to be used to create VM.
                                              Note this is not a path to key.
                --user=USER      give the user name of the server that you want
                                 to use to login
                --name=NAME      give the name of the virtual machine
                --force          delete vms without user's confirmation
                --command=COMMAND
                                 specify the commands to be executed
                --new=NEWNAME    Specify the new name for a VM while renaming.
                                 By default, this will be set to <username>-<count> format.



            Description:
                commands used to boot, start or delete servers of a cloud

                vm default [options...]     Displays default parameters that are set for VM boot.
                vm boot [options...]        Boots servers on a cloud, user may specify
                                            flavor, image .etc, otherwise default values
                                            will be used, see how to set default values
                                            of a cloud: cloud help
                vm start [options...]       Starts a suspended or stopped vm instance.
                vm stop [options...]        Stops a vm instance .
                vm delete [options...]      delete servers of a cloud, user may delete
                                            a server by its name or id, delete servers
                                            of a group or servers of a cloud, give prefix
                                            and/or range to find servers by their names.
                                            Or user may specify more options to narrow
                                            the search
                vm floating_ip_assign [options...]   assign a public ip to a VM of a cloud
                vm ip show [options...]     show the ips of VMs
                vm login [options...]       login to a server or execute commands on it
                vm list [options...]        same as command "list vm", please refer to it
                vm status [options...]      Retrieves status of last VM booted on cloud and displays it.

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
                                    order=["network",
                                           "version",
                                           "addr"],
                                    output="table",
                                    sort_keys=True)
            else:
                return d

        """
        def list_vms_on_cloud(cloud="kilo", group=None, format="table"):

            Utility reusable function to list vms on the cloud.
            :param cloud:
            :param group:
            :param format:
            :return:

            _cloud = cloud
            _group = group
            _format = format

            cloud_provider = CloudProvider(_cloud).provider
            servers = cloud_provider.list_vm(_cloud)


            server_list = {}
            index = 0
            # TODO: Improve the implementation to display more fields if required.
            for server in servers:
                server_list[index] = {}
                server_list[index]["name"] = server.name
                server_list[index]["id"] = server.id
                server_list[index]["status"] = server.status
                index += 1


            # TODO: Get this printed in a table
            print("Print table")
            dict_printer(servers, output=_format)
        """

        # pprint(arguments)

        def _refresh():
            try:
                msg = "Refresh VMs for cloud {:}.".format(cloud)
                if Vm.refresh(cloud=cloud):
                    Console.ok("{:} OK.".format(msg))
                else:
                    Console.error("{:} failed".format(msg))
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(e)
                Console.error("Problem running VM refresh")

        cloud = arguments["--cloud"] or Default.get_cloud()

        if arguments["boot"]:
            name = None
            try:
                name = arguments["--name"]
                is_name_provided = True

                if name is None:
                    is_name_provided = False

                    count = Counter.get()
                    prefix = Username()

                    if prefix is None or count is None:
                        Console.error("Prefix and Count could not be retrieved correctly.")
                        return

                    # BUG THE Z FILL SHOULD BE detected from yaml file
                    name = prefix + "-" + str(count).zfill(3)

                # if default cloud not set, return error
                if not cloud:
                    Console.error("Default cloud not set.")
                    return ""

                image = arguments["--image"] or Default.get("image",
                                                            category=cloud)
                # if default image not set, return error
                if not image:
                    Console.error("Default image not set.")
                    return ""

                flavor = arguments["--flavor"] or Default.get("flavor",
                                                              category=cloud)
                # if default flavor not set, return error
                if not flavor:
                    Console.error("Default flavor not set.")
                    return ""

                group = arguments["--group"] or Default.get_group()

                # if default group not set, return error
                if not group:
                    group = "default"
                    Default.set_group(group)

                secgroup = arguments["--secgroup"] or Default.get(
                    "secgroup", category=cloud)
                # print("SecurityGrp : {:}".format(secgroup))
                secgroup_list = ["default"]
                if secgroup is not None:
                    secgroup_list.append(secgroup)

                key_name = arguments["--key"] or Default.get_key()
                # if default keypair not set, return error
                if not key_name:
                    Console.error("Default key not set.")
                    return ""

                if arguments["--dryrun"]:

                    data = {
                        "cloud": cloud,
                        "name": name,
                        "image": image,
                        "flavor": flavor,
                        "key_name": key_name,
                        "secgroup_list": secgroup_list,
                        "group": group
                    }
                    print (attribute_printer(data, output="table"))
                    msg = "dryrun info. OK."
                    Console.ok(msg)
                else:
                    vm_id = Vm.boot(cloud=cloud,
                                    name=name,
                                    image=image,
                                    flavor=flavor,
                                    key_name=key_name,
                                    secgroup_list=secgroup_list)
                    Default.set("last_vm_id", vm_id)
                    Default.set("last_vm_name", name)

                    # SHOULD WE NOT DO THIS BY DEFAULT EVEN IF WE SPECIFY THE NAME?
                    if is_name_provided is False:
                        # Incrementing count
                        Counter.incr()

                    # Add to group
                    if vm_id is not None:
                        Group.add(name=group, type="vm", id=name,
                                  category=cloud)

                    msg = "info. OK."
                    Console.ok(msg)

            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(e)
                Console.error("Problem booting instance {:}".format(name))

        elif arguments["default"]:
            try:
                count = Counter.get()
                prefix = Username()

                if prefix is None or count is None:
                    Console.error("Prefix and Count could not be retrieved correctly.")
                    return

                vm_name = prefix + "-" + str(count).zfill(3)
                data = {"name": vm_name,
                        "cloud": arguments["--cloud"] or Default.get_cloud()}
                for attribute in ["image", "flavor", "key", "login_key", "group", "secgroup"]:
                    data[attribute] = Default.get(attribute, category=cloud)
                output_format = arguments["--format"] or "table"
                print (attribute_printer(data, output=output_format))
                msg = "info. OK."
                Console.ok(msg)
                ValueError("default command not implemented properly. Upon "
                           "first install the defaults should be read from yaml.")
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(e)
                Console.error("Problem listing defaults")

        elif arguments["status"]:
            try:
                cloud_provider = CloudProvider(cloud).provider
                vm_list = cloud_provider.list_vm(cloud)
                print("Status of VM {} is {}".format(vm_list[0]["name"], vm_list[0]["status"]))
                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(e)
                Console.error("Problem retrieving status of the VM")

        elif arguments["info"]:
            try:
                cloud_provider = CloudProvider(cloud).provider
                vms = cloud_provider.list_vm(cloud)
                vm = vms[0]
                output_format = arguments["--format"] or "table"
                print (attribute_printer(vm, output=output_format))
                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(e)
                Console.error("Problem retrieving status of the VM")

        elif arguments["start"]:
            try:
                servers = arguments["NAME"]

                # If names not provided, take the last vm from DB.
                if servers is None or len(servers) == 0:
                    last_vm = Vm.get_last_vm(cloud=cloud)
                    if last_vm is None:
                        Console.error("No VM records in database. Please run vm refresh.")
                        return ""
                    name = last_vm["name"]
                    # print(name)
                    servers = list()
                    servers.append(name)

                group = arguments["--group"]
                force = arguments["--force"]

                # if default cloud not set, return error
                if not cloud:
                    Console.error("Default cloud not set.")
                    return ""
                Vm.start(cloud=cloud, servers=servers)

                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(e)
                Console.error("Problem starting instances")

        elif arguments["stop"]:
            try:
                servers = arguments["NAME"]

                # If names not provided, take the last vm from DB.
                if servers is None or len(servers) == 0:
                    last_vm = Vm.get_last_vm(cloud=cloud)
                    if last_vm is None:
                        Console.error("No VM records in database. Please run vm refresh.")
                        return ""
                    name = last_vm["name"]
                    # print(name)
                    servers = list()
                    servers.append(name)

                group = arguments["--group"]
                force = arguments["--force"]

                # if default cloud not set, return error
                if not cloud:
                    Console.error("Default cloud not set.")
                    return ""

                Vm.stop(cloud=cloud, servers=servers)

                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(e)
                Console.error("Problem stopping instances")

        elif arguments["refresh"]:

            _refresh()

        elif arguments["delete"]:
            try:
                servers = arguments["NAME"]

                # If names not provided, take the last vm from DB.
                if servers is None or len(servers) == 0:
                    last_vm = Vm.get_last_vm(cloud=cloud)
                    if last_vm is None:
                        Console.error("No VM records in database. Please run vm refresh.")
                        return ""
                    name = last_vm["name"]
                    servers = list()
                    servers.append(name)

                group = arguments["--group"]
                force = arguments["--force"]

                # if default cloud not set, return error
                if not cloud:
                    Console.error("Default cloud not set.")
                    return ""

                Vm.delete(cloud=cloud, servers=servers)

                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(e)
                Console.error("Problem deleting instances")

        elif arguments["ip"] and arguments["assign"]:
            vmids = arguments["NAME"]

            # If names not provided, take the last vm from DB.
            if vmids is None or len(vmids) == 0:
                last_vm = Vm.get_last_vm(cloud=cloud)
                if last_vm is None:
                    Console.error("No VM records in database. Please run vm refresh.")
                    return ""
                name = last_vm["name"]
                vmids = list()
                vmids.append(name)

            # if default cloud not set, return error
            if not cloud:
                Console.error("Default cloud not set.")
                return ""
            try:
                cloud_provider = CloudProvider(cloud).provider
                for sname in vmids:
                    floating_ip = cloud_provider.create_assign_floating_ip(
                        sname)
                    if floating_ip is not None:
                        print(
                            "Floating IP assigned to {:} successfully and it is: {:}".format(
                                sname, floating_ip))
                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(e)
                Console.error("Problem assigning floating ips.")

        elif arguments["ip"] and arguments["show"]:
            vmids = arguments["NAME"]

            # If names not provided, take the last vm from DB.
            if vmids is None or len(vmids) == 0:
                last_vm = Vm.get_last_vm(cloud=cloud)
                if last_vm is None:
                    Console.error("No VM records in database. Please run vm refresh.")
                    return ""
                name = last_vm["name"]
                vmids = list()
                vmids.append(name)

            group = arguments["--group"]
            output_format = arguments["--format"] or "table"
            refresh = arguments["--refresh"]

            # if default cloud not set, return error
            if not cloud:
                Console.error("Default cloud not set.")
                return ""

            try:
                cloud_provider = CloudProvider(cloud).provider
                for server in vmids:
                    ip_addr = cloud_provider.get_ips(server)

                    ipaddr_dict = Vm.construct_ip_dict(ip_addr, cloud)

                    print(
                        "IP Addresses of instance {:} are as follows:-".format(
                            server))
                    print(_print_dict_ip(ipaddr_dict, format=output_format))
                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(e)
                Console.error(
                    "Problem getting ip addresses for instance {:}".format(id))

        elif arguments["login"]:
            vm_names = arguments["NAME"]

            # If names not provided, take the last vm from DB.
            if vm_names is None or len(vm_names) == 0:
                last_vm = Vm.get_last_vm(cloud=cloud)
                if last_vm is None:
                    Console.error("No VM records in database. Please run vm refresh.")
                    return ""
                name = last_vm["name"]
            else:
                name = vm_names[0]

            print("Logging in into {:} machine...".format(name))

            user = arguments["--user"]

            # Get user if user argument not specified.
            if user is None:
                user_from_db = Vm.get_vm_login_user(name, cloud)
                user_suggest = user_from_db or getpass.getuser()
                user = raw_input("Enter the user to login (Default: {}):".format(user_suggest)) or user_suggest
                Vm.set_vm_login_user(name, cloud, user)

            ip = arguments["--ip"]
            commands = arguments["--command"]

            # if default cloud not set, return error
            if not cloud:
                Console.error("Default cloud not set.")
                return ""

            key = arguments["--key"] or Default.get("login_key",
                                                    category=cloud)
            if not key:
                Console.error("Default login_key not set.")
                return ""

            cloud_provider = CloudProvider(cloud).provider
            # print("Name : {:}".format(name))
            ip_addr = cloud_provider.get_ips(name)

            ip_addresses = []
            ipaddr_dict = Vm.construct_ip_dict(ip_addr, cloud)
            for entry in ipaddr_dict:
                ip_addresses.append(ipaddr_dict[entry]["addr"])

            if ip is not None:
                if ip not in ip_addresses:
                    print(
                        "ERROR: IP Address specified does not match with the host.")
                    return ""
            else:
                print("Determining IP Address to use with a ping test.")
                # This part assumes that the ping is allowed to the machine.
                for ipadd in ip_addresses:
                    print("Checking {:}...".format(ipadd))
                    try:
                        socket.gethostbyaddr(ipadd)
                        # ip will be set if above command is successful.
                        ip = ipadd
                    except socket.herror:
                        print("Cannot reach {:}.".format(ipadd))

            if ip is None:
                print("SORRY. Unable to connect to the machine")
                return ""
            else:
                print("IP to be used is: {:}".format(ip))

            SecGroup.enable_ssh(cloud=cloud)
            # print("COMMANDS : {:}".format(commands))

            # Constructing the ssh command to connect to the machine.
            sshcommand = "ssh"
            if key is not None:
                sshcommand += " -i {:}".format(key)
            sshcommand += " -o StrictHostKeyChecking=no"
            sshcommand += " {:}@{:}".format(user, ip)
            if commands is not None:
                sshcommand += " \"{:}\"".format(commands)

            # print(sshcommand)
            os.system(sshcommand)

        elif arguments["list"]:

            if arguments["--all"]:
                try:
                    _format = arguments["--format"] or "table"
                    d = ConfigDict("cloudmesh.yaml")
                    for cloud in d["cloudmesh"]["clouds"]:

                        if arguments["--refresh"] or Default.refresh():
                            _refresh()

                        print("Listing VMs on Cloud: {:}".format(cloud))
                        result = Vm.list(cloud=cloud, output_format=_format)
                        if result is not None:
                            print(result)
                        else:
                            print("Sorry. No data found with requested parameters in DB.")
                    msg = "info. OK."
                    Console.ok(msg)
                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    print(e)
                    Console.error("Problem listing all instances")
            else:

                # if default cloud not set, return error
                if not cloud:
                    Console.error("Default cloud not set.")
                    return ""

                try:
                    name_or_id = arguments["NAME_OR_ID"]
                    group = arguments["--group"]
                    _format = arguments["--format"] or "table"

                    # list_vms_on_cloud(cloud, group, _format)
                    if arguments["--refresh"] or Default.refresh():
                        _refresh()

                    result = Vm.list(name_or_id=name_or_id, cloud=cloud, output_format=_format)

                    if result is not None:
                        print(result)
                    else:
                        print("No data found with the requested parameters.")

                    msg = "info. OK."
                    Console.ok(msg)

                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    print(e)
                    Console.error(
                        "Problem listing instances on cloud {:}".format(cloud))

        elif arguments["rename"]:
            try:
                servers = arguments["NAME"]

                # If names not provided, take the last vm from DB.
                if servers is None or len(servers) == 0:
                    last_vm = Vm.get_last_vm(cloud=cloud)
                    if last_vm is None:
                        Console.error("No VM records in database. Please run vm refresh.")
                        return ""
                    name = last_vm["name"]
                    servers = list()
                    servers.append(name)

                # if default cloud not set, return error
                if not cloud:
                    Console.error("Default cloud not set.")
                    return ""

                new_name = arguments["--new"]
                is_name_provided = True

                # If the new name is not provided, make the new new name in format username-count.
                if new_name is None or len(new_name) == 0:

                    is_name_provided = False

                    count = Counter.get()
                    prefix = Username()

                    if prefix is None or count is None:
                        Console.error("Prefix and Count could not be retrieved correctly.")
                        return

                    # BUG THE Z FILL SHOULD BE detected from yaml file
                    new_name = prefix + "-" + str(count).zfill(3)

                Vm.rename(cloud=cloud, servers=servers, new_name=new_name)

                if is_name_provided is False:
                    # Incrementing count
                    Counter.incr()

                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                print(e)
                Console.error("Problem deleting instances")

        return ""

