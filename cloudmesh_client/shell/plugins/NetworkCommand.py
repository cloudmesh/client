from __future__ import print_function
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.default import Default
from cloudmesh_client.cloud.network import Network
from cloudmesh_client.shell.command import PluginCommand, CloudCommand


class NetworkCommand(PluginCommand, CloudCommand):
    topics = {"network": "network"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command network")

    @command
    def do_network(self, args, arguments):
        """
        ::

            Usage:
                network get fixed [ip] [--cloud=CLOUD] FIXED_IP
                network get floating [ip] [--cloud=CLOUD] FLOATING_IP_ID
                network reserve fixed [ip] [--cloud=CLOUD] FIXED_IP
                network unreserve fixed [ip] [--cloud=CLOUD] FIXED_IP
                network associate floating [ip] [--cloud=CLOUD] --server=SERVER FLOATING_IP
                network disassociate floating [ip] [--cloud=CLOUD] --server=SERVER FLOATING_IP
                network create floating [ip] [--cloud=CLOUD] [--pool=FLOATING_IP_POOL]
                network delete floating [ip] [--cloud=CLOUD] [--pool=FLOATING_IP_POOL]
                network list floating [ip] [--cloud=CLOUD]
                network list floating pool [--cloud=CLOUD]
                network -h | --help

            Options:
                -h                          help message
                --cloud=CLOUD               Name of the IaaS cloud e.g. india_openstack_grizzly.
                --server=SERVER             Server Name
                --pool=FLOATING_IP_POOL     Name of Floating IP Pool

            Arguments:
                FIXED_IP        Fixed IP Address, e.g. 10.1.5.2
                FLOATING_IP     Floating IP Address, e.g. 192.1.66.8
                FLOATING_IP_ID  ID associated with Floating IP, e.g. 185c5195-e824-4e7b-8581-703abec4bc01

            Examples:
                $ network get fixed ip --cloud india 10.1.2.5
                $ network get fixed --cloud india 10.1.2.5
                $ network get floating ip --cloud india 185c5195-e824-4e7b-8581-703abec4bc01
                $ network get floating --cloud india 185c5195-e824-4e7b-8581-703abec4bc01
                $ network reserve fixed ip --cloud india 10.1.2.5
                $ network reserve fixed --cloud india 10.1.2.5
                $ network unreserve fixed ip --cloud india 10.1.2.5
                $ network unreserve fixed --cloud india 10.1.2.5
                $ network associate floating ip --cloud india --server=albert-001 192.1.66.8
                $ network associate floating --cloud india --server=albert-001 192.1.66.8
                $ network disassociate floating ip --cloud india --server=albert-001 192.1.66.8
                $ network disassociate floating --cloud india --server=albert-001 192.1.66.8
                $ network create floating ip --cloud india --floating-ip-pool=albert-f01
                $ network create floating --cloud india --floating-ip-pool=albert-f01
                $ network delete floating ip --cloud india 192.1.66.8
                $ network delete floating --cloud india 192.1.66.8
                $ network list floating ip --cloud india
                $ network list floating --cloud india
                $ network list floating pool --cloud india

        """

        # Get the cloud parameter OR read default
        cloud = arguments["--cloud"] \
                or Default.get_cloud()

        if cloud is None:
            Console.error("Default cloud has not been set!"
                          "Please use the following to set it:\n"
                          "cm default cloud=CLOUDNAME\n"
                          "or provide it via the --cloud=CLOUDNAME argument.")
            return

        if arguments["get"] \
                and arguments["fixed"]:
            TODO.implement("Yet to implement <get fixed ip>")
            pass
        if arguments["get"] \
                and arguments["floating"]:
            floating_ip_id = arguments["FLOATING_IP_ID"]
            result = Network.get_floating_ip(cloud, floating_ip_id=floating_ip_id)
            Console.msg(result)
            return
        elif arguments["reserve"] \
                and arguments["fixed"]:
            TODO.implement("Yet to implement <reserve fixed ip>")
            pass
        elif arguments["unreserve"] \
                and arguments["fixed"]:
            TODO.implement("Yet to implement <unreserve fixed ip>")
            pass
        elif arguments["associate"] \
                and arguments["floating"]:
            TODO.implement("Yet to implement <associate floating ip>")
            pass
        elif arguments["disassociate"] \
                and arguments["floating"]:
            TODO.implement("Yet to implement <disassociate floating ip>")
            pass
        elif arguments["create"] \
                and arguments["fixed"]:
            TODO.implement("Yet to implement <create floating ip>")
            pass
        elif arguments["delete"] \
                and arguments["floating"]:
            TODO.implement("Yet to implement <delete floating ip>")
            pass
        elif arguments["list"] \
                and arguments["floating"]\
                and arguments["pool"]:
            TODO.implement("Yet to implement <list floating pool>")
            pass
        elif arguments["list"] \
                and arguments["floating"]:
            result = Network.list_floating_ip(cloud)
            Console.msg(result)
            pass

        return


if __name__ == '__main__':
    command = cm_shell_network()
    command.do_network("list")
    command.do_network("a=x")
    command.do_network("x")
