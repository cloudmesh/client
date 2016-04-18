from __future__ import print_function

import json
import getpass

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.cloud.vm import Vm
from cloudmesh_client.cloud.group import Group
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.network import Network
from cloudmesh_client.common.hostlist import Parameter
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand

from builtins import input


# noinspection PyBroadException
class NetworkCommand(PluginCommand, CloudPluginCommand):
    topics = {"network": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command network")

    # noinspection PyUnusedLocal
    @command
    def do_network(self, args, arguments):
        """
        ::

            Usage:
                network get fixed [ip] [--cloud=CLOUD] FIXED_IP
                network get floating [ip] [--cloud=CLOUD] FLOATING_IP_ID
                network reserve fixed [ip] [--cloud=CLOUD] FIXED_IP
                network unreserve fixed [ip] [--cloud=CLOUD] FIXED_IP
                network associate floating [ip] [--cloud=CLOUD] [--group=GROUP]
                                           [--instance=INS_ID_OR_NAME] [FLOATING_IP]
                network disassociate floating [ip] [--cloud=CLOUD] [--group=GROUP]
                                              [--instance=INS_ID_OR_NAME] [FLOATING_IP]
                network create floating [ip] [--cloud=CLOUD] [--pool=FLOATING_IP_POOL]
                network delete floating [ip] [--cloud=CLOUD] [--unused] [FLOATING_IP]
                network list floating pool [--cloud=CLOUD]
                network list floating [ip] [--cloud=CLOUD] [--unused] [--instance=INS_ID_OR_NAME] [IP_OR_ID]
                network create cluster --group=demo_group
                network -h | --help

            Options:
                -h                          help message
                --unused                    unused floating ips
                --cloud=CLOUD               Name of the IaaS cloud e.g. india_openstack_grizzly.
                --group=GROUP               Name of the group in Cloudmesh
                --pool=FLOATING_IP_POOL     Name of Floating IP Pool
                --instance=INS_ID_OR_NAME   ID or Name of the vm instance

            Arguments:
                IP_OR_ID        IP Address or ID of IP Address
                FIXED_IP        Fixed IP Address, e.g. 10.1.5.2
                FLOATING_IP     Floating IP Address, e.g. 192.1.66.8
                FLOATING_IP_ID  ID associated with Floating IP, e.g. 185c5195-e824-4e7b-8581-703abec4bc01

            Examples:
                network get fixed ip --cloud=india 10.1.2.5
                network get fixed --cloud=india 10.1.2.5
                network get floating ip --cloud=india 185c5195-e824-4e7b-8581-703abec4bc01
                network get floating --cloud=india 185c5195-e824-4e7b-8581-703abec4bc01
                network reserve fixed ip --cloud=india 10.1.2.5
                network reserve fixed --cloud=india 10.1.2.5
                network unreserve fixed ip --cloud=india 10.1.2.5
                network unreserve fixed --cloud=india 10.1.2.5
                network associate floating ip --cloud=india --instance=albert-001 192.1.66.8
                network associate floating --cloud=india --instance=albert-001
                network associate floating --cloud=india --group=albert_group
                network disassociate floating ip --cloud=india --instance=albert-001 192.1.66.8
                network disassociate floating --cloud=india --instance=albert-001 192.1.66.8
                network create floating ip --cloud=india --pool=albert-f01
                network create floating --cloud=india --pool=albert-f01
                network delete floating ip --cloud=india 192.1.66.8 192.1.66.9
                network delete floating --cloud=india 192.1.66.8 192.1.66.9
                network list floating ip --cloud=india
                network list floating --cloud=india
                network list floating --cloud=india --unused
                network list floating --cloud=india 192.1.66.8
                network list floating --cloud=india --instance=323c5195-7yy34-4e7b-8581-703abec4b
                network list floating pool --cloud=india
                network create cluster --group=demo_group

        """
        # pprint(arguments)
        # Get the cloud parameter OR read default
        cloudname = arguments["--cloud"] or Default.cloud

        if cloudname is None:
            Console.error("Default cloud has not been set!"
                          "Please use the following to set it:\n"
                          "cm default cloud=CLOUDNAME\n"
                          "or provide it via the --cloud=CLOUDNAME argument.")
            return ""

        # Fixed IP info
        if arguments["get"] \
                and arguments["fixed"]:
            fixed_ip = arguments["FIXED_IP"]
            result = Network.get_fixed_ip(cloudname,
                                          fixed_ip_addr=fixed_ip)
            Console.msg(result)

        # Floating IP info
        elif arguments["get"] \
                and arguments["floating"]:
            floating_ip_id = arguments["FLOATING_IP_ID"]
            result = Network.get_floating_ip(cloudname,
                                             floating_ip_or_id=floating_ip_id)
            Console.msg(result)

        # Reserve a fixed ip
        elif arguments["reserve"] \
                and arguments["fixed"]:
            fixed_ip = arguments["FIXED_IP"]
            result = Network.reserve_fixed_ip(cloudname=cloudname,
                                              fixed_ip_addr=fixed_ip)
            if result is not None:
                Console.ok("Reserve fixed ip address {} complete.".format(fixed_ip))

        # Un-Reserve a fixed ip
        elif arguments["unreserve"] \
                and arguments["fixed"]:
            fixed_ip = arguments["FIXED_IP"]
            result = Network.unreserve_fixed_ip(cloudname=cloudname,
                                                fixed_ip_addr=fixed_ip)
            if result is not None:
                Console.ok("Un-Reserve fixed ip address {} complete.".format(fixed_ip))

        # Associate floating IP
        elif arguments["associate"] \
                and arguments["floating"]:

            # Get all command-line arguments
            group_name = arguments["--group"]
            instance_id = arguments["--instance"]
            floating_ip = arguments["FLOATING_IP"]

            # group supplied
            if group_name is not None:
                """
                Group name has been provided.
                Assign floating IPs to all vms in the group
                and return
                """
                # Get the group information
                group = Group.get_info(name=group_name,
                                       category=cloudname,
                                       output="json")
                if group is not None:
                    # Convert from str to json
                    group = json.loads(group)
                    # For each vm in the group
                    # Create and assign a floating IP
                    for item in group:
                        instance_id = group[item]["value"]
                        floating_ip = Network.find_assign_floating_ip(cloudname=cloudname,
                                                                      instance_id=instance_id)
                        if floating_ip is not None:
                            Console.ok("Created and assigned Floating IP {} to instance {}."
                                       .format(floating_ip, instance_id))
                            # Refresh VM in db
                            self.refresh_vm(cloudname)
                else:
                    Console.error("No group {} in the Cloudmesh database."
                                  .format(group_name))
                    return ""

            # floating-ip not supplied, instance-id supplied
            elif not floating_ip and instance_id is not None:
                """
                Floating IP has not been provided, instance-id provided.
                Generate one from the pool, and assign to vm
                and return
                """
                floating_ip = Network.find_assign_floating_ip(cloudname=cloudname,
                                                              instance_id=instance_id)
                if floating_ip is not None:
                    Console.ok("Associated floating IP {} to instance {}."
                               .format(floating_ip, instance_id))

            # instance-id & floating-ip supplied
            elif instance_id is not None:
                """
                Floating IP & Instance ID have been provided
                Associate the IP to the instance
                and return
                """
                Network.find_assign_floating_ip(cloudname=cloudname,
                                                instance_id=instance_id,
                                                floating_ip=floating_ip[0])

            # Invalid parameters
            else:
                Console.error("Please provide at least one of [--group] OR [--instance] parameters.\n"
                              "You can also provide [FLOATING_IP] AND [--instance] parameters.\n"
                              "See 'cm network --help' for more info.")
                return ""

            # Refresh VM in db
            self.refresh_vm(cloudname)

        elif arguments["disassociate"] \
                and arguments["floating"]:

            # Get all command-line arguments
            group_name = arguments["--group"]
            instance_id = arguments["--instance"]
            floating_ip = arguments["FLOATING_IP"]

            # group supplied
            if group_name is not None:
                """
                Group name has been provided.
                Remove floating IPs of all vms in the group
                and return
                """
                # Get the group information
                group = Group.get_info(name=group_name,
                                       category=cloudname,
                                       output="json")
                if group is not None:
                    # Convert from str to json
                    group = json.loads(group)
                    # For each vm in the group
                    # Create and assign a floating IP
                    for item in group:
                        instance_id = group[item]["value"]
                        # Get the instance dict
                        instance_dict = Network.get_instance_dict(cloudname=cloudname,
                                                                  instance_id=instance_id)
                        # Instance not found
                        if instance_dict is None:
                            Console.error("Instance {} not found in the cloudmesh database!"
                                          .format(instance_id))
                            return ""

                        # Get the instance name
                        instance_name = instance_dict["name"]
                        floating_ip = instance_dict["floating_ip"]

                        # Floating ip argument invalid
                        if floating_ip is None:
                            Console.error("Instance{} does not have a floating_ip."
                                          .format(instance_name))
                            return ""

                        result = Network.disassociate_floating_ip(cloudname=cloudname,
                                                                  instance_name=instance_name,
                                                                  floating_ip=floating_ip)
                        if result is not None:
                            Console.ok("Disassociated Floating IP {} from instance {}."
                                       .format(floating_ip, instance_name))
                else:
                    Console.error("No group {} in the Cloudmesh database."
                                  .format(group_name))
                    return ""

            # floating-ip not supplied, instance-id supplied
            elif len(floating_ip) == 0 and instance_id is not None:
                """
                Floating IP has not been provided, instance-id provided.
                Remove floating ip allocated to vm
                and return
                """
                instance_dict = Network.get_instance_dict(cloudname=cloudname,
                                                          instance_id=instance_id)
                # Instance not found
                if instance_dict is None:
                    Console.error("Instance {} not found in the cloudmesh database!"
                                  .format(instance_id))
                    return ""

                instance_name = instance_dict["name"]
                floating_ip = instance_dict["floating_ip"]

                # Floating ip argument invalid
                if floating_ip is None:
                    Console.error("Instance{} does not have a floating_ip."
                                  .format(instance_name))
                    return ""

                result = Network.disassociate_floating_ip(cloudname=cloudname,
                                                          instance_name=instance_name,
                                                          floating_ip=floating_ip)
                if result is not None:
                    Console.ok("Disassociated Floating IP {} from instance {}."
                               .format(floating_ip, instance_name))

            # instance-id & floating-ip supplied
            elif instance_id is not None:
                """
                Floating IP & Instance ID have been provided
                Remove the IP from the instance
                and return
                """
                instance_dict = Network.get_instance_dict(cloudname=cloudname,
                                                          instance_id=instance_id)
                floating_ip = floating_ip[0]

                # Instance not found
                if instance_dict is None:
                    Console.error("Instance {} not found in the cloudmesh database!"
                                  .format(instance_id))
                    return ""

                instance_name = instance_dict["name"]
                _floating_ip = instance_dict["floating_ip"]

                # Floating ip argument invalid
                if _floating_ip != floating_ip:
                    Console.error("Invalid floating_ip {} for instance {}."
                                  .format(floating_ip, instance_name))
                    return ""

                result = Network.disassociate_floating_ip(cloudname=cloudname,
                                                          instance_name=instance_name,
                                                          floating_ip=floating_ip)
                if result is not None:
                    Console.ok("Disassociated Floating IP {} from instance {}."
                               .format(floating_ip, instance_name))

            # Invalid parameters
            else:
                Console.error("Please provide at least one of [--group] OR [--instance] parameters.\n"
                              "You can also provide [FLOATING_IP] AND [--instance] parameters.\n"
                              "See 'cm network --help' for more info.")
                return ""

            # Refresh VM in db
            self.refresh_vm(cloudname)

        # Create new floating ip under floating pool
        elif arguments["create"] \
                and arguments["floating"]:
            floating_pool = arguments["--pool"]
            result = Network.create_floating_ip(cloudname=cloudname,
                                                floating_pool=floating_pool)
            if result is not None:
                Console.ok("Created new floating IP {}".format(result))
            else:
                Console.error("Failed to create floating IP! Please check arguments.")

        # Delete a floating ip address
        elif arguments["delete"] \
                and arguments["floating"]:

            # delete all unused floating ips
            if arguments["--unused"]:
                unused_floating_ips = Network.get_unused_floating_ip_list(cloudname=cloudname)
                if unused_floating_ips:
                    for floating_ip in unused_floating_ips:
                        self._delete_floating_ip(cloudname=cloudname,
                                                 floating_ip=floating_ip["id"])
                else:
                    Console.msg("No unused floating ips exist at this moment. Ok.")
                return ""

            # delete specified floating ips
            floating_ips = Parameter.expand(arguments["FLOATING_IP"])

            for floating_ip in floating_ips:
                self._delete_floating_ip(cloudname=cloudname,
                                         floating_ip=floating_ip)

        # Floating IP Pool List
        elif arguments["list"] \
                and arguments["floating"] \
                and arguments["pool"]:
            result = Network.list_floating_ip_pool(cloudname)
            Console.msg(result)

        # Floating IP list [or info]
        elif arguments["list"] \
                and arguments["floating"]:

            ip_or_id = arguments["IP_OR_ID"]
            instance_id = arguments["--instance"]

            # List unused floating addr
            if arguments["--unused"]:
                result = Network.list_unused_floating_ip(cloudname=cloudname)
                Console.msg(result)
                return ""

            # Refresh VM in db
            self.refresh_vm(cloudname)

            # If instance id is supplied
            if instance_id is not None:
                instance_dict = Network.get_instance_dict(cloudname=cloudname,
                                                          instance_id=instance_id)
                # Instance not found
                if instance_dict is None:
                    Console.error("Instance {} not found in the cloudmesh database!"
                                  .format(instance_id))
                    return ""

                # Read the floating_ip from the dict
                ip_or_id = instance_dict["floating_ip"]

                if ip_or_id is None:
                    Console.error("Instance with ID {} does not have a floating IP address!"
                                  .format(instance_id))
                    return ""

            # If the floating ip or associated ID is supplied
            if ip_or_id is not None:
                result = Network.get_floating_ip(cloudname,
                                                 floating_ip_or_id=ip_or_id)

                if result is not None:
                    Console.msg(result)
                else:
                    Console.error("Floating IP not found! Please check your arguments.")
                    return ""
            # Retrieve the full list
            else:
                result = Network.list_floating_ip(cloudname)
                Console.msg(result)

        # Create a virtual cluster
        elif arguments["cluster"] and \
                arguments["create"]:

            group_name = arguments["--group"] or \
                         Default.get(name="group", category=cloudname)

            # Get the group information
            group = Group.get_info(name=group_name,
                                   category=cloudname,
                                   output="json")
            if group is not None:
                # Convert from str to json
                group = json.loads(group)

                # var contains pub key of all vms
                public_keys = ""
                login_users = []
                login_ips = []

                # For each vm in the group
                # Create and assign a floating IP
                for item in group:
                    instance_id = group[item]["value"]
                    # Get the instance dict
                    instance_dict = Network.get_instance_dict(cloudname=cloudname,
                                                              instance_id=instance_id)
                    # Instance not found
                    if instance_dict is None:
                        Console.error("Instance {} not found in the cloudmesh database!"
                                      .format(instance_id))
                        return ""

                    # Get the instance name
                    instance_name = instance_dict["name"]
                    floating_ip = instance_dict["floating_ip"]

                    # If vm does not have floating ip, then create
                    if floating_ip is None:
                        floating_ip = Network.create_assign_floating_ip(cloudname=cloudname,
                                                                        instance_name=instance_name)
                        if floating_ip is not None:
                            Console.ok("Created and assigned Floating IP {} to instance {}."
                                       .format(floating_ip, instance_name))
                            # Refresh VM in db
                            self.refresh_vm(cloudname)

                    # Get the login user for this machine
                    user = input("Enter the login user for VM {} : ".format(instance_name))
                    passphrase = getpass.getpass("Enter the passphrase key on VM {} : ".format(instance_name))

                    # create list for second iteration
                    login_users.append(user)
                    login_ips.append(floating_ip)

                    login_args = [
                        user + "@" + floating_ip,
                    ]

                    keygen_args = [
                        "ssh-keygen -t rsa -f ~/.ssh/id_rsa -N " + passphrase
                    ]

                    cat_pubkey_args = [
                        "cat ~/.ssh/id_rsa.pub"
                    ]

                    generate_keypair = login_args + keygen_args
                    result = Shell.ssh(*generate_keypair)

                    # print("***** Keygen *****")
                    # print(result)

                    cat_public_key = login_args + cat_pubkey_args
                    result = Shell.ssh(*cat_public_key)
                    public_keys += "\n" + result

                    # print("***** id_rsa.pub *****")
                    # print(result)

                # print("***** public keys *****")
                # print(public_keys)

                for user, ip in zip(login_users, login_ips):
                    arguments = [
                        user + "@" + ip,
                        "echo '" + public_keys + "' >> ~/.ssh/authorized_keys"
                    ]

                    # copy the public key contents to auth_keys
                    result = Shell.ssh(*arguments)

                Console.ok("Virtual cluster creation successfull.")
            else:
                Console.error("No group {} in the Cloudmesh database."
                              .format(group_name))
                return ""

        return ""

    @classmethod
    def refresh_vm(cls, cloudname):
        try:
            msg = "Refreshing database for cloud {:}.".format(cloudname)
            if Vm.refresh(cloud=cloudname) is not None:
                Console.ok("{:} OK.".format(msg))
            else:
                Console.error("{:} failed".format(msg))
        except Exception:
            Console.error("Problem running database refresh")

    @classmethod
    def _delete_floating_ip(cls, cloudname, floating_ip):
        result = Network.delete_floating_ip(cloudname=cloudname,
                                            floating_ip_or_id=floating_ip)

        if result is not None:
            Console.ok(result)
        else:
            Console.error("Failed to delete floating IP address!")

    @classmethod
    def _assign_floating_ip(cls, cloudname, instance_id, floating_ip):
        # find instance in db
        instance_dict = Network.get_instance_dict(cloudname=cloudname,
                                                  instance_id=instance_id)
        # Instance not found
        if instance_dict is None:
            Console.error("Instance {} not found in the cloudmesh database!"
                          .format(instance_id))
            return ""

        instance_name = instance_dict["name"]
        result = Network.associate_floating_ip(cloudname=cloudname,
                                               instance_name=instance_name,
                                               floating_ip=floating_ip)
        if result is not None:
            Console.ok("Associated Floating IP {} to instance {}."
                       .format(floating_ip, instance_name))
