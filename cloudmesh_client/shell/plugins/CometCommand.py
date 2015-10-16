import webbrowser
import os

from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command
from cloudmesh_client.comet.comet import Comet


# noinspection PyUnusedLocal
class CometCommand:
    topics = {"comet": "comet"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init comet command")

    @command
    def do_comet(self, args, arguments):
        """
        ::

            Usage:
               comet status
               comet tunnel start
               comet tunnel stop
               comet tunnel status

            ARGUMENTS:
                FILENAME  the file to open in the cwd if . is
                          specified. If file in in cwd
                          you must specify it with ./FILENAME

            Opens the given URL in a browser window.
        """

        if arguments["status"]:

            Comet.state()

        elif arguments["tunnel"] and arguments["start"]:

            Comet.tunnel(True)

        elif arguments["tunnel"] and arguments["stop"]:

            Comet.tunnel(False)

        elif arguments["tunnel"] and arguments["status"]:

            Comet.state()
