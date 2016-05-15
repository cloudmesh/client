from __future__ import print_function

import os
import sys
from builtins import input

from cloudmesh_client.shell.command import PluginCommand, ShellPluginCommand, \
    CometPluginCommand
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
import time

class TerminalCommands(PluginCommand, ShellPluginCommand, CometPluginCommand):
    topics = {"clear": "shell",
              "echo": "shell",
              "puase": "shell",
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
    def do_sleep(self, args, arguments):
        """
        Usage:
            sleep SECONDS

        Clears the screen."""

        seconds = arguments["SECONDS"]
        time.sleep(float(seconds))


    # noinspection PyUnusedLocal
    @command
    def do_echo(self, args, arguments):
        """
        ::

            Usage:
                echo  [-r COLOR] TEXT

            Arguments:
                TEXT   The text message to print
                COLOR  the color

            Options:
                -r COLOR  The color of the text. [default: BLACK]

            Prints a text in the given color
        """
        color = arguments["-r"] or "black"
        color = color.upper()
        text = arguments["TEXT"]
        if color is "black":
            Console.msg(text)
        else:
            Console.cprint(color, "", text)

        return ""

    # noinspection PyUnusedLocal
    @command
    def do_banner(self, args, arguments):
        """
        ::

            Usage:
                banner [-c CHAR] [-n WIDTH] [-i INDENT] [-r COLOR] TEXT...

            Arguments:
                TEXT...   The text message from which to create the banner
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

        line = ' '.join(arguments['TEXT'])
        Console.cprint(color, "", i * " " + str((n - i) * c))
        Console.cprint(color, "", i * " " + c + " " + line)
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

    #
    # Echo
    #
    def set_verbose(self, on):
        # self.echo = on
        pass

    def set_banner(self, banner):
        self.banner = banner

    # @command
    # def do_loglevel(self, args, arguments):
    #     """
    #     ::
    #
    #       Usage:
    #           loglevel
    #           loglevel critical
    #           loglevel error
    #           loglevel warning
    #           loglevel info
    #           loglevel debug
    #
    #           Shows current log level or changes it.
    #
    #           loglevel - shows current log level
    #           critical - shows log message in critical level
    #           error    - shows log message in error level including critical
    #           warning  - shows log message in warning level including error
    #           info     - shows log message in info level including warning
    #           debug    - shows log message in debug level including info
    #
    #       NOTE:
    #         NOT YET IMPLEMENTED
    #     """
    #
    #
    #     if arguments['debug']:
    #         self.loglevel = "DEBUG"
    #     elif arguments['error']:
    #         self.loglevel = "ERROR"
    #     elif arguments['warning']:
    #         self.loglevel = "WARNING"
    #     elif arguments['info']:
    #         self.loglevel = "INFO"
    #     elif arguments['critical']:
    #         self.loglevel = "CRITICAL"
    #     else:
    #         Console.ok("Log level: {0}".format(self.loglevel))
    #         return ""
    #     Console.ok ("Log level: {0} is set".format(self.loglevel))
    #
    #     filename = path_expand("~/.cloudmesh/cloudmesh.yaml")
    #     config = ConfigDict(filename)
    #     config["cloudmesh.logging.level"] = self.loglevel
    #     config.write("aaa.yaml")
    #     #config.write(filename=filename, output="yaml", attribute_indent="    ")
    #     return ""

    @command
    def do_verbose(self, args, arguments):
        """
        Usage:
            verbose (True | False)
            verbose

        NOTE: NOT YET IMPLEMENTED.
        If it sets to True, a command will be printed before execution.
        In the interactive mode, you may want to set it to False.
        When you use scripts, we recommend to set it to True.

        The default is set to False

        If verbose is specified without parameter the flag is
        toggled.

        """
        # if args == '':
        #    self.echo = not self.echo
        # else:
        #    self.echo = arguments['True']

        Console.error("verbose NOT YET IMPLEMENTED")

        return ""
