from __future__ import print_function
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.default import Default
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

            Usage:A
                network get fixed [ip] [--cloud=CLOUD] FIXED_IP
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
                FLOATING_IP     Fixed IP Address, e.g. 192.1.66.8

            Examples:
                $ network get fixed ip --cloud india 10.1.2.5
                $ network get fixed --cloud india 10.1.2.5
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
        # pprint(arguments)

        if arguments["get"] \
                and arguments["fixed"]:
            TODO.implement("Yet to implement <get fixed ip>")
            pass
        elif arguments["reserve"] \
                and arguments["fixed"]:
            TODO.implement("Yet to implement <reserve fixed ip>")
            pass
        elif arguments["unreserve"] \
                and arguments["fixed"]:
            TODO.implement("Yet to implement <unreserve fixed ip>")
            pass
        elif arguments["associate"] \
                and arguments["fixed"]:
            TODO.implement("Yet to implement <associate fixed ip>")
            pass
        elif arguments["disassociate"] \
                and arguments["fixed"]:
            TODO.implement("Yet to implement <disassociate fixed ip>")
            pass
        elif arguments["create"] \
                and arguments["fixed"]:
            TODO.implement("Yet to implement <create fixed ip>")
            pass
        elif arguments["delete"] \
                and arguments["fixed"]:
            TODO.implement("Yet to implement <delete fixed ip>")
            pass
        elif arguments["list"] \
                and arguments["fixed"]\
                and arguments["pool"]:
            TODO.implement("Yet to implement <list fixed pool>")
            pass
        elif arguments["list"] \
                and arguments["fixed"]:
            TODO.implement("Yet to implement <list fixed ip>")
            pass

        return ""


if __name__ == '__main__':
    command = cm_shell_network()
    command.do_network("list")
    command.do_network("a=x")
    command.do_network("x")
