from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.default import Default
from cloudmesh_client.cloud.secgroup import SecGroup


class SecgroupCommand(object):
    topics = {"secgroup": "security"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command secgroup")

    @command
    def do_secgroup(self, args, arguments):
        """
        ::

            Usage:
                secgroup list [--cloud=CLOUD] [--tenant=TENANT]
                secgroup create [--cloud=CLOUD] [--tenant=TENANT] LABEL
                secgroup delete [--cloud=CLOUD] [--tenant=TENANT] LABEL
                secgroup rules-list [--cloud=CLOUD] [--tenant=TENANT] LABEL
                secgroup rules-add [--cloud=CLOUD] [--tenant=TENANT] LABEL FROMPORT TOPORT PROTOCOL CIDR
                secgroup rules-delete [--cloud=CLOUD] [--tenant=TENANT] LABEL FROMPORT TOPORT PROTOCOL CIDR
                secgroup -h | --help
                secgroup --version

            Options:
                -h                  help message
                --cloud=CLOUD       Name of the IaaS cloud e.g. india_openstack_grizzly.
                --tenant=TENANT     Name of the tenant, e.g. fg82.

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
                $ secgroup list --cloud india --tenant fg82
                $ secgroup rules-list --cloud india --tenant fg82 default
                $ secgroup create --cloud india --tenant fg82 webservice
                $ secgroup rules-add --cloud india --tenant fg82 webservice 8080 8088 TCP "129.79.0.0/16"

        """
        # pprint(arguments)

        if arguments["list"]:
            # if no arguments read default
            cloud = arguments["--cloud"] or Default.get("cloud")
            tenant = arguments["--tenant"] or Default.get("tenant")

            # If default not set, terminate
            if not cloud:
                Console.error("Default cloud not set!")
                return
            if not tenant:
                Console.error("Default tenant not set!")
                return

            result = SecGroup.list_secgroup(tenant, cloud)
            if result:
                print(result)
            else:
                Console.error(
                    "No Security Groups found in the cloudmesh database!")
            return

        elif arguments["create"]:
            # if no arguments read default
            cloud = arguments["--cloud"] or Default.get("cloud")
            tenant = arguments["--tenant"] or Default.get("tenant")
            label = arguments["LABEL"]

            # If default not set, terminate
            if not cloud:
                Console.error("Default cloud not set!")
                return
            if not tenant:
                Console.error("Default tenant not set!")
                return

            # Create returns uuid of created sec-group
            uuid = SecGroup.create(label, cloud, tenant)

            if uuid:
                Console.ok("Created a new security group [{}] with UUID [{}]"
                           .format(label, uuid))
            else:
                Console.error("Exiting!")
            return

        elif arguments["delete"]:
            # if no arguments read default
            cloud = arguments["--cloud"] or Default.get("cloud")
            tenant = arguments["--tenant"] or Default.get("tenant")
            label = arguments["LABEL"]

            # If default not set, terminate
            if not cloud:
                Console.error("Default cloud not set!")
                return
            if not tenant:
                Console.error("Default tenant not set!")
                return

            result = SecGroup.delete_secgroup(label, cloud, tenant)
            if result:
                print(result)
            else:
                Console.error("Security Group [{}, {}, {}] could not be "
                              "deleted".format(label, cloud, tenant))

            return

        elif arguments["rules-delete"]:
            # if no arguments read default
            cloud = arguments["--cloud"] or Default.get("cloud")
            tenant = arguments["--tenant"] or Default.get("tenant")

            label = arguments["LABEL"]
            from_port = arguments["FROMPORT"]
            to_port = arguments["TOPORT"]
            protocol = arguments["PROTOCOL"]
            cidr = arguments["CIDR"]

            # If default not set, terminate
            if not cloud:
                Console.error("Default cloud not set!")
                return
            if not tenant:
                Console.error("Default tenant not set!")
                return

            # Get the security group
            sec_group = SecGroup.get_secgroup(label, tenant, cloud)
            if sec_group:
                # Get the rules
                result = SecGroup.delete_rule(sec_group, from_port, to_port,
                                              protocol, cidr)
                if result:
                    print(result)
                else:
                    Console.error(
                        "Rule [{} | {} | {} | {}] could not be deleted"
                            .format(from_port, to_port, protocol, cidr))

            return

        elif arguments["rules-list"]:
            # if no arguments read default
            cloud = arguments["--cloud"] or Default.get("cloud")
            tenant = arguments["--tenant"] or Default.get("tenant")
            label = arguments["LABEL"]

            # If default not set, terminate
            if not cloud:
                Console.error("Default cloud not set!")
                return
            if not tenant:
                Console.error("Default tenant not set!")
                return

            # Get the security group
            sec_group = SecGroup.get_secgroup(label, tenant, cloud)
            if sec_group:
                # Get the rules
                result = SecGroup.get_rules(sec_group.uuid)
                print(result)
            else:
                Console.error(
                    "Security Group with label [{}], cloud [{}], and "
                    "tenant [{}] not found!"
                        .format(label, cloud, tenant))
                return

        elif arguments["rules-add"]:
            # if no arguments read default
            cloud = arguments["--cloud"] or Default.get("cloud")
            tenant = arguments["--tenant"] or Default.get("tenant")

            label = arguments["LABEL"]
            from_port = arguments["FROMPORT"]
            to_port = arguments["TOPORT"]
            protocol = arguments["PROTOCOL"]
            cidr = arguments["CIDR"]

            # If default not set, terminate
            if not cloud:
                Console.error("Default cloud not set!")
                return
            if not tenant:
                Console.error("Default tenant not set!")
                return

            # Get the security group
            sec_group = SecGroup.get_secgroup(label, tenant, cloud)
            if sec_group:
                # Add rules to the security group
                SecGroup.add_rule(sec_group, from_port, to_port, protocol,
                                  cidr)
            else:
                Console.error(
                    "Security Group with label [{}], cloud [{}], and tenant [{"
                    "}] not found!".format(label, cloud, tenant))
                return

        # TODO: Add Implementation
        elif arguments["--version"]:
            Console.ok('Version: ')


if __name__ == '__main__':
    command = cm_shell_security_group()
    command.do_security_group("list")
    command.do_security_group("a=x")
    command.do_security_group("x")
