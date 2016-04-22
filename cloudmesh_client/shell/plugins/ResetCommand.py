from __future__ import print_function

from cloudmesh_client.common.util import path_expand
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console

# from cloudmesh_client.shell.cm import c
import os
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand


class ResetCommand(PluginCommand, CloudPluginCommand):
    topics = {"reset": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command reset")

    # noinspection PyUnusedLocal
    @command
    def do_reset(self, args, arguments):
        """
        ::

          Usage:
              reset

        Description:

            DANGER: This method erases the database.


        Examples:
            clean

        """
        filename = path_expand("~/.cloudmesh/cloudmesh.db")
        if os.path.exists(filename):
            os.remove(filename)
        Console.ok("Database reset")
        r = self.do_quit(None)
        Console.error(
            "Quitting the shell does not yet work. please exit the shell now.")

        return ""

