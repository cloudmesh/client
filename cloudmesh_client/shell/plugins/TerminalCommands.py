from __future__ import print_function
import os
import sys

from builtins import input
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import PluginCommand, ShellPluginCommand, \
    CometPluginCommand


class TerminalCommands(PluginCommand, ShellPluginCommand, CometPluginCommand):
    topics = {"clear": "shell",
              "banner": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command clear")
            print("init command banner")

            # self.register_command_topic('cloud', 'admin')

    # noinspection PyUnusedLocal
    @command
    def do_clear(self, args, arguments):
        """
        Usage:
            clear

        Clears the screen."""

        sys.stdout.write(os.popen('clear').read())

    # noinspection PyUnusedLocal
    @command
    def do_echo(self, args, arguments):
        """
        ::

            Usage:
                echo  [-r COLOR] TEXT

            Arguments:
                TEXT   The text message from which to create the banner
                COLOR  the color

            Options:
                -r COLOR  The color of the banner. [default: BLACK]

            Prints a banner form a one line text message.
        """
        Console.ok("banner")
        n = int(arguments['-n'])
        c = arguments['-c']
        i = int(arguments['-i'])
        color = arguments['-r'].upper()

        Console.cprint(color, "", i * " " + str((n - i) * c))
        Console.cprint(color, "", i * " " + c + " " + arguments['TEXT'])
        Console.cprint(color, "", i * " " + str((n - i) * c))

        return ""

    # noinspection PyUnusedLocal
    @command
    def do_banner(self, args, arguments):
        """
        ::

            Usage:
                banner [-c CHAR] [-n WIDTH] [-i INDENT] [-r COLOR] TEXT

            Arguments:
                TEXT   The text message from which to create the banner
                CHAR   The character for the frame.
                WIDTH  Width of the banner
                INDENT indentation of the banner
                COLOR  the color

            Options:
                -c CHAR   The character for the frame. [default: #]
                -n WIDTH  The width of the banner. [default: 70]
                -i INDENT  The width of the banner. [default: 0]
                -r COLOR  The color of the banner. [default: BLACK]

            Prints a banner form a one line text message.
        """
        Console.ok("banner")
        n = int(arguments['-n'])
        c = arguments['-c']
        i = int(arguments['-i'])
        color = arguments['-r'].upper()

        Console.cprint(color, "", i * " " + str((n - i) * c))
        Console.cprint(color, "", i * " " + c + " " + arguments['TEXT'])
        Console.cprint(color, "", i * " " + str((n - i) * c))

        return ""

    @command
    def do_pause(self, arg, arguments):
        """
        ::

            Usage:
                pause [MESSAGE]

            Displays the specified text then waits for the user to press RETURN.

            Arguments:
               MESSAGE  message to be displayed
        """

        if arguments["MESSAGE"] is None:
            arg = 'Press ENTER to continue'
        input(arg + '\n')

        return ""
