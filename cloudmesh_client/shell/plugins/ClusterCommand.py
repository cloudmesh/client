from __future__ import print_function
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console


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
        Console.error("NOT YET IMPLEMENTED")
        return ""
