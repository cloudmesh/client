from __future__ import print_function
import os
import sys
from cloudmesh_client.shell.cm import command
from cloudmesh_client.shell.console import Console
from cloudmesh_base.logger import LOGGER
from cloudmesh_base.tables import row_table
from cloudmesh_base.Shell import Shell
from cloudmesh_client.cloud.nova import Nova

from pprint import pprint
import warnings
import urllib3

log = LOGGER(__file__)


class NovaCommand (object):


    topics = {"nova": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print ("init command nova")

    @command
    def do_nova(self, args, arguments):
        """
        ::
        
          Usage:
                 nova set CLOUD
                 nova info [CLOUD] [--password]
                 nova help
                 nova ARGUMENTS...

          A simple wrapper for the openstack nova command

          Arguments:

            ARGUMENTS      The arguments passed to nova
            help           Prints the nova manual
            set            reads the information from the current cloud
                           and updates the environment variables if
                           the cloud is an openstack cloud
            info           the environment values for OS

          Options:
             --password    Prints the password
             -v            verbose mode

        """
        # pprint(arguments)
        cloud = arguments['CLOUD']
        if cloud is None:
            cloud = "india"

        if arguments["help"]:
            os.system("nova help")
            return
        elif arguments["info"]:
            nova.set_os_environ(cloud)
            d = {}
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
            print(row_table(d, order=None, labels=["Variable", "Value"]))
            msg = "info. OK."
            Console.ok(msg)
            return
        elif arguments["set"]:
            if cloud:

                nova.set_os_environ(cloud)

                msg = "{0} is set".format(cloud)
                Console.ok(msg)
            else:
                Console.error("CLOUD is required")

        else:  # nova ARGUMENTS...
            nova.set_os_environ(cloud)
            args = arguments["ARGUMENTS"]
            result = Shell.execute("nova", args)
            print(nova.remove_subjectAltName_warning(result))
            return
