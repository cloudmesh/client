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
                network create floating [ip] [--cloud=CLOUD] --pool=FLOATING_IP_POOL
                network delete floating [ip] [--cloud=CLOUD] FLOATING_IP
                network list floating [ip] [--cloud=CLOUD] [--instance=INS_ID_OR_NAME] [IP_OR_ID]
                network list floating pool [--cloud=CLOUD]
                network -h | --help

            Options:
                -h                          help message
                --cloud=CLOUD               Name of the IaaS cloud e.g. india_openstack_grizzly.
                --server=SERVER             Server Name
                --pool=FLOATING_IP_POOL     Name of Floating IP Pool
                --instance=INS_ID_OR_NAME   ID of the vm instance

            Arguments:
                IP_OR_ID        IP Address or ID
                FIXED_IP        Fixed IP Address, e.g. 10.1.5.2
                FLOATING_IP     Floating IP Address, e.g. 192.1.66.8
                FLOATING_IP_ID  ID associated with Floating IP, e.g. 185c5195-e824-4e7b-8581-703abec4bc01

            Examples:
                $ network get fixed ip --cloud=india 10.1.2.5
                $ network get fixed --cloud=india 10.1.2.5
                $ network get floating ip --cloud=india 185c5195-e824-4e7b-8581-703abec4bc01
                $ network get floating --cloud=india 185c5195-e824-4e7b-8581-703abec4bc01
                $ network reserve fixed ip --cloud=india 10.1.2.5
                $ network reserve fixed --cloud=india 10.1.2.5
                $ network unreserve fixed ip --cloud=india 10.1.2.5
                $ network unreserve fixed --cloud=india 10.1.2.5
                $ network associate floating ip --cloud=india --server=albert-001 192.1.66.8
                $ network associate floating --cloud=india --server=albert-001 192.1.66.8
                $ network disassociate floating ip --cloud=india --server=albert-001 192.1.66.8
                $ network disassociate floating --cloud=india --server=albert-001 192.1.66.8
                $ network create floating ip --cloud=india --pool=albert-f01
                $ network create floating --cloud=india --pool=albert-f01
                $ network delete floating ip --cloud=india 192.1.66.8
                $ network delete floating --cloud=india 192.1.66.8
                $ network list floating ip --cloud=india
                $ network list floating --cloud=india
                $ network list floating --cloud=india 192.1.66.8
                $ network list floating --cloud=india --instance=323c5195-7yy34-4e7b-8581-703abec4b
                $ network list floating pool --cloud=india

        """

        # Get the cloud parameter OR read default
        cloudname = arguments["--cloud"] \
                    or Default.get_cloud()

        if cloudname is None:
            Console.error("Default cloud has not been set!"
                          "Please use the following to set it:\n"
                          "cm default cloud=CLOUDNAME\n"
                          "or provide it via the --cloud=CLOUDNAME argument.")
            return

        # Fixed IP info
        if arguments["get"] \
                and arguments["fixed"]:
            fixed_ip = arguments["FIXED_IP"]
            result = Network.get_fixed_ip(cloudname,
                                          fixed_ip_addr=fixed_ip)
            Console.msg(result)
            return

            # Floating IP info
        if arguments["get"] \
                and arguments["floating"]:
            floating_ip_id = arguments["FLOATING_IP_ID"]
            result = Network.get_floating_ip(cloudname,
                                             floating_ip_or_id=floating_ip_id)
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

        # Create new floating ip under floating pool
        elif arguments["create"] \
                and arguments["floating"]:
            floating_pool = arguments["--pool"]
            result = Network.create_floating_ip(cloudname=cloudname,
                                                floating_pool=floating_pool)
            if result is not None:
                Console.ok("Created new floating IP [{}]".format(result))
            else:
                Console.error("Failed to create floating IP! Please check arguments.")

            return

        # Delete a floating ip address
        elif arguments["delete"] \
                and arguments["floating"]:
            floating_ip = arguments["FLOATING_IP"]
            result = Network.delete_floating_ip(cloudname=cloudname,
                                                floating_ip_or_id=floating_ip)

            if result is not None:
                Console.ok(result)
            else:
                Console.error("Failed to delete floating IP address!")
            return

        # Floating IP Pool List
        elif arguments["list"] \
                and arguments["floating"] \
                and arguments["pool"]:
            result = Network.list_floating_ip_pool(cloudname)
            Console.msg(result)
            return

        # Floating IP list [or info]
        elif arguments["list"] \
                and arguments["floating"]:

            ip_or_id = arguments["IP_OR_ID"]
            instance_id = arguments["--instance"]

            # If instance id is supplied
            if instance_id is not None:
                instance_dict = Network.get_instance_dict(cloudname=cloudname,
                                                          instance_id=instance_id)
                # Instance not found
                if instance_dict is None:
                    Console.error("Instance [{}] not found in the cloudmesh database!"
                                  .format(instance_id))
                    return

                # Read the floating_ip from the dict
                ip_or_id = instance_dict["floating_ip"]

                if ip_or_id is None:
                    Console.error("Instance with ID [{}] does not have a floating IP address!"
                                  .format(instance_id))
                    return

            # If the floating ip or associated ID is supplied
            if ip_or_id is not None:
                result = Network.get_floating_ip(cloudname,
                                                 floating_ip_or_id=ip_or_id)

                if result is not None:
                    Console.msg(result)
                else:
                    Console.error("Floating IP not found! Please check your arguments.")
                    return
            # Retrieve the full list
            else:
                result = Network.list_floating_ip(cloudname)
                Console.msg(result)
            pass

        return


if __name__ == '__main__':
    command = cm_shell_network()
    command.do_network("list")
    command.do_network("a=x")
    command.do_network("x")
