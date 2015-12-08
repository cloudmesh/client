import webbrowser
import os

from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.command import PluginCommand, ShellPluginCommand, \
    CometPluginCommand


# noinspection PyUnusedLocal,PyBroadException,PyBroadException
class OpenCommand(PluginCommand, ShellPluginCommand, CometPluginCommand):
    topics = {"open": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command browser")

    def _expand_filename(self, line):
        """expands the filename if there is a . as leading path"""
        # expand .
        newline = line
        path = os.getcwd()
        if newline.startswith("."):
            newline = newline.replace(".", path, 1)
        # expand ~
        newline = os.path.expanduser(newline)
        return newline

    @command
    def do_open(self, args, arguments):
        """
        ::

            Usage:
                    open FILENAME

            ARGUMENTS:
                FILENAME  the file to open in the cwd if . is
                          specified. If file in in cwd
                          you must specify it with ./FILENAME

            Opens the given URL in a browser window.
        """
        filename = arguments['FILENAME']
        filename = self._expand_filename(filename)
        Console.ok("open {0}".format(filename))

        if not (filename.startswith("file:") or filename.startswith("http:")):
            try:
                with open(filename):
                    pass
                filename += "file://"
            except:
                Console.error(
                    "unsupported browser format in file {0}".format(filename))
                return ""

        try:
            webbrowser.open("%s" % filename)
        except:
            Console.error(
                "can not open browser with file {0}".format(filename))
