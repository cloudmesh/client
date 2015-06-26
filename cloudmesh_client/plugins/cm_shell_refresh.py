from __future__ import print_function
import os
from cmd3.console import Console
from cmd3.shell import command
from pprint import pprint
# from cloudmesh_client.cloud.command_refresh import command_refresh


class cm_shell_refresh:
    def activate_cm_shell_refresh(self):
        self.register_command_topic('cloud', 'refresh')

    @command
    def do_refresh(self, args, arguments):
        """
        ::

           Refreshes the database with information from the clouds


           Usage:
               refresh
               refresh status
               refresh list
               refresh CLOUD...

           Arguments:

               CLOUD  (parameterized) the name of a cloud

           Description:

               Refreshes are activated on all clouds that are "active". A cloud
               can be activated with the cloud command

                  cloud activate CLOUD

               refresh
                   refreshes the information that we have about all
                   activeclouds.

               refresh CLOUD...
                   refreshes the information form the specific clouds

               refresh status
                   as the refresh may be done asynchronously, the stats will
                   show you the progress of the ongoing refresh NOT
                   IMPLEMENTED It also shows when the last refresh on a
                   specific cloud object took place.

               refresh list
                   lists all the Clouds that need a refresh

           Example:

                The following command sequences each refresh the clouds named
                india and aws.

                    refresh india,aws
                    refresh india aws
                    refresh india
                    refresh aws

             To utilize the refresh command without parameters you need to
             assure the clouds are activated

                cloud activate india
                cloud activate aws
                refresh
        """
        # pprint(arguments)
        if args is '':
            Console.ok('refresh the information')
        elif arguments['status']:
            Console.ok('Status')
        elif arguments['list']:
            Console.ok('clouds that need a refresh')
        elif arguments['CLOUD']:
            clouds = arguments['CLOUD']
            if ',' in clouds[0] and len(clouds) == 1:
                clouds = clouds[0].split(',')
            Console.ok('refresh the information of {}'.format(clouds))
        else:
            self.do_refresh.__doc__

        pass


if __name__ == '__main__':
    command = cm_shell_refresh()
    command.do_refresh("list")
    command.do_refresh("a=x")
    command.do_refresh("x")
