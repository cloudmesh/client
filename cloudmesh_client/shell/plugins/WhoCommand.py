from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.command import PluginCommand

"""



            ARGUMENTS:
                FILENAME  the file to open in the cwd if . is
                          specified. If file in in cwd
                          you must specify it with ./FILENAME
"""


# noinspection PyUnusedLocal,PyBroadException
class WhoCommand(PluginCommand):
    topics = {"Who ": "system"}

    def __init__(self, context):
        self.context = context
        self.context.who_token = None
        if self.context.debug:
            Console.ok("init Who command")

    @command
    def do_who(self, args, arguments):
        """
        ::

            Usage:
               who  hostname

        """

        try:
            logon = who.logon()
            if logon is False:
                Console.error("Could not logon")
                return
        except:
            Console.error("Could not logon")
        # pprint (arguments)
        output_format = arguments["--format"] or "table"

        if arguments["status"]:
            pass

        ValueError("NOT yet implemented")

        return ""
