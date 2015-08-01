from __future__ import print_function
from cmd3.shell import command
from pprint import pprint
from cloudmesh_client.common.ConfigDict import Config
import os
import os.path
from cloudmesh_client.cloud.CloudRegister import CloudRegister
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.common.tables import dict_printer


class cm_shell_cloud:
    def activate_cm_shell_cloud(self):
        self.register_command_topic('cloud', 'cloud')

    @command
    def do_cloud(self, args, arguments):
        """
        ::

          Usage:
              cloud list [--output=FORMAT]


          managing the admins test test test test

          Arguments:

            KEY    the name of the admin
            VALUE  the value to set the key to

          Options:

             --cloud=CLOUD    the name of the cloud [cloud: general]
             --output=FORMAT  the output format [cloud: table]

        """
        # pprint(arguments)
        cloud = arguments["--cloud"]
        output_format = arguments["--format"]
        pass


if __name__ == '__main__':
    command = cm_shell_register()
    command.do_register("list")
