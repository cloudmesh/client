from __future__ import print_function

from pprint import pprint

from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.command import PluginCommand, ShellPluginCommand


# from cloudmesh_client.cloud.command_status import command_status


# noinspection PyPep8Naming
class cm_shell_status(PluginCommand, ShellPluginCommand):
    def activate_cm_shell_status(self):
        self.register_command_topic('cloud', 'status')

    # noinspection PyUnusedLocal
    @command
    def do_status(self, args, arguments):
        """
        ::

          Usage:
              status
              status db
              status CLOUDS...




          Arguments:



          Options:



        """
        pprint(arguments)

        if arguments['db']:
            print ('status db')
        elif arguments['CLOUDS']:
            print ('status CLOUDS...')
        else:
            print ('status')
