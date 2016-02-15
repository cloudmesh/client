from __future__ import print_function
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default


class DebugCommand(PluginCommand, CloudPluginCommand):
    topics = {"debug": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command debug")
        try:
            value = Default.get_debug()
        except:
            Default.set_debug("off")

    # noinspection PyUnusedLocal
    @command
    def do_debug(self, args, arguments):
        """
        ::

            Usage:
                debug on
                debug off
                debug list

                switches on and off the debug messages

        """
        if arguments["on"]:
            Default.set_debug("on")
            Console.ok("Switch debug on")
        elif arguments["off"]:
            Default.set_debug("off")
            Console.ok("Switch debug off")
        elif arguments["list"]:
            debug = Default.debug()
            Console.ok("Debug is switched {}".format(debug))

        return ""
