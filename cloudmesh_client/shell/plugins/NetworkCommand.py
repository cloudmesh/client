from __future__ import print_function
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.default import Default


class NetworkCommand(object):
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
                network fixed-ip-get [--cloud=CLOUD] FIXED_IP
                network fixed-ip-reserve [--cloud=CLOUD] FIXED_IP
                network fixed-ip-unreserve [--cloud=CLOUD] FIXED_IP
                network floating-ip-associate [--cloud=CLOUD] --server=SERVER FLOATING_IP
                network floating-ip-disassociate [--cloud=CLOUD] --server=SERVER FLOATING_IP
                network floating-ip-create [--cloud=CLOUD] [--floating-ip-pool=FLOATING_IP_POOL]
                network floating-ip-delete [--cloud=CLOUD] FLOATING_IP
                network floating-ip-list [--cloud=CLOUD]
                network floating-ip-pool-list [--cloud=CLOUD]
                network -h | --help

            Options:
                -h                  help message
                --cloud=CLOUD       Name of the IaaS cloud e.g. india_openstack_grizzly.
                --server=SERVER     Server Name
                --floating-ip-pool  Name of Floating IP Pool

            Arguments:
                FIXED_IP        Fixed IP Address, e.g. 10.1.5.2
                FLOATING_IP     Fixed IP Address, e.g. 192.1.66.8

            Examples:
                $ network fixed-ip-get --cloud india 10.1.2.5
                $ network fixed-ip-reserve --cloud india 10.1.2.5
                $ network fixed-ip-unreserve --cloud india 10.1.2.5
                $ network floating-ip-associate --cloud india --server=albert-001 192.1.66.8
                $ network floating-ip-disassociate --cloud india --server=albert-001 192.1.66.8
                $ network floating-ip-create --cloud india --floating-ip-pool=albert-f01
                $ network floating-ip-delete --cloud india 192.1.66.8
                $ network floating-ip-list --cloud india
                $ network floating-ip-pool-list --cloud india

        """
        # pprint(arguments)

        if arguments["fixed-ip-get"]:
            TODO.implement("Yet to implement")
            pass
        elif arguments["fixed-ip-reserve"]:
            TODO.implement("Yet to implement")
            pass
        elif arguments["fixed-ip-unreserve"]:
            TODO.implement("Yet to implement")
            pass
        elif arguments["floating-ip-associate"]:
            TODO.implement("Yet to implement")
            pass
        elif arguments["floating-ip-disassociate"]:
            TODO.implement("Yet to implement")
            pass
        elif arguments["floating-ip-create"]:
            TODO.implement("Yet to implement")
            pass
        elif arguments["floating-ip-delete"]:
            TODO.implement("Yet to implement")
            pass
        elif arguments["floating-ip-list"]:
            TODO.implement("Yet to implement")
            pass
        elif arguments["floating-ip-pool-list"]:
            TODO.implement("Yet to implement")
            pass

if __name__ == '__main__':
    command = cm_shell_security_group()
    command.do_security_group("list")
    command.do_security_group("a=x")
    command.do_security_group("x")