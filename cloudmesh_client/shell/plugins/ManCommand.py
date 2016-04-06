from __future__ import print_function
import textwrap

from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.command import PluginCommand, ShellPluginCommand, \
    CometPluginCommand


# noinspection PyBroadException
class ManCommand(PluginCommand, ShellPluginCommand, CometPluginCommand):
    topics = {"man": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command man")

    def _print_rst(self, what):
        """
        prints the rst page of the command what

        :param what: the command
        :type what: string

        """

        print
        print("Command - %s::" % what)
        h = None
        exec("h = self.do_%s.__doc__" % what)
        # noinspection PyUnboundLocalVariable
        h = textwrap.dedent(h).replace("::\n\n", "")
        h = textwrap.dedent(h).replace("\n", "\n    ")
        print(h)

    # noinspection PyUnusedLocal
    @command
    def do_man(self, args, arguments):
        """
        ::
        
            Usage:
                   man COMMAND
                   man [--noheader]

            Options:
                   --norule   no rst header

            Arguments:
                   COMMAND   the command to be printed 

            Description:
                man 
                    Prints out the help pages

                man COMMAND
                    Prints out the help page for a specific command
        """
        if arguments['COMMAND'] is None:

            print
            print("Commands")
            print(70 * "=")

            commands = [k for k in dir(self) if k.startswith("do_")]
            commands = sorted(commands, key=str.lower)

        else:
            print(arguments)
            commands = [arguments['COMMAND']]

        for command in commands:
            what = command.replace("do_", "")
            try:
                if not arguments["--noheader"]:
                    print(what)
                    print(70 * "-")
                self._print_rst(what)
            except:
                print("\n    Command documentation %s missing, help_%s" % (what, what))
            print
        return ""
