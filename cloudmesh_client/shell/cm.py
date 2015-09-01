from __future__ import print_function

import cmd
from .command_decorator import command
import plugins
import textwrap
import inspect
import shlex
from docopt import docopt
from pprint import pprint
import sys
import traceback

# from cloudmesh_client.shell.plugins.RegisterCommand import RegisterCommand
# from cloudmesh_client.shell.plugins.KeyCommands import KeyCommands
# import inspect

from plugins.Bar import BarCommand
from plugins.RegisterCommand import RegisterCommand
from plugins.NovaCommand import NovaCommand
from plugins.SSHCommand import SSHCommand
from plugins.KeyCommand import KeyCommand
from plugins.GroupCommand import GroupCommand
from plugins.SelectCommand import SelectCommand


class CloudmeshContext(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


# noinspection PyPep8Naming
class CloudmeshConsole(cmd.Cmd,
                       SelectCommand,
                       GroupCommand,
                       KeyCommand,
                       SSHCommand,
                       BarCommand,
                       RegisterCommand,
                       NovaCommand):
    """
    Cloudmesh Console
    """

    def __init__(self, context):
        cmd.Cmd.__init__(self)
        self.context = context
        if self.context.debug:
            print("init CloudmeshConsole")

        self.prompt = 'cm> '

        self.banner = textwrap.dedent("""
            +=======================================================+
            .   ____ _                 _                     _      .
            .  / ___| | ___  _   _  __| |_ __ ___   ___  ___| |__   .
            . | |   | |/ _ \| | | |/ _` | '_ ` _ \ / _ \/ __| '_ \  .
            . | |___| | (_) | |_| | (_| | | | | | |  __/\__ \ | | | .
            .  \____|_|\___/ \__,_|\__,_|_| |_| |_|\___||___/_| |_| .
            +=======================================================+
                                 Cloudmesh Shell
            """)
        # KeyCommands.__init__(self, context)
        for c in CloudmeshConsole.__bases__[1:]:
            c.__init__(self, context)

    def preloop(self):
        """adds the banner to the preloop"""

        if self.context.splash:
            lines = textwrap.dedent(self.banner).split("\n")
            for line in lines:
                # Console._print("BLUE", "", line)
                print(line)

    def do_EOF(self, args):
        """
        Usage:
            EOF

        Command to the shell to terminate reading a script.
        """
        return True

    def do_quit(self, args):
        """
        Usage:
            quit

        Action to be performed whne quit is typed
        """
        return True

    do_q = do_quit

    def emptyline(self):
        return

    def do_context(self, args):
        print(self.context)

    '''
    @command
    def do_bar(self, arg, arguments):
        """Usage:
                bar -f FILE
                bar FILE
                bar list

        This command does some useful things.

        Arguments:
              FILE   a file name

        Options:
              -f      specify the file

        """
        print(arguments)
    '''


def simple():
    context = CloudmeshContext(debug=False,
                               splash=True)
    con = CloudmeshConsole(context)
    con.cmdloop()


def main():
    """cm.

    Usage:
      cm --help
      cm [--debug] [--nosplash] [--file=SCRIPT] [-i] [COMMAND ...]

    Arguments:
      COMMAND                  A command to be executed

    Options:
      --file=SCRIPT  -f  SCRIPT  Executes the script
      -i                 After start keep the shell interactive,
                         otherwise quit [default: False]
      --nosplash    do not show the banner [default: False]
    """

    try:
        arg = docopt(main.__doc__, help=True)
        if arg['--help']:
            print(main.__doc__)
            sys.exit()

        # fixing the help parameter parsing

        #   arguments['COMMAND'] = ['help']
        #   arguments['help'] = 'False'

        script_file = arg['--file']

        pprint(arg)

    except:
        script_file = None
        interactive = False

        arguments = sys.argv[1:]
        print("ARG", sys.argv[1:])
        arg = {
            '--debug': '--debug' in arguments,
            '--nosplash': '--nosplash' in arguments,
            '-i': '-i' in arguments}

        for a in arg:
            if arg[a]:
                arguments.remove(a)

        arg['COMMAND'] = [' '.join(arguments)]

    print('PASS ARGS', arg)
    splash = not arg['--nosplash']
    debug = arg['--debug']
    interactive = arg['-i']
    print(splash)

    context = CloudmeshContext(debug=debug,
                               splash=splash)
    cmd = CloudmeshConsole(context)

    """
    create_cmd3_yaml_file(force=False, verbose=False)

    filename = path_expand("~/.cloudmesh/cmd3.yaml")
    try:
        module_config = ConfigDict(filename=filename)
        modules = module_config["cmd3"]["modules"]
        properties = module_config["cmd3"]["properties"]
    except:
        modules = ['cloudmesh_cmd3.plugins']
    for module_name in modules:
        #print ("INSTALL", module_name)
        try:
            plugins.append(dict(get_plugins_from_module(module_name)))
        except:
            # print "WARNING: could not find", module_name
            pass

    """

    # if script_file is not None:
    #     cmd.do_exec(script_file)

    if len(arg['COMMAND']) > 0:
        try:
            user_cmd = " ".join(arg['COMMAND'])
            if debug:
                print(">", user_cmd)
            cmd.onecmd(user_cmd)
        except Exception, e:
            print("ERROR: executing command '{0}'".format(user_cmd))
            print(70 * "=")
            print(e)
            print(70 * "=")
            print(traceback.format_exc())

        if interactive:
            cmd.cmdloop()

    elif not script_file or interactive:
        cmd.cmdloop()


if __name__ == "__main__":
    main()
    # simple()
