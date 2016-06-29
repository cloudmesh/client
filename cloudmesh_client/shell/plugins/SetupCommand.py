from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.default import Default
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.dotdict import dotdict
import os

class SetupCommand(PluginCommand, CloudPluginCommand):
    topics = {"setup": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command setup")

    # noinspection PyUnusedLocal
    @command
    def do_setup(self, args, arguments):
        """
        ::

            Usage:
                setup

            Examples:
                cm setup

        """
        arg = dotdict(arguments)


        #if Default.key in ["TBD", ""] or Default.user in ["TBD", ""]:
        os.system ("cm register profile")
        os.system ("cm reset")
        os.system ("cm key add --ssh")
        os.system ("cm info")

        return ""
