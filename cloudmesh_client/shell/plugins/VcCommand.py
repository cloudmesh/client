from __future__ import print_function
from cloudmesh_client.cloud.vc import Vc
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.hostlist import Parameter
from pprint import pprint

class VcCommand(PluginCommand, CloudPluginCommand):
    topics = {"vc": "todo"}

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
                vc key add KEYFILE NAMES [--username=USERNAME] [--proxy=PROXY]
                vc key distribute NAMES [--username=USERNAME] [--proxy=PROXY]
                vc key list NAMES [--usort] [--username=USERNAME] [--proxy=PROXY] [--format=FORMAT]
                vc key proxy NAMES [--username=USERNAME] [--proxy=PROXY]

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

                Proxy server

                    vc key proxy NAMES
                        sometimes you may not have enough floating IPs so it is possible to dedicate one machine
                        as a proxy server that has such a floating ip. The way this is done is that you need to set
                        up ssh tunnels via the proxy server in your  .ssh/config file. The command will print a
                        template that you could include in your .ssh/config file to gain easily access to your other
                        machines without floating ip. For example it will generate the following for a given PROXY host,
                        USERNAME, and vm1 is the name of the first vm in NAMES

                        Host vm1
                            User  USERNAME
                            Hostname PROXY
                            ProxyCommand  ssh 10.1.1.2 nc %h %p
                            ForwardX11 yes

                        Note: this is just a draft and will be improved upon discussion with the team

        """

        arg = dotdict(arguments)
        arg.usort = arguments["--usort"]
        arg.format = arguments["--format"]
        arg.username = arguments["--username"]
        arg.proxy = arguments["--proxy"]


        if arg.proxy:
            Console.error("proxy not yet supported", traceflag=False)

        if arg.NAMES is not None:
            arg.names = Parameter.expand(arg.NAMES)
        else:
            arg.names = None


        pprint (arg)

        if arg.add:

            print("vc key add KEYFILE NAMES --username=USERNAME")

            print(arg.username)
            print(arg.names)
            print(arg.KEYFILE)
            print(arg.proxy)


            Console.TODO("not yet implemented")
            return ""

        elif arg.distribute:

            print("vc key distribute NAMES --username=USERNAME")
            print(arg.names)
            print(arg.username)
            print(arg.proxy)

            Console.TODO("not yet implemented")
            return ""

        elif arg.list:

            print("vc key list NAMES [--usort] [--format=FORMAT]")

            print(arg.names)
            print(arg.username)
            print(arg.format)
            print(arg.usort)
            print(arg.proxy)
            result = Vc.list(names=arg.names)  # dont forget format and sort
            Console.TODO("not yet implemented")
            return ""

        elif arg.proxy:

            print("vc key proxy NAMES [--username=USERNAME] [--proxy=PROXY]")

            print(arg.names)
            print(arg.username)
            print(arg.format)
            print(arg.usort)
            print(arg.proxy)

            result = Vc.list(names=arg.names)  # dont forget format and sort
            Console.TODO("not yet implemented")
            return ""