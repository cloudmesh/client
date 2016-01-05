from __future__ import print_function
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.default import Default


class DebugCommand(PluginCommand, CloudPluginCommand):
    topics = {"debug": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command debug")

    # noinspection PyUnusedLocal
    @command
    def do_debug(self, args, arguments):
        """
        ::

            Usage:
                debug on
                debug off

                switches on and off the debug messages

        """
        if arguments["on"]:

            Console.ok("Switch on debug")

        if arguments["off"]:

            Console.ok("Switch off debug")

        return ""
