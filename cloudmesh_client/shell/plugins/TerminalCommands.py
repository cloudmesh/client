import os
import sys

from cloudmesh_client.shell.cm import command
from cloudmesh_client.shell.console import Console


class TerminalCommands(object):

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command clear")
            print("init command banner")

    @command
    def do_clear(self, arg, arguments):
        """
        Usage:
            clear

        Clears the screen."""

        sys.stdout.write(os.popen('clear').read())

    @command
    def do_banner(self, arg, arguments):
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
        print arguments
        n = int(arguments['-n'])
        c = arguments['-c']
        i = int(arguments['-i'])
        color = arguments['-r'].upper()

        
        Console._print(color, "", i * " " + (n-i) * c)
        Console._print(color, "",  i * " " + c + " " + arguments['TEXT'])
        Console._print(color, "",  i * " " + (n-i) * c)

