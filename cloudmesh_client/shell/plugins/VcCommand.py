from __future__ import print_function
from cloudmesh_client.cloud.vc import Vc
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.hostlist import Parameter

class VcCommand(PluginCommand, CloudPluginCommand):
    topics = {"vc": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command vc")

    # noinspection PyUnusedLocal
    @command
    def do_vc(self, args, arguments):
        """
        ::

            Usage:
                vc key add KEYFILE NAMES [--username=USERNAME]
                vc key distribute NAMES
                vc key list NAMES [--usort] [--format=FORMAT]

                This lists out the vcs present for a cloud

            Options:
               --format=FORMAT  the output format [default: table]

            Description:

                see examples

            Examples:
                cm vc key add keys.txt gregor-[001-010]
                    adds the keys in the file keys.txt to the authorized_keys file
                    in the user that is registered for the vm

                cm vc key add keys.txt gregor-[001-010] --username=ubuntu
                    adds the keys in the file keys.txt to the authorized_keys file
                    in the user ubuntu for each of the vms

                vc key distribute gregor-[001-010]
                    gathers the keys from the host gathers it into a single file
                    and adds them to the authorized keys file. Duplicated keys will
                    be ignored.

                vc key list gregor-[001-010] [--usort]
                    creates a table with all keys in authorized_keys from all of the
                    remote machines. If the parameter usort is specified it only lists
                    the key once, but lists in the host column the list of all host on
                    which the key is stored



        """

        arg = dotdict(arguments)
        arg.usort = arguments["--usort"]
        arg.format = arguments["--format"]
        arg.username = arguments["--username"]

        if arg.NAMES is not None:
            arg.names = Parameter.expand(arg.NAMES)
        else:
            arg.names = None


        if arg.add:

            print ("vc key add KEYFILE NAMES --username=USERNAME")
            Console.TODO("not yet implemented")
            return ""

        elif arg.distribute:


            print ("vc key distribute NAMES")
            Console.TODO("not yet implemented")
            return ""

        elif arg.list:

            print("vc key list NAMES [--usort] [--format=FORMAT]")

            print (arg.names)
            result = Vc.list(names=arg.names) # dont forget format and sort
            Console.TODO("not yet implemented")
            return ""

