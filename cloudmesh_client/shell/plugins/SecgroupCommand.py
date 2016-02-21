from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.secgroup import SecGroup
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand


class SecgroupCommand(PluginCommand, CloudPluginCommand):
    topics = {"secgroup": "security"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command secgroup")

    # noinspection PyUnusedLocal
    @command
    def do_secgroup(self, args, arguments):
        """
        ::

            Usage:
                secgroup list [--cloud=CLOUD]
                secgroup create [--cloud=CLOUD] LABEL
                secgroup delete [--cloud=CLOUD] LABEL
                secgroup rules-list [--cloud=CLOUD] LABEL
                secgroup rules-add [--cloud=CLOUD] LABEL FROMPORT TOPORT PROTOCOL CIDR
                secgroup rules-delete [--cloud=CLOUD] [--all] LABEL [FROMPORT] [TOPORT] [PROTOCOL] [CIDR]
                secgroup refresh [--cloud=CLOUD]
                secgroup -h | --help
                secgroup --version

            Options:
                -h                  help message
                --cloud=CLOUD       Name of the IaaS cloud e.g. india_openstack_grizzly.

            Arguments:
                LABEL         The label/name of the security group
                FROMPORT      Staring port of the rule, e.g. 22
                TOPORT        Ending port of the rule, e.g. 22
                PROTOCOL      Protocol applied, e.g. TCP,UDP,ICMP
                CIDR          IP address range in CIDR format, e.g., 129.79.0.0/16

            Description:
                security_group command provides list/add/delete
                security_groups for a tenant of a cloud, as well as
                list/add/delete of rules for a security group from a
                specified cloud and tenant.


            Examples:
                secgroup list --cloud india
                secgroup rules-list --cloud=kilo default
                secgroup create --cloud=kilo webservice
                secgroup rules-add --cloud=kilo webservice 8080 8088 TCP 129.79.0.0/16
                secgroup rules-delete --cloud=kilo webservice 8080 8088 TCP 129.79.0.0/16
                secgroup rules-delete --all


        """
        # pprint(arguments)

        cloud = arguments["--cloud"] or Default.get_cloud()

        # if refresh ON, pull data from cloud to db
        if arguments["refresh"] or \
                Default.refresh():
            msg = "Refresh secgroup for cloud {:}.".format(cloud)
            if SecGroup.refresh(cloud):
                Console.ok("{:} ok".format(msg))
            else:
                Console.error("{:} failed".format(msg))

        # list all security-groups in cloud
        if arguments["list"]:
            # If default not set, terminate
            if not cloud:
                Console.error("Default cloud not set!")
                return

            result = SecGroup.list(cloud=cloud)
            if result:
                print(result)
            else:
                Console.error(
                    "No Security Groups found in the cloudmesh database!")
            return ""

        # Create a security-group
        elif arguments["create"]:
            # if no arguments read default
            label = arguments["LABEL"]

            # If default not set, terminate
            if not cloud:
                Console.error("Default cloud not set!")
                return

            # Create returns uuid of created sec-group
            uuid = SecGroup.create(label, cloud)

            if uuid:
                Console.ok("Created a new security group [{}] with UUID [{}]"
                           .format(label, uuid))
            else:
                Console.error("Exiting!")
            return ""

        # Delete a security-group
        elif arguments["delete"]:
            # if no arguments read default
            label = arguments["LABEL"]

            # If default not set, terminate
            if not cloud:
                Console.error("Default cloud not set!")
                return ""

            result = SecGroup.delete_secgroup(label, cloud)
            if result is not None:
                Console.ok("Security Group [{}] in cloud [{}] deleted successfully." \
                           .format(label, cloud))
            else:
                Console.error("Failed to delete Security Group [{}] in cloud [{}]"
                              .format(label, cloud))

            return ""

        # Delete security group rule
        elif arguments["rules-delete"]:
            # if no arguments read default
            cloud = arguments["--cloud"] or Default.get_cloud()

            label = arguments["LABEL"]
            from_port = arguments["FROMPORT"]
            to_port = arguments["TOPORT"]
            protocol = arguments["PROTOCOL"]
            cidr = arguments["CIDR"]

            # If default not set, terminate
            if not cloud:
                Console.error("Default cloud not set!")
                return ""

            # Get the security group
            sec_group = SecGroup.get(label, cloud)
            if sec_group:

                # delete all rules for secgroup
                if arguments["--all"]:
                    SecGroup.delete_all_rules(secgroup=sec_group)
                    return ""

                # Get the rules
                result = SecGroup.delete_rule(cloud=cloud,
                                              secgroup=sec_group,
                                              from_port=from_port,
                                              to_port=to_port,
                                              protocol=protocol,
                                              cidr=cidr)
                if result:
                    Console.ok(result)
                else:
                    Console.error(
                        "Rule [{} | {} | {} | {}] could not be deleted"
                            .format(from_port, to_port, protocol, cidr))

            return ""

        # list security group rules
        elif arguments["rules-list"]:
            # if no arguments read default
            label = arguments["LABEL"]

            # If default not set, terminate
            if not cloud:
                Console.error("Default cloud not set!")
                return ""

            # Get the security group
            sec_group = SecGroup.get(label, cloud)
            if sec_group:
                # Get the rules
                result = SecGroup.get_rules(sec_group.uuid)
                print(result)
            else:
                Console.error(
                    "Security Group with label [{}] in cloud [{}] not found!"
                        .format(label, cloud))
                return ""

        # add rule to security group
        elif arguments["rules-add"]:
            label = arguments["LABEL"]
            from_port = arguments["FROMPORT"]
            to_port = arguments["TOPORT"]
            protocol = arguments["PROTOCOL"]
            cidr = arguments["CIDR"]

            # If default not set, terminate
            if not cloud:
                Console.error("Default cloud not set!")
                return ""

            # Get the security group
            sec_group = SecGroup.get(label, cloud)
            if sec_group:
                # Add rules to the security group
                SecGroup.add_rule(cloud=cloud,
                                  secgroup=sec_group,
                                  from_port=from_port,
                                  to_port=to_port,
                                  protocol=protocol,
                                  cidr=cidr)
            else:
                Console.error(
                    "Security Group with label [{}] in cloud [{}] not found!".format(label, cloud))
                return ""

        # TODO: Add Implementation
        elif arguments["--version"]:
            Console.ok('Version: ')

        return ""
