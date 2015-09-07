from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console

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
                secgroup list CLOUD TENANT
                secgroup create CLOUD TENANT LABEL
                secgroup delete CLOUD TENANT LABEL
                secgroup rules-list CLOUD TENANT LABEL
                secgroup rules-add CLOUD TENANT LABEL FROMPORT TOPORT PROTOCOL CIDR
                secgroup rules-delete CLOUD TENANT LABEL FROMPORT TOPORT PROTOCOL CIDR
                secgroup -h | --help
                secgroup --version

            Options:
                -h            help message

            Arguments:
                CLOUD         Name of the IaaS cloud e.g. india_openstack_grizzly.
                TENANT        Name of the tenant, e.g. fg82.
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
                $ secgroup list india fg82
                $ secgroup rules-list india fg82 default
                $ secgroup create india fg82 webservice
                $ secgroup rules-add india fg82 webservice 8080 8088 TCP "129.79.0.0/16"

        """
        # pprint(arguments)
        if arguments["list"]:
            cloud = arguments["CLOUD"]
            tenant = arguments["TENANT"]
            Console.ok('list for cloud: {} and tenant: {}'.format(cloud, tenant))
        elif arguments["create"]:
            cloud = arguments["CLOUD"]
            tenant = arguments["TENANT"]
            label = arguments["LABEL"]
            Console.ok('create for cloud: {}, tenant: {} and label: {}'.format(cloud, tenant, label))
        elif arguments["delete"]:
            cloud = arguments["CLOUD"]
            tenant = arguments["TENANT"]
            label = arguments["LABEL"]
            Console.ok('delete for cloud: {}, tenant: {} and label: {}'.format(cloud, tenant, label))
        elif arguments["rules-list"]:
            cloud = arguments["CLOUD"]
            tenant = arguments["TENANT"]
            label = arguments["LABEL"]
            Console.ok('rules-list for cloud: {}, tenant: {} and label: {}'.format(cloud, tenant, label))
        elif arguments["rules-add"]:
            cloud = arguments["CLOUD"]
            tenant = arguments["TENANT"]
            label = arguments["LABEL"]
            from_port = arguments["FROMPORT"]
            to_port = arguments["TOPORT"]
            protocol = arguments["PROTOCOL"]
            cidr = arguments["CIDR"]
            Console.ok('rules-add for cloud: {}, '
                       'tenant: {}, '
                       'label: {}, '
                       'from port: {}, '
                       'to port: {}, '
                       'protocol: {}, '
                       'cidr: {}'.format(cloud,
                                         tenant,
                                         label,
                                         from_port,
                                         to_port,
                                         protocol,
                                         cidr))
        elif arguments["--version"]:
            Console.ok('Version: ')
        pass


if __name__ == '__main__':
    command = cm_shell_security_group()
    command.do_security_group("list")
    command.do_security_group("a=x")
    command.do_security_group("x")
