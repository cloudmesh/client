from __future__ import print_function
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.default import Default
from pprint import pprint
from cloudmesh_client.cloud.vm import Vm
from cloudmesh_client.cloud.image import Image
from cloudmesh_client.cloud.flavor import Flavor
from cloudmesh_client.cloud.group import Group
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.ConfigDict import ConfigDict
import os
from cloudmesh_client.common.util import path_expand

def boot_from_args(arg):
    arg.username = arg.username or Image.guess_username(arg.image)
    is_name_provided = arg.name is not None

    arg.user = Default.user

    for index in range(0, arg.count):
        vm_details = dotdict({
            "cloud": arg.cloud,
            "name": Vm.generate_vm_name(arg.name, index),
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


class ClusterCommand(PluginCommand, CloudPluginCommand):
    topics = {"cluster": "notimplemented"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command cluster ")

    # noinspection PyUnusedLocal
    @command
    def do_cluster(self, args, arguments):
        """
        ::

          Usage:
              cluster list [--format=FORMAT]
              cluster list NAME
                           [--format=FORMAT]
                           [--column=COLUMN]
                           [--short]
              cluster create NAME
                             [--count=COUNT]
                             [--login=USERNAME]
                             [--cloud=CLOUD]
                             [--image=IMAGE]
                             [--flavor=FLAVOR]
                             [--add]
              cluster delete NAME
              cluster setup NAME [--username]
              cluster inventory NAME

          Description:
              with the help of the cluster command you can create a number
              of virtual machines that are integrated in a named virtual cluster.
              You will be able to login between the nodes of the virtual cluster
              while using public keys.

              cluster setup NAME
                sets up the keys between the cluster node as well as the machine that
                executes the cm command

              cluster inventory NAME
                creates an inventory.txt file to be used by ansible in the current directory

              cluster create NAME
                 creates the virtual machines used for the cluster

              cluster list NAME
                 lists selected details of the vms for the cluster

              cluster delete NAME
                  remove the cluster and its VMs

          Examples:
              cluster list
                  list the clusters

              cluster create NAME --count=COUNT --login=USERNAME [options...]
                  Start a cluster of VMs, and each of them can log into each other.
                  CAUTION: you should specify defaults before using this command:
                  1. select cloud to work on, e.g. cloud select kilo
                       default cloud=kilo
                  2. test if you can create a single VM on the cloud to see if
                     everything is set up
                  3. set the default key to start VMs, e.g. key default [USERNAME-key]
                  5. set image of VMs, e.g. default image
                  6. set flavor of VMs, e.g. default flavor
                  7. Make sure to use a new unused group name

          Arguments:
              NAME              cluster name or group name

          Options:
              --count=COUNT     give the number of VMs to add into the cluster
              --login=USERNAME  give a login name for the VMs, e.g. ubuntu
              --cloud=CLOUD     give a cloud to work on
              --flavor=FLAVOR   give the name of the flavor or flavor id
              --image=IMAGE     give the name of the image or image id
              --add             if a group exists and there are VMs in it
                                additional vms will be added to this cluster and the
                                keys will be added to each other so one can login between
                                them
              FORMAT            output format: table, json, csv
              COLUMN            customize what information to display, for example:
                                --column=status,addresses prints the columns status
                                and addresses
              --detail          for table print format, a brief version
                                is used as default, use this flag to print
                                detailed table

        """

        def get_vms(group_name):
            groups = Vm.get_vms_by_group(group_name)
            vms = []
            for group in groups:
                name = group["member"]
                print(name)
                vm = Vm.get_vm(name)
                vm['cluster'] = group_name
                vms.append(vm)
            return vms

        def _print(f):
                print (f)

        def write(filename, msg):
            with open(path_expand(filename), 'w') as f:
                output = f.write(msg)

        arg = dotdict(arguments)

        arg.format = arguments["--format"] or "table"
        arg.count = int(arguments["--count"] or 1)
        arg.username = arguments["--login"]
        arg.cloud = arguments["--cloud"] or Default.cloud
        arg.image = arguments["--image"] or Default.get(name="image", category=arg.cloud)
        arg.flavor = arguments["--flavor"] or Default.get(name="flavor", category=arg.cloud)
        arg.add = arguments["--add"]
        arg.group = arg.NAME
        arg.name = None
        arg.key = Default.key
        arg.secgroup = Default.secgroup
        arg.group = arg.NAME
        arg.short = arguments["--short"]

        if arg.create:

            boot_from_args(arg)

        elif arg.inventory:

            group = Vm.get_vms_by_group(arg.group)

            result = ""
            if arg.format is "table":
                result = "[servers]\n"

            for element in group:
                name = element["member"]
                vm = Vm.get_vm(name)[0]
                vm['cluster'] = arg.group
                result += "{floating_ip}\n".format(**vm)

            Console.ok("Writing ips to inventory.txt")
            print(result)

            write("inventory.txt", result)

            Console.ok(".ok")
            return ""


        elif arg.list and arg.NAME is not None:

            if arg.short:

                vms = Vm.get_vms_by_group(arg.group)

                if vms is None:
                    Console.error("no vms found for {}".format(arg.group))
                else:

                    print(Printer.list(vms,
                               header=['Group', 'Vm'],
                               order=['name', 'member'],
                               output=arg.format))

            else:

                groups = Vm.get_vms_by_group(arg.group)

                pprint(groups)

                vms = []
                for group in groups:
                    name = group["member"]
                    vm = Vm.get_vm(name)[0]
                    vm['cluster'] = arg.group
                    if vm is not None:
                        vms.append(vm)

                pprint(vms)


                if vms is None:
                    Console.error("no vms found for {}".format(arg.group))
                else:

                    print(Printer.list(vms,
                                   order=['name', 'cluster', 'flavor', 'image', 'status', 'user_id', 'floating_ip'],
                                   output=arg.format))
            return ""

        elif arg.setup:

            def push(from_path, vm):
                vm.ip = vm.floating_ip
                if vm.ip is not None:
                    if arg.verbose:
                        Console.info("Connecting to Instance at IP:" + format(vm.ip))

                    sshcommand = "scp"
                    sshcommand += " -o StrictHostKeyChecking=no"
                    sshcommand += " {:}".format(from_path)
                    sshcommand += " {username}@{ip}:.ssh/authorized_keys".format(**vm)

                    print(sshcommand)
                    os.system(sshcommand)
                else:
                    Console.error("No Public IPs found for the instance", traceflag=False)


            groups = Vm.get_vms_by_group(arg.group)

            pprint (groups)

            vms = []
            for group in groups:
                name = group["member"]
                vm = Vm.get_vm(name)[0]
                vm['cluster'] = arg.group
                if vm is not None:
                    vms.append(vm)

            pprint(vms)

            if vms is None:
                Console.error("no vms found for {}".format(arg.group))
            else:

                print(Printer.list(vms,
                           order=['name', 'cluster', 'flavor', 'image', 'status', 'user_id', 'floating_ip'],
                           output=arg.format))

                keys = ""
                for vm in vms:
                    vm = dotdict(vm)
                    cloud = vm.category

                    if vm.username is None:
                        vm.username = arguments["--username"] or Image.guess_username(arg.image)



                    chameleon = "chameleon" in ConfigDict(filename="cloudmesh.yaml")["cloudmesh"]["clouds"][cloud][
                        "cm_host"]


                    print ("C", chameleon)

                    if chameleon:
                        vm.username = "cc"
                    elif vm.category == "azure":
                        vm.username = ConfigDict(filename="cloudmesh.yaml")["cloudmesh"]["clouds"]["azure"]["default"][
                        "username"]
                    else:
                        if vm.username is None:
                            Console.error("Could not guess the username of the vm", traceflag=False)
                            return


                    Vm.set_login_user(name=vm.name, cloud=vm.category, username=vm.username)
                    vm.ip = vm.floating_ip


                    def execute(commands):
                        if vm.ip is not None:
                            if arg.verbose:
                                Console.info("Connecting to Instance at IP:" + format(vm.ip))

                            sshcommand = "ssh"
                            if arg.key is not None:
                                sshcommand += " -i {:}".format(arg.key)
                            sshcommand += " -o StrictHostKeyChecking=no"
                            sshcommand += " {username}@{ip}".format(**vm)
                            sshcommand += " \'{:}\'".format(commands)

                            print(sshcommand)
                            os.system(sshcommand)
                        else:
                            Console.error("No Public IPs found for the instance", traceflag=False)

                    def copy(commands):
                        if vm.ip is not None:
                            if arg.verbose:
                                Console.info("Connecting to Instance at IP:" + format(vm.ip))

                            sshcommand = "scp"
                            sshcommand += " -o StrictHostKeyChecking=no"
                            sshcommand += " {username}@{ip}".format(**vm)
                            sshcommand += ":{:}".format(commands)

                            print(sshcommand)
                            os.system(sshcommand)
                        else:
                            Console.error("No Public IPs found for the instance", traceflag=False)


                    def cat(filename):
                        with open(path_expand(filename), 'r') as f:
                            output = f.read()
                        return output



                    execute('cat /dev/zero | ssh-keygen -q -N ""')
                    copy(".ssh/id_rsa.pub ~/.ssh/id_rsa_{name}.pub".format(**vm))

                    output = "~/.ssh/id_rsa_{name}.pub".format(**vm)

                    keys = keys + cat(output)

                print ("WRITE KEYS")
                keys = keys + cat("~/.ssh/id_rsa.pub")
                output = "~/.ssh/id_rsa_{group}.pub".format(**arg)
                write(output, keys)

                print("PUSH KEYS")
                for vm in vms:
                    vm = dotdict(vm)
                    push("~/.ssh/id_rsa_{group}.pub".format(**arg), vm)

        return ""
