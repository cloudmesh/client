from __future__ import print_function
import json
import os
import getpass
import socket

import pyaml
import time
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.vm import Vm
from cloudmesh_client.cloud.secgroup import SecGroup
from cloudmesh_client.cloud.network import Network
from cloudmesh_client.cloud.group import Group
from cloudmesh_client.cloud.counter import Counter
from cloudmesh_client.default import Default
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.ConfigDict import Username
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.common.Error import Error
from cloudmesh_client.common.LibcloudDict import LibcloudDict
from builtins import input
from cloudmesh_client.common.hostlist import Parameter
from cloudmesh_client.common.Shell import Shell
from pprint import pprint
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.cloud.image import Image
from cloudmesh_client.cloud.ip import Ip
from cloudmesh_client.common.util import search
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase

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
                vm refresh [all][--cloud=CLOUD]
                vm boot [--name=NAME]
                        [--cloud=CLOUD]
                        [--username=USERNAME]
                        [--image=IMAGE]
                        [--flavor=FLAVOR]
                        [--group=GROUP]
                        [--public]
                        [--secgroup=SECGROUP]
                        [--key=KEY]
                        [--dryrun]
                vm boot [--n=COUNT]
                        [--cloud=CLOUD]
                        [--username=USERNAME]
                        [--image=IMAGE]
                        [--flavor=FLAVOR]
                        [--group=GROUP]
                        [--public]
                        [--secgroup=SECGROUP]
                        [--key=KEY]
                        [--dryrun]
                vm ping [NAME] [N]
                vm console [NAME]
                         [--group=GROUP]
                         [--cloud=CLOUD]
                         [--force]
                vm start [NAMES]
                         [--group=GROUP]
                         [--cloud=CLOUD]
                         [--force]
                vm stop [NAMES]
                        [--group=GROUP]
                        [--cloud=CLOUD]
                        [--force]
                vm terminate [NAMES]
                          [--group=GROUP]
                          [--cloud=CLOUD]
                          [--force]
                vm delete [NAMES]
                          [--group=GROUP]
                          [--cloud=CLOUD]
                          [--keep]
                          [--dryrun]
                vm ip assign [NAMES]
                          [--cloud=CLOUD]
                vm ip show [NAMES]
                           [--group=GROUP]
                           [--cloud=CLOUD]
                           [--format=FORMAT]
                           [--refresh]
                vm ip inventory [NAMES]
                                [--header=HEADER]
                                [--file=FILE]
                vm ssh [NAME] [--username=USER]
                         [--quiet]
                         [--ip=IP]
                         [--cloud=CLOUD]
                         [--key=KEY]
                         [--command=COMMAND]
                vm rename [OLDNAMES] [NEWNAMES] [--force] [--dryrun]
                vm list [NAMES]
                        [--cloud=CLOUDS|--active]
                        [--group=GROUP]
                        [--format=FORMAT]
                        [--refresh]
                vm status [NAMES]
                vm wait [--cloud=CLOUD] [--interval=SECONDS]
                vm info [--cloud=CLOUD]
                        [--format=FORMAT]
                vm check NAME
                vm username USERNAME [NAMES] [--cloud=CLOUD]

            Arguments:
                COMMAND        positional arguments, the commands you want to
                               execute on the server(e.g. ls -a) separated by ';',
                               you will get a return of executing result instead of login to
                               the server, note that type in -- is suggested before
                               you input the commands
                NAME           server name. By default it is set to the name of last vm from database.
                NAMES          server name. By default it is set to the name of last vm from database.
                KEYPAIR_NAME   Name of the openstack keypair to be used to create VM. Note this is
                               not a path to key.
                NEWNAMES       New names of the VM while renaming.
                OLDNAMES       Old names of the VM while renaming.

            Options:
                --username=USERNAME  the username to login into the vm. If not specified it will be guessed
                                     from the image name and the cloud
                --ip=IP          give the public ip of the server
                --cloud=CLOUD    give a cloud to work on, if not given, selected
                                 or default cloud will be used
                --count=COUNT    give the number of servers to start
                --detail         for table print format, a brief version
                                 is used as default, use this flag to print
                                 detailed table
                --flavor=FLAVOR  give the name or id of the flavor
                --group=GROUP          give the group name of server
                --secgroup=SECGROUP    security group name for the server
                --image=IMAGE    give the name or id of the image
                --key=KEY        specify a key to use, input a string which
                                 is the full path to the private key file
                --keypair_name=KEYPAIR_NAME   Name of the openstack keypair to be used to create VM.
                                              Note this is not a path to key.
                --user=USER      give the user name of the server that you want
                                 to use to login
                --name=NAME      give the name of the virtual machine
                --force          rename/ delete vms without user's confirmation
                --command=COMMAND
                                 specify the commands to be executed


            Description:
                commands used to boot, start or delete servers of a cloud

                vm default [options...]
                    Displays default parameters that are set for vm boot either on the
                    default cloud or the specified cloud.

                vm boot [options...]
                    Boots servers on a cloud, user may specify flavor, image .etc, otherwise default values
                    will be used, see how to set default values of a cloud: cloud help

                vm start [options...]
                    Starts a suspended or stopped vm instance.

                vm stop [options...]
                    Stops a vm instance .

                vm delete [options...]
                    Delete servers of a cloud, user may delete a server by its name or id, delete servers
                    of a group or servers of a cloud, give prefix and/or range to find servers by their names.
                    Or user may specify more options to narrow the search

                vm floating_ip_assign [options...]
                    assign a public ip to a VM of a cloud

                vm ip show [options...]
                    show the ips of VMs

                vm ssh [options...]
                    login to a server or execute commands on it

                vm list [options...]
                    same as command "list vm", please refer to it

                vm status [options...]
                    Retrieves status of last VM booted on cloud and displays it.

            Tip:
                give the VM name, but in a hostlist style, which is very
                convenient when you need a range of VMs e.g. sample[1-3]
                => ['sample1', 'sample2', 'sample3']
                sample[1-3,18] => ['sample1', 'sample2', 'sample3', 'sample18']

            Quoting commands:
                cm vm login gvonlasz-004 --command=\"uname -a\"
        """

        """

        # terminate
        #  issues a termination to the cloud, keeps vm in database

        # delete
        #   issues a terminate if not already done
        #      (remember you do not have to go to cloud if state is already terminated)
        #   deletes the vm from database
        #


        # bulk rename

        rename abc[0-1] def[3-4]       renames the abc0,abc1 -> def3,def4

        if arguments["rename"]:
            oldnames = Parameter.expand(arguments["OLDNAME"])
            newnames = Parameter.expand(arguments["NEWNAME"])

            # check if new names ar not already taken
            # to be implemented

            if len(oldnames) == len(newnames):
                for i in range(0, len(oldnames)):
                    oldname = oldnames[i]
                    newname = newnames[i]
                if newname is None or newname == '':
                    print("New node name cannot be empty")
                else:
                    print(Cluster.rename_node(clusterid, oldname, newname))
        """

        cm = CloudmeshDatabase()

        def _print_dict(d, header=None, output='table'):
            return Printer.write(d, order=["id", "name", "status"], output=output, sort_keys=True)

        def _print_dict_ip(d, header=None, output='table'):
            return Printer.write(d, order=["network", "version", "addr"], output=output, sort_keys=True)

        def get_vm_name(name=None, offset=0, fill=3):

            if name is None:
                count = Default.get_counter(name='name') + offset
                prefix = Default.user
                if prefix is None or count is None:
                    Console.error("Prefix and Count could not be retrieved correctly.", traceflag=False)
                    return
                name = prefix + "-" + str(count).zfill(fill)
            return name

        def _refresh_cloud(cloud):
            try:
                msg = "Refresh VMs for cloud {:}.".format(cloud)
                if Vm.refresh(cloud=cloud):
                    Console.ok("{:} OK.".format(msg))
                else:
                    Console.error("{:} failed".format(msg), traceflag=False)
            except Exception as e:
                Console.error("Problem running VM refresh", traceflag=False)

        def _get_vm_names():

            vm_list  = cm.find(kind="vm")

            vms = [vm["name"] for vm in vm_list]

            names = pattern = arguments["NAMES"]
            if pattern is not None:
                if "*" in pattern:
                    names = search(vms, pattern)
                else:
                    names = Parameter.expand(names)

            if names == ['last'] or names is None:
                names == [Default.vm]

            return vm_list, names

        cloud = arguments["--cloud"] or Default.cloud

        config = ConfigDict("cloudmesh.yaml")
        active_clouds = config["cloudmesh"]["active"]

        def _refresh(cloud):
            all = arguments["all"] or None

            if all is None:

                _refresh_cloud(cloud)
            else:
                for cloud in active_clouds:
                    _refresh_cloud(cloud)

        arg = dotdict(arguments)

        arg.cloud = arguments["--cloud"] or Default.cloud
        arg.image = arguments["--image"] or Default.get(name="image", category=arg.cloud)
        arg.flavor = arguments["--flavor"] or Default.get(name="flavor", category=arg.cloud)
        arg.group = arguments["--group"] or Default.group
        arg.secgroup = arguments["--secgroup"] or Default.secgroup
        arg.key = arguments["--key"] or Default.key
        arg.dryrun = arguments["--dryrun"]
        arg.name = arguments["--name"]
        arg.format = arguments["--format"] or 'table'
        arg.refresh = Default.refresh or arguments["--refresh"]
        arg.count = int(arguments["--n"] or 1)
        arg.dryrun = arguments["--dryrun"]
        arg.verbose = not arguments["--quiet"]

        #
        # in many cases use NAMES
        # if arg.NAMES is not None:
        #   arg.names = Parameter.expand(arg.NAMES)   #  gvonlasz[001-002]  gives ["gvonlasz-001", "gvonlasz-002"]
        # else:
        #    arg.names = None
        #

        if arguments["boot"]:

            arg.username = arguments["--username"] or Image.guess_username(arg.image)
            is_name_provided = arg.name is not None

            arg.user = Default.user

            for index in range(0, arg.count):
                vm_details = dotdict({
                    "cloud": arg.cloud,
                    "name": get_vm_name(arg.name, index),
                    "image": arg.image,
                    "flavor": arg.flavor,
                    "key": arg.key,
                    "secgroup": arg.secgroup,
                    "group": arg.group,
                    "username": arg.username,
                    "user": arg.user
                })
                # correct the username
                vm_details.username = Image.guess_username_from_category(
                    vm_details.cloud,
                    vm_details.image,
                    username=arg.username)
                try:

                    if arg.dryrun:
                        print(Printer.attribute(vm_details, output=arg.format))
                        msg = "dryrun info. OK."
                        Console.ok(msg)
                    else:
                        vm_id = Vm.boot(**vm_details)

                        if vm_id is None:
                            msg = "info. failed."
                            Console.error(msg, traceflag=False)
                            return ""

                        # set name and counter in defaults
                        Default.set_vm(value=vm_details.name)
                        if is_name_provided is False:
                            Default.incr_counter("name")

                        # Add to group
                        if vm_id is not None:
                            Group.add(name=vm_details.group,
                                      species="vm",
                                      member=vm_details.name,
                                      category=vm_details.cloud)

                        msg = "info. OK."
                        Console.ok(msg)

                except Exception as e:
                    Console.error("Problem booting instance {name}".format(**vm_details), traceflag=False)

        elif arguments["username"]:

            arg.username = arguments["--username"] or Image.guess_username(arg.image)

            cloud = arg.cloud
            username = arg.USERNAME
            if arg.NAMES is None:
                names = [Default.vm]
            else:
                names = Parameter.expand(arg.NAMES)

            if len(names) == 0:
                return

            for name in names:
                arg.name = name
                Console.ok("Set username for {cloud}:{name} to {USERNAME}".format(**arg))
                Vm.set_login_user(name=name, cloud=cloud, username=username)

        elif arguments["default"]:
            try:
                count = Default.get_counter()
                prefix = Username()

                if prefix is None or count is None:
                    Console.error("Prefix and Count could not be retrieved correctly.", traceflag=False)
                    return

                vm_name = prefix + "-" + str(count).zfill(3)
                arg = {
                    "name": vm_name,
                    "cloud": arguments["--cloud"] or Default.cloud
                }
                for attribute in ["image", "flavor"]:
                    arg[attribute] = Default.get(name=attribute, category=cloud)
                for attribute in ["key", "group", "secgroup"]:
                    arg[attribute] = Default.get(name=attribute, category='general')

                output = arguments["--format"] or "table"
                print(Printer.attribute(arg, output=output))
                msg = "info. OK."
                Console.ok(msg)
                ValueError("default command not implemented properly. Upon "
                           "first install the defaults should be read from yaml.")
            except Exception as e:
                # Error.traceback(e)
                Console.error("Problem listing defaults", traceflag=False)

        elif arguments["ping"]:
            try:
                if arguments["NAME"] is None and arguments["N"] is None:
                    name = arguments["NAME"] or Default.vm
                    n = arguments["N"] or 1
                elif arguments["NAME"].isdigit():
                    n = arguments["NAME"]
                    name = Default.vm
                else:
                    name = arguments["NAME"] or Default.vm
                    n = arguments["N"] or 1

                print("Ping:", name, str(n))

                vm = dotdict(Vm.list(name=name, category=cloud, output="dict")["dict"])

                ip = vm.floating_ip

                result = Shell.ping(host=ip, count=n)
                print(result)

            except Exception as e:
                Console.error(e.message, traceflag=False)

        elif arguments["console"]:
            try:
                name = arguments["NAME"] or Default.vm

                vm = dotdict(Vm.list(name=name, category=cloud, output="dict")["dict"])

                cloud_provider = CloudProvider(cloud).provider
                vm_list = cloud_provider.list_console(vm.uuid)
                print(vm_list)
                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                # Error.traceback(e)
                Console.error("Problem retrieving status of the VM", traceflag=False)

        elif arguments["status"]:
            try:
                cloud_provider = CloudProvider(cloud).provider
                vm_list = cloud_provider.list_vm(cloud)

                vms = [vm_list[i]["name"] for i in vm_list ]
                print ("V", vms)

                pattern = arguments["NAMES"]
                if pattern is not None:
                    if "*" in pattern:
                        print ("serach")
                        names  = search(vms, pattern)
                    else:
                        names = Parameter.expand()
                    for i in vm_list:
                        if vm_list[i]["name"] in names:
                            print("{} {}".format(vm_list[i]["status"], vm_list[i]["name"]))
                else:
                    print("{} {}".format(vm_list[0]["status"], vm_list[0]["name"]))
            except Exception as e:
                # Error.traceback(e)
                Console.error("Problem retrieving status of the VM", traceflag=True)
        elif arguments["wait"]:
            interval = arguments["--interval"] or 5
            try:
                cloud_provider = CloudProvider(cloud).provider
                for i in range(1,10):
                    vm_list = cloud_provider.list_vm(cloud)
                    time.sleep(float(1))
                    d = {}
                    for id in vm_list:
                        vm = vm_list[id]
                        d[vm["name"]] = vm["status"]
                    print (d)
                    print("{} {}".format(vm_list[0]["status"], vm_list[0]["name"]))
                    if vm_list[0]["status"] in ['ACTIVE']:
                        return
            except Exception as e:
                # Error.traceback(e)
                Console.error("Problem retrieving status of the VM", traceflag=True)

        elif arguments["info"]:
            try:
                cloud_provider = CloudProvider(cloud).provider
                vms = cloud_provider.list_vm(cloud)
                vm = vms[0]
                output_format = arguments["--format"] or "table"
                print(Printer.attribute(vm, output=output_format))
                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                # Error.traceback(e)
                Console.error("Problem retrieving status of the VM", traceflag=False)

        elif arguments["check"]:

            test = {}
            try:

                names = Parameter.expand(arguments["NAME"])
                id = 0
                for name in names:
                    print("Not implemented: {}".format(name))
                    # TODO: check the status of the vms
                    status = "active"
                    # TODO: check if they have a floating ip
                    # TODO: get ip
                    floating_ip = "127.0.0.1"
                    ip = True
                    # ping
                    # TODO: ping the machine with the shell command
                    ping = True
                    # check if one can login and run a command
                    check = False
                    try:
                        r = Shell.execute("uname", "-a")
                        # do a real check
                        check = True
                    except:
                        check = False
                    test[name] = {
                        "id": id,
                        "name": name,
                        "status": status,
                        "ip": ip,
                        "ping": ping,
                        "login": check
                    }
                    id += 1

                pprint(test)

                print(Printer.write(test,
                                    order=["id",
                                           "name",
                                           "status",
                                           "ip",
                                           "ping",
                                           "login"],
                                    output="table",
                                    sort_keys=True))

                msg = "not yet implemented. failed."
                Console.error(msg, traceflag=False)
            except Exception as e:
                # Error.traceback(e)
                Console.error("Problem retrieving status of the VM", traceflag=False)

        elif arguments["start"]:
            try:
                servers = Parameter.expand(arguments["NAMES"])

                # If names not provided, take the last vm from DB.
                if len(servers) == 0:
                    last_vm = Default.vm
                    if last_vm is None:
                        Console.error("No VM records in database. Please run vm refresh.", traceflag=False)
                        return ""
                    name = last_vm["name"]
                    # print(name)
                    servers = list()
                    servers.append(name)

                group = arguments["--group"]
                force = arguments["--force"]

                # if default cloud not set, return error
                if not cloud:
                    Console.error("Default cloud not set.", traceflag=False)
                    return ""

                Vm.start(cloud=cloud, servers=servers)

                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                # Error.traceback(e)
                Console.error("Problem starting instances", traceflag=False)

        elif arguments["stop"]:
            try:
                servers = Parameter.expand(arguments["NAMES"])

                # If names not provided, take the last vm from DB.
                if servers is None or len(servers) == 0:
                    last_vm = Default.vm
                    if last_vm is None:
                        Console.error("No VM records in database. Please run vm refresh.", traceflag=False)
                        return ""
                    name = last_vm["name"]
                    # print(name)
                    servers = list()
                    servers.append(name)

                group = arguments["--group"]
                force = arguments["--force"]

                # if default cloud not set, return error
                if not cloud:
                    Console.error("Default cloud not set.", traceflag=False)
                    return ""

                Vm.stop(cloud=cloud, servers=servers)

                msg = "info. OK."
                Console.ok(msg)
            except Exception as e:
                # Error.traceback(e)
                Console.error("Problem stopping instances", traceflag=False)

        elif arguments["refresh"]:

            _refresh(cloud)

        elif arguments["delete"]:

            dryrun = arguments["--dryrun"]
            group = arguments["--group"]
            force = not arguments["--keep"]
            cloud = arguments["--cloud"]
            vms, servers = _get_vm_names()

            if servers in [None, []]:
                Console.error("No vms found.", traceflag=False)
                return ""

            for server in servers:
                if dryrun:
                    Console.ok("Dryrun: delete {}".format(server))
                else:
                   Vm.delete(servers=[server], force=force)

            return ""

        elif arguments["ip"] and arguments["assign"]:
            if arguments["NAMES"] is None:
                names = [Default.vm]
            else:
                names = Parameter.expand(arguments["NAMES"])

            for name in names:

                # ip = Network.get_floatingip(....)

                vm = dotdict(Vm.list(name=name, category=cloud, output="dict")["dict"])

                if vm.floating_ip is None:

                    Console.ok("Assign IP to {}".format(name))

                    try:
                        floating_ip = Network.find_assign_floating_ip(cloudname=cloud,
                                                                      instance_id=name)

                        Vm.refresh(cloud=cloud)

                        if floating_ip is not None:
                            print(
                                "Floating IP assigned to {:} is {:}".format(
                                    name, floating_ip))
                            msg = "info. OK."
                            Console.ok(msg)
                    except Exception as e:

                        Console.error("Problem assigning floating ips.", traceflag=False)

                else:
                    Console.error("VM {} already has a floating ip: {}".format(name, vm.floating_ip), traceflag=False)


        elif arguments["ip"] and arguments["inventory"]:

            vms, names = _get_vm_names()

            if names in [None, []]:
                if str(Default.vm) in ['None', None]:
                    Console.error("The default vm is not set.", traceflag=False)
                    return ""
                else:
                    names = [Default.vm]

            header = arguments["--header"] or "[servers]"
            filename = arguments["--file"] or "inventory.txt"

            try:
                vm_ips = []
                for vm in vms:
                    if  vm["name"] in names:
                        print (vm["name"])
                        vm_ips.append(vm["floating_ip"])

                result = header + "\n"

                result += '\n'.join(vm_ips)
                Console.ok("Creating inventory file: {}".format(filename))

                Console.ok(result)

                with open(filename, 'w') as f:
                    f.write(result)



            except Exception as e:
                Console.error("Problem getting ip addresses for instance", traceflag=True)

        elif arguments["ip"] and arguments["show"]:
            if arguments["NAMES"] is None:
                if str(Default.vm) in ['None', None]:
                    Console.error("The default vm is not set.", traceflag=False)
                    return ""
                else:
                    names = [Default.vm]
            else:
                names = Parameter.expand(arguments["NAMES"])

            group = arguments["--group"]
            output_format = arguments["--format"] or "table"
            refresh = arguments["--refresh"]

            try:

                ips = Ip.list(cloud=arg.cloud, output=output_format, names=names)
                print(ips)
            except Exception as e:
                Console.error("Problem getting ip addresses for instance", traceflag=False)

        elif arguments["ssh"]:

            def _print(msg):
                if arg.verbose:
                    Console.msg(msg)

            chameleon = "chameleon" in ConfigDict(filename="cloudmesh.yaml")["cloudmesh"]["clouds"][arg.cloud][
                "cm_host"]

            if chameleon:
                arg.username = "cc"
            elif arg.cloud == "azure":
                arg.username = ConfigDict(filename="cloudmesh.yaml")["cloudmesh"]["clouds"]["azure"]["default"]["username"]
            else:
                if arg.username is None:
                    Console.error("Could not guess the username of the vm", traceflag=False)
                    return
                arg.username = arguments["--username"] or Image.guess_username(arg.image)
            arg.command = arguments["--command"]

            data = dotdict({
                'name': arguments["NAME"] or Default.vm,
                'username': arg.username,
                'cloud': arg.cloud,
                'command': arg.command
            })

            _print("login {cloud}:{username}@{name}".format(**data))

            vm = Vm.get(data.name, category=data.cloud)


            Vm.set_login_user(name=data.name, cloud=data.cloud, username=data.username)

            data.floating_ip = vm.floating_ip
            data.key = arguments["--key"] or Default.key

            _print(Printer.attribute(data))

            '''
            if vm.username is None:
                user_from_db = Vm.get_login_user(vm.name, vm.cloud)

                user_suggest = user_from_db or Default.user
                username = input("Username (Default: {}):".format(user_suggest)) or user_suggest

            Vm.set_login_user(name=data.name, cloud=cloud, username=data.username)
            '''

            ip = arguments["--ip"]
            commands = arguments["--command"]

            ip_addresses = []

            cloud_provider = CloudProvider(cloud).provider
            ip_addr = cloud_provider.get_ips(vm.name)

            ipaddr_dict = Vm.construct_ip_dict(ip_addr, cloud)
            for entry in ipaddr_dict:
                ip_addresses.append(ipaddr_dict[entry]["addr"])

            if len(ip_addresses) > 0:
                if ip is not None:
                    if ip not in ip_addresses:
                        Console.error("IP Address specified does not match with the host.", traceflag=False)
                        return ""
                else:
                    _print("Determining IP Address to use with a ping test.")
                    # This part assumes that the ping is allowed to the machine.
                    for ipadd in ip_addresses:
                        _print("Checking {:}...".format(ipadd))
                        try:
                            # Evading ping test, as ping is not enabled for VMs on Azure cloud
                            # socket.gethostbyaddr(ipadd)
                            # ip will be set if above command is successful.
                            ip = ipadd
                        except socket.herror:
                            _print("Cannot reach {:}.".format(ipadd))

                if ip is None:
                    _print("Unable to connect to the machine")
                    return ""
                else:
                    _print("IP to be used is: {:}".format(ip))

                #
                # TODO: is this correctly implemented
                #
                if not cloud == 'azure':
                    SecGroup.enable_ssh(cloud=cloud)

                if arg.verbose:
                    Console.info("Connecting to Instance at IP:" + format(ip))
                # Constructing the ssh command to connect to the machine.
                sshcommand = "ssh"
                if arg.key is not None:
                    sshcommand += " -i {:}".format(arg.key)
                sshcommand += " -o StrictHostKeyChecking=no"
                sshcommand += " {:}@{:}".format(data.username, ip)
                if commands is not None:
                    sshcommand += " \"{:}\"".format(commands)

                # print(sshcommand)
                os.system(sshcommand)
            else:
                Console.error("No Public IPs found for the instance", traceflag=False)

        elif arguments["list"]:

            # groups = Group.list(output="dict")

            arg = dotdict(arguments)
            arg.names = arguments["NAMES"]

            arg.group = arguments["--group"]
            if arg.group is None:
                arg.group = []
            else:
                arg.group = Parameter.expand(arguments["--group"])

            arg.refresh = arguments["--refresh"] or Default.refresh

            if arg.NAMES is not None:
                arg.names = Parameter.expand(arguments["NAMES"])
            else:
                arg.names = ["all"]

            _format = arguments["--format"] or "table"

            if arguments["--active"]:
                clouds = active_clouds
            else:
                if arguments["--cloud"]:
                    clouds = Parameter.expand(arguments["--cloud"])
                else:
                    clouds = [Default.cloud]

            try:

                d = ConfigDict("cloudmesh.yaml")
                for cloud in clouds:

                    if arg.refresh:
                        _refresh(cloud)

                    Console.ok("Listing VMs on Cloud: {:}".format(cloud))

                    vms = Vm.list(category=cloud, output="raw")

                    # print ("XXX", type(vms), vms)

                    if vms is None:
                        break

                    result = []
                    if "all" in arg.names:
                        if result is None:
                            result = []
                        else:
                            result = vms
                    elif arg.group is not None and len(arg.group) > 0:
                        for vm in vms:
                            if vm["group"] in arg.group:
                                result.append(vm)
                    elif arg.names is not None and len(arg.names) > 0:
                        for vm in vms:
                            if vm["name"] in arg.names:
                                result.append(vm)

                    if len(result) > 0:
                        # print(result)
                        (order, header) = CloudProvider(cloud).get_attributes("vm")
                        print(Printer.write(result,
                                            order=order,
                                            output=_format)
                              )
                    else:
                        Console.error("No data found with requested parameters.", traceflag=False)
            except Exception as e:
                # Error.traceback(e)
                Console.error("Problem listing all instances", traceflag=False)


        elif arguments["rename"]:
            try:
                oldnames = Parameter.expand(arguments["OLDNAMES"])
                newnames = Parameter.expand(arguments["NEWNAMES"])
                force = arguments["--force"]

                if oldnames is None or newnames is None:
                    Console.error("Wrong VMs specified for rename", traceflag=False)
                elif len(oldnames) != len(newnames):
                    Console.error("The number of VMs to be renamed is wrong",
                                  traceflat=False)
                else:
                    for i in range(0, len(oldnames)):
                        oldname = oldnames[i]
                        newname = newnames[i]
                        if arguments["--dryrun"]:
                            Console.ok("Rename {} to {}".format(oldname, newname))
                        else:
                            Vm.rename(cloud=cloud,
                                      oldname=oldname,
                                      newname=newname,
                                      force=force
                                      )
                    msg = "info. OK."
                    Console.ok(msg)
            except Exception as e:
                # Error.traceback(e)
                Console.error("Problem deleting instances", traceflag=False)

        return ""
