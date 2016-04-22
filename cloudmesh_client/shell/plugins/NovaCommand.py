from __future__ import print_function
import os

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.logger import LOGGER
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.cloud.nova import Nova
from cloudmesh_client.cloud.group import Group
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.iaas.provider.openstack.CloudProviderOpenstackAPI import \
    set_os_environ
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand

log = LOGGER(__file__)


# noinspection PyBroadException
class NovaCommand(PluginCommand, CloudPluginCommand):
    topics = {"nova": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command nova")

    # noinspection PyUnusedLocal
    @command
    def do_nova(self, args, arguments):
        """
        ::
        
            Usage:
                nova set CLOUD
                nova info [CLOUD] [--password]
                nova help
                nova [--group=GROUP] ARGUMENTS...

            A simple wrapper for the openstack nova command

            Arguments:
                GROUP           The group to add vms to
                ARGUMENTS       The arguments passed to nova
                help            Prints the nova manual
                set             reads the information from the current cloud
                                and updates the environment variables if
                                the cloud is an openstack cloud
                info            the environment values for OS

            Options:
                --group=GROUP   Add VM to GROUP group
                --password      Prints the password
                -v              verbose mode

        """
        # pprint(arguments)
        cloud = arguments['CLOUD'] or Default.cloud
        if not cloud:
            Console.error("Default cloud not set!")
            return ""

        group = arguments["--group"] or Default.group

        if not group:
            Console.error("Default group not set!")
            return ""

        if arguments["help"]:
            os.system("nova help")
            return ""
        elif arguments["info"]:
            set_os_environ(cloud)
            d = {}
            #
            # TODO: this naturally does not work as clouds will have
            # different parameters. ALos it does not unset previous
            # parameters from other clouds. See register
            #
            for attribute in ['OS_USERNAME',
                              'OS_TENANT_NAME',
                              'OS_AUTH_URL',
                              'OS_CACERT',
                              'OS_PASSWORD',
                              'OS_REGION']:
                try:
                    d[attribute] = os.environ[attribute]
                except:
                    Console.warning("OS environment variable {:} not found"
                                    .format(attribute))
                    d[attribute] = None
                if not arguments["--password"]:
                    d['OS_PASSWORD'] = "********"
            print(Printer.row_table(d, order=None, labels=["Variable", "Value"]))
            msg = "info. OK."
            Console.ok(msg)
            return ""
        elif arguments["set"]:
            if cloud:

                set_os_environ(cloud)

                msg = "{0} is set".format(cloud)
                Console.ok(msg)
            else:
                Console.error("CLOUD is required")

        else:  # nova ARGUMENTS...
            print("Cloud = {0}".format(cloud))
            try:
                set_os_environ(cloud)
                args = arguments["ARGUMENTS"]

                # arguments may contain multiple optional arguments
                if len(args) == 1:
                    args = args[0].split()

                result = Shell.execute("nova", args)


                print (result)
                # print(Nova.remove_subjectAltName_warning(result))

                """
                If request for nova boot,
                add the vm to group specified,
                or else add to default group
                """
                if "boot" in args:
                    # Logic to find ID of VM in the result
                    fields = []
                    for field in result.split("|"):
                        fields.append(field.strip())
                    index = fields.index('id') + 1
                    vm_id = fields[index]

                    # Add to group
                    Group.add(name=group, species="vm", member=vm_id, category=cloud)
            except Exception as ex:
                Console.error("Error executing Nova command: {}".format(ex))
            return ""
