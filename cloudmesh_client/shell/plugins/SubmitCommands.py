from __future__ import print_function
from cloudmesh_client.shell.command import PluginCommand
from cloudmesh_client.shell.command import command


class SubmitCommands(PluginCommand):
    topics = {"submit": "system"}

    def __init__(self, context):
        super(self.__class__, self).__init__()
        self.context = context
        if self.context.debug:
            print("init SubmitCommands")

    # noinspection PyUnusedLocal
    @command
    def do_submit(self, args, arguments):
        """
        ::

            Usage:
                submit ARGUMENTS...

            We do not yet know what this command will do ;-)

            Arguments:
                ARGUMENTS       The arguments passed to nova

            Options:
                -v              verbose mode

        """
        return "Not implemented yet."

