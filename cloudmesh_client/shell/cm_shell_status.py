from __future__ import print_function
from cloudmesh_client.shell.command import command, PluginCommand, \
    ShellPluginCommand


# noinspection PyPep8Naming
class cm_shell_status(PluginCommand, ShellPluginCommand):
    topics = {"status": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init status default")

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
        # pprint(arguments)

        if arguments['db']:
            print('status db')
        elif arguments['CLOUDS']:
            print('status CLOUDS...')
        else:
            print('status')
