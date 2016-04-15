from __future__ import print_function
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default


class RefreshCommand(PluginCommand, CloudPluginCommand):
    topics = {"refresh": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command refresh")
        #try:
        #    value = Default.get_refresh()
        #except:
        #    Default.set_refresh(True)

    # noinspection PyUnusedLocal
    @command
    def do_refresh(self, args, arguments):
        """
        ::

            Usage:
                refresh on
                refresh off
                refresh [list]

                switches on and off the refresh for clouds

        """
        if arguments["on"]:
            Default.set_refresh(True)
            Console.ok("Switch refresh on")
        elif arguments["off"]:
            Default.set_refresh(False)
            Console.ok("Switch refresh off")
        else:
            refresh = Default.refresh
            if refresh:
                msg = "on"
            else:
                msg = "off"
            Console.ok("Automatic cloud refresh is switched {}".format(msg))

        return ""
