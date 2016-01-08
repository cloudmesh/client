from __future__ import print_function
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.default import Default


class RefreshCommand(PluginCommand, CloudPluginCommand):
    topics = {"refresh": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command refresh")
        try:
            value = Default.get_refresh()
        except:
            Default.set_refresh("off")

    # noinspection PyUnusedLocal
    @command
    def do_refresh(self, args, arguments):
        """
        ::

            Usage:
                refresh on
                refresh off
                refresh list

                switches on and off the refresh for clouds

        """
        if arguments["on"]:
            Default.set_refresh("on")
            Console.ok("Switch debug on")
        elif arguments["off"]:
            Default.set_refresh("off")
            Console.ok("Switch debug off")
        elif arguments["list"]:
            refresh = Default.get_refresh()
            Console.ok("Automatic cloud refresh is switched {}".format(refresh))

        return ""
