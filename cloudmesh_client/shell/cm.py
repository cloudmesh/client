from __future__ import print_function

import datetime
import cmd
import sys
import traceback
import string
import textwrap
import os
from docopt import docopt
import shutil

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_base.util import path_expand
from cloudmesh_client.shell.console import Console
from cloudmesh_base.Shell import Shell

import cloudmesh_client


def create_cloudmesh_yaml(filename):
    if not os.path.exists(filename):
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            Shell.mkdir(path)
        etc_path = os.path.dirname(cloudmesh_client.__file__)
        etc_file = os.path.join(etc_path, "etc", "cloudmesh.yaml")
        to_dir = path_expand("~/.cloudmesh")
        shutil.copy(etc_file, to_dir)
        Console.ok("~/.cloudmesh/cloudmesh.yaml created")


filename = path_expand("~/.cloudmesh/cloudmesh.yaml")
create_cloudmesh_yaml(filename)
os.system("chmod -R go-rwx " + path_expand("~/.cloudmesh"))

# noinspection PyPep8
from .plugins import *
from cloudmesh_client.cloud.default import Default
from cloudmesh_base.util import get_python
from cloudmesh_base.util import check_python
import cloudmesh_base
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.command import PluginCommand
from cloudmesh_base.ssh_config import ssh_config
import cloudmesh_client.etc


class CloudmeshContext(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


PluginCommandClasses = type(
    'CommandProxyClass',
    tuple(PluginCommand.__subclasses__()),
    {})

"""
print (type(PluginCommand.__subclasses__()))

# not yet implemented
class ConsoleClasses(object):

    def __init__(self, *command_classes):

        classes = []
        for c in command_classes:
            classes.append(PluginCommand.__subclasses__())
        print (classes)

        PluginCommandClasses = type(
            'CommandProxyClass',
            tuple(classes),
            {})

        return PluginCommandClasses
"""


# console = ConsoleFactory(PluginCommand)


# noinspection PyBroadException,PyPep8Naming
class CloudmeshConsole(cmd.Cmd, PluginCommandClasses):
    # class CloudmeshConsole(cmd.Cmd,
    #                       ConsoleClasses(PluginCommand)):

    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        """
        line = self.replace_vars(line)
        if line != "hist" and line:
            self._hist += [line.strip()]
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if os.path.isfile(line):
            self.do_exec(line)
            return ""
        if line.startswith('#') \
                or line.startswith('//') \
                or line.startswith('/*'):
            print(line)
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            return func(arg)

    def register_topics(self):
        topics = {}
        for command in PluginCommand.__subclasses__():
            tmp = command.topics.copy()
            topics.update(tmp)
        for name in topics:
            self.register_command_topic(topics[name], name)
        for name in ["q", "EOF", "man", "version", "help", "history",
                     "pause", "quit", "var"]:
            self.register_command_topic("shell", name)

    def __init__(self, context):
        cmd.Cmd.__init__(self)
        self.variables = {}
        self.command_topics = {}
        self.register_topics()
        self.context = context
        self._hist = []
        if self.context.debug:
            print("init CloudmeshConsole")

        self.prompt = 'cm> '
        self.doc_header = "Documented commands (type help <command>):"
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

        #
        # set default cloud and default group if they do not exist
        # use the first cloud in cloudmesh.yaml as default
        #

        filename = path_expand("~/.cloudmesh/cloudmesh.yaml")
        create_cloudmesh_yaml(filename)

        # sys,exit(1)

        value = Default.get('cloud', cloud='general')
        if value is None:
            clouds = ConfigDict(filename=filename)["cloudmesh"]["clouds"]
            cloud = clouds.keys()[0]
            Default.set('cloud', cloud, cloud='general')

        value = Default.get('default', cloud='general')
        if value is None:
            Default.set('default', 'default', cloud='general')

        cluster = 'kilo'  # hardcode a value if not defined
        value = Default.get('cluster', cloud='general')
        if value is None:
            try:
                hosts = ssh_config().names()
                if hosts is not None:
                    cluster = hosts[0]
            except:
                pass  # use the hardcoded cluster

        else:
            cluster = value
        Default.set('cluster', cluster, cloud='general')

        #
        # Read cloud details from yaml file
        #
        filename = 'cloudmesh.yaml'
        config = ConfigDict(filename=filename)["cloudmesh"]
        clouds = config["clouds"]

        defaults = {
            'clouds': {},
            'key': {}
        }

        for cloud in clouds:
            if "default" in config['clouds'][cloud]:
                defaults['clouds'][cloud] = config["clouds"][cloud]['default']

        if "default" in config["keys"]:
            defaults["keys"] = config["keys"]["default"]
            if config["keys"] in ["None", "TBD"]:
                defaults['key'] = None
        else:
            defaults['key'] = None

        for cloud in defaults["clouds"]:
            for default, value in defaults["clouds"][cloud].iteritems():

                try:
                    value = Default.get(default, cloud=cloud)
                except:
                    pass

                Default.set(default, value, cloud=cloud)

        for c in CloudmeshConsole.__bases__[1:]:
            # noinspection PyArgumentList
            c.__init__(self, context)

    def preloop(self):
        """adds the banner to the preloop"""

        if self.context.splash:
            lines = textwrap.dedent(self.banner).split("\n")
            for line in lines:
                # Console.cprint("BLUE", "", line)
                print(line)

    # noinspection PyUnusedLocal
    def do_EOF(self, args):
        """
        ::

            Usage:
                EOF

            Description:
                Command to the shell to terminate reading a script.
        """
        return True

    # noinspection PyUnusedLocal
    def do_quit(self, args):
        """
        ::

            Usage:
                quit

            Description:
                Action to be performed whne quit is typed
        """
        return True

    do_q = do_quit

    def emptyline(self):
        return

    # noinspection PyUnusedLocal
    def do_context(self, args):
        """
        ::

            Usage:
                context

            Description:
                Lists the context variables and their values
        """
        """
        :param args:
        :return:
        """
        print(self.context.__dict__)

    # noinspection PyUnusedLocal
    @command
    def do_version(self, args, arguments):
        """
        Usage:
           version [--format=FORMAT] [--check=CHECK]

        Options:
            --format=FORMAT  the format to print the versions in [default: table]
            --check=CHECK    boolean tp conduct an additional check [default: True]

        Description:
            Prints out the version number
        """

        python_version, pip_version = get_python()

        versions = {
            "cloudmesh_client": {
                "name": "cloudmesh_client",
                "version": str(cloudmesh_client.__version__)
            },
            "cloudmesh_base": {
                "name": "cloudmesh_base",
                "version": str(cloudmesh_base.__version__)
            },
            "python": {
                "name": "python",
                "version": str(python_version)
            },
            "pip": {
                "name": "pip",
                "version": str(pip_version)
            }
        }

        print(dict_printer(versions, output=arguments["--format"],
                           order=["name", "version"]))
        if arguments["--check"] in ["True"]:
            check_python()

    def register_command_topic(self, topic, command_name):
        try:
            tmp = self.command_topics[topic]
        except:
            self.command_topics[topic] = []
        self.command_topics[topic].append(command_name)

    def do_help(self, arg):
        """
        ::

            Usage:
                help
                help COMMAND

            Description:
                List available commands with "help" or detailed help with
                "help COMMAND"."""

        if arg:
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc = getattr(self, 'do_' + arg).__doc__
                    if doc:
                        self.stdout.write("%s\n" % str(doc))
                        return
                except AttributeError:
                    pass
                self.stdout.write("%s\n" % str(self.nohelp % (arg,)))
                return
            func()
        else:
            names = self.get_names()
            cmds_doc = []
            cmds_undoc = []
            help_page = {}
            for name in names:
                if name[:5] == 'help_':
                    help_page[name[5:]] = 1
            names.sort()
            # There can be duplicates if routines overridden
            prevname = ''
            for name in names:
                if name[:3] == 'do_':
                    if name == prevname:
                        continue
                    prevname = name
                    cmd = name[3:]
                    if cmd in help_page:
                        cmds_doc.append(cmd)
                        del help_page[cmd]
                    elif getattr(self, name).__doc__:
                        cmds_doc.append(cmd)
                    else:
                        cmds_undoc.append(cmd)

            self.stdout.write("%s\n" % str(self.doc_leader))
            self.print_topics(self.doc_header, cmds_doc, 15, 80)
            self.print_topics(self.misc_header, list(help_page.keys()), 15, 80)
            self.print_topics(self.undoc_header, cmds_undoc, 15, 80)

            for topic in self.command_topics:
                topic_cmds = sorted(self.command_topics[topic], key=str.lower)
                self.print_topics(string.capwords(topic + " commands"),
                                  topic_cmds, 15, 80)

    def help_help(self):
        """
        ::

            Usage:
               help NAME

            Prints out the help message for a given function
        """
        print(textwrap.dedent(self.help_help.__doc__))

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

    def do_exec(self, filename):
        """
        ::

            Usage:
               exec FILENAME

            executes the commands in the file. See also the script command.

            Arguments:
              FILENAME   The name of the file
        """
        if not filename:
            Console.error("the command requires a filename as parameter")
            return

        if os.path.exists(filename):
            with open(filename, "r") as f:
                for line in f:
                    #if self.debug:
                    Console.ok("> {:}".format(str(line)))
                    self.onecmd(line)
        else:
            Console.error('file "{:}" does not exist.'.format(filename))
            sys.exit()

    # noinspection PyUnusedLocal
    @command
    def do_shell(self, args, arguments):
        """
        Usage:
           shell ARGUMENTS...

        Description:
            Executes a shell command
        """
        # just ignore arguments and pass on args
        os.system(args)

    #
    # VAR
    #

    def update_time(self):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        self.variables['time'] = time
        self.variables['date'] = date

    def replace_vars(self, line):

        self.update_time()

        newline = line
        for v in self.variables:
            newline = newline.replace("$" + v, self.variables[v])
        for v in os.environ:
            newline = newline.replace("$" + v, os.environ[v])
        return newline

    def _add_variable(self, name, value):
        self.variables[name] = value
        # self._list_variables()

    def _delete_variable(self, name):
        self._list_variables()
        del self.variables[name]
        # self._list_variables()

    def _list_variables(self):
        Console.ok(10 * "-")
        Console.ok('Variables')
        Console.ok(10 * "-")
        for v in self.variables:
            Console.ok("{:} = {:}".format(v, self.variables[v]))

    @command
    def do_var(self, arg, arguments):
        """
        Usage:
            var list
            var delete NAMES
            var NAME=VALUE
            var NAME
        Arguments:
            NAME    Name of the variable
            NAMES   Names of the variable separated by spaces
            VALUE   VALUE to be assigned
        special vars date and time are defined
        """
        if arguments['list'] or arg == '' or arg is None:
            self._list_variables()
            return ""

        elif arguments['NAME=VALUE'] and "=" in arguments["NAME=VALUE"]:
            (variable, value) = arg.split('=', 1)
            if value == "time" or value == "now":
                value = datetime.datetime.now().strftime("%H:%M:%S")
            elif value == "date":
                value = datetime.datetime.now().strftime("%Y-%m-%d")
            elif "." in value:
                try:
                    config = ConfigDict("cloudmesh.yaml")
                    value = config[value]
                except Exception, e:
                    Console.error("can not find variable {} in cloudmesh.yaml".format(value))
                    value = None
            self._add_variable(variable, value)
            return ""
        elif arguments['NAME=VALUE'] and "=" in arguments["NAME=VALUE"]:
            try:
                v = arguments['NAME=VALUE']
                Console.ok(str(self.variables[v]))
            except:
                Console.error('variable {:} not defined'.format(arguments['NAME=VALUE']))

        elif arg.startswith('delete'):
            variable = arg.split(' ')[1]
            self._delete_variable(variable)
            return ""

    @command
    def do_history(self, args, arguments):
        """
        Usage:
            history
            history list
            history last
            history ID
        """
        try:
            if arguments["list"] or args == "":
                print ("LIST")
                h = 0
                for line in self._hist:
                    print ("{}: {}".format(h, self._hist[h]))
                    h = h + 1
                return ""

            elif arguments["last"]:
                h = len(self._hist)
                if (h > 1):
                    self.onecmd(self._hist[h-2])
                return ""

            elif arguments["ID"]:
                h = int(arguments["ID"])
                if h in range(0, len(self._hist)):
                    print ("{}".format(self._hist[h]))
                    if not args.startswith("history"):
                        self.onecmd(self._hist[h])
                return ""
        except:
            Console.error("could not execute the last command")

    do_h = do_history


def simple():
    context = CloudmeshContext(debug=False,
                               splash=True)
    con = CloudmeshConsole(context)
    con.cmdloop()


# noinspection PyBroadException
def main():
    """cm.

    Usage:
      cm --help
      cm [--debug] [--nosplash] [-i] [COMMAND ...]

    Arguments:
      COMMAND                  A command to be executed

    Options:
      --file=SCRIPT  -f  SCRIPT  Executes the script
      -i                 After start keep the shell interactive,
                         otherwise quit [default: False]
      --nosplash    do not show the banner [default: False]
    """

    def manual():
        print(main.__doc__)



    args = sys.argv[1:]


    print (args)


    arguments = {
        '--debug': '--debug' in args,
        '--nosplash': '--nosplash' in args,
        '-i': '-i' in args}

    for a in args:
        if a in arguments:
            args.remove(a)

    arguments['COMMAND'] = [' '.join(args)]

    print (arguments)

    commands = arguments["COMMAND"]
    if len(commands) > 0:
        if ".cm" in commands[0]:
            arguments["SCRIPT"] = commands[0]
            commands = commands[1:]
        else:
            arguments["SCRIPT"] = None

        arguments["COMMAND"] = ' '.join(commands)
        if arguments["COMMAND"] == '':
            arguments["COMMAND"] = None


    if arguments['COMMAND'] == []:
        arguments['COMMAND'] = None

    splash = not arguments['--nosplash']
    debug = arguments['--debug']
    interactive = arguments['-i']
    script = arguments["SCRIPT"]
    command = arguments["COMMAND"]



    context = CloudmeshContext(debug=debug,
                               splash=splash)
    cmd = CloudmeshConsole(context)


    if script is not None:
        cmd.do_exec(script)

    try:
        if debug:
            print(">", command)
        if command is not None:
            cmd.onecmd(command)
    except Exception, e:
        print("ERROR: executing command '{0}'".format(command))
        print(70 * "=")
        print(e)
        print(70 * "=")
        print(traceback.format_exc())

    if interactive or (command is None and script is None):
        cmd.cmdloop()


if __name__ == "__main__":
    main()
    # simple()
