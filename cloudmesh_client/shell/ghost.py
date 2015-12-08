from __future__ import print_function

import cmd
import sys
import traceback
import string
import textwrap

from docopt import docopt
from cloudmesh_client.cloud.default import Default
import cloudmesh_client
from cloudmesh_base.util import get_python
from cloudmesh_base.util import check_python
import cloudmesh_base
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.shell.command import command
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_base.util import path_expand

# from cloudmesh_client.shell.command import PluginCommand
from cloudmesh_client.shell.command import CometPluginCommand


class CloudmeshContext(object):
    def __init__(self, **kwargs):
        self.__dict__ = kwargs


PluginCommandClasses = type(
    'CommandProxyClass',
    tuple(CometPluginCommand.__subclasses__()),
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


# noinspection PyBroadException
class CloudmeshConsole(cmd.Cmd, PluginCommandClasses):
    # class CloudmeshConsole(cmd.Cmd,
    #                       ConsoleClasses(PluginCommand)):

    def register_topics(self):
        topics = {}
        for command in CometPluginCommand.__subclasses__():
            tmp = command.topics.copy()
            topics.update(tmp)
        for name in topics:
            self.register_command_topic(topics[name], name)
        for name in ["q", "EOF", "man"]:
            self.register_command_topic("shell", name)

    def __init__(self, context):
        cmd.Cmd.__init__(self)
        self.command_topics = {}
        self.register_topics()
        self.context = context
        if self.context.debug:
            print("init CloudmeshConsole")

        self.prompt = 'ghost> '

        self.banner = textwrap.dedent("""
            +==========================================================+
            .                          _   .-')       ('-.   .-') _    .
            .                         ( '.( OO )_   _(  OO) (  OO) )   .
            .     .-----.  .-'),-----. ,--.   ,--.)(,------./     '._  .
            .    '  .--./ ( OO'  .-.  '|   `.'   |  |  .---'|'--...__) .
            .    |  |('-. /   |  | |  ||         |  |  |    '--.  .--' .
            .   /_) |OO  )\_) |  |\|  ||  |'.'|  | (|  '--.    |  |    .
            .   ||  |`-'|   \ |  | |  ||  |   |  |  |  .--'    |  |    .
            .  (_'  '--'\    `'  '-'  '|  |   |  |  |  `---.   |  |    .
            .     `-----'      `-----' `--'   `--'  `------'   `--'    .
            +==========================================================+
                                  Comet Ghost Shell
            """)
        # KeyCommands.__init__(self, context)

        #
        # set default cloud and default group if they do not exist
        # use the first cloud in cloudmesh.yaml as default
        #
        value = Default.get('cloud', 'general')
        if value is None:
            filename = path_expand("~/.cloudmesh/cloudmesh.yaml")
            clouds = ConfigDict(filename=filename)["cloudmesh"]["clouds"]
            cloud = clouds.keys()[0]
            Default.set('cloud', cloud, 'general')

        value = Default.get('default', 'general')
        if value is None:
            Default.set('default', 'default', 'general')

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
            a = self.command_topics[topic]
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

    except:
        script_file = None
        interactive = False

        arguments = sys.argv[1:]
        arg = {
            '--debug': '--debug' in arguments,
            '--nosplash': '--nosplash' in arguments,
            '-i': '-i' in arguments}

        for a in arg:
            if arg[a]:
                arguments.remove(a)

        arg['COMMAND'] = [' '.join(arguments)]

    splash = not arg['--nosplash']
    debug = arg['--debug']
    interactive = arg['-i']

    context = CloudmeshContext(debug=debug,
                               splash=splash)
    cmd = CloudmeshConsole(context)

    # TODO: check if cludmesh_yaml exists and if not create it
    # also creat .cloudmesh dir if it not exists
    """
    from cloudmesh_client.common import cloudmesh_yaml

    create_cmd3_yaml_file(force=False, verbose=False)

    filename = cloudmesh_yaml
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
        user_cmd = None
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
