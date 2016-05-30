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

def boot_from_args(arg):
    arg.username = arg.username or Image.guess_username(arg.image)
    is_name_provided = arg.name is not None

    arg.user = Default.user

    for index in range(0, arg.count):
        vm_details = dotdict({
            "cloud": arg.cloud,
            "name": Vm.get_vm_name(arg.name, index),
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
                           [--detail]
              cluster create NAME
                             [--count=COUNT]
                             [--login=USERNAME]
                             [--cloud=CLOUD]
                             [--image=IMAGE]
                             [--flavor=FLAVOR]
                             [--add]
              cluster delete NAME

          Description:
              with the help of the cluster command you can create a number
              of virtual machines that are integrated in a named virtual cluster.
              You will be able to login between the nodes of the virtual cluster
              while using public keys.

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

              cluster list NAME
                  show the detailed information about the cluster VMs

              cluster delete NAME
                  remove the cluster and its VMs

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
        arg = dotdict(arguments)

        if arg.create:

            arg.count = int(arguments["--count"]) or 1
            arg.username = arguments["--login"]
            arg.cloud = arguments["--cloud"] or Default.cloud
            arg.image = arguments["--image"] or  Default.get(name="image", category=arg.cloud)
            arg.flavor = arguments["--flavor"] or Default.get(name="flavor", category=arg.cloud)
            arg.add = arguments["--add"]
            arg.group = arg.NAME
            arg.name = None
            arg.key  = Default.key
            arg.secgroup = Default.secgroup
            pprint (arg)

            boot_from_args(arg)


        Console.error("NOT YET IMPLEMENTED")
        return ""
