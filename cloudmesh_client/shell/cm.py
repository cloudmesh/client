from __future__ import print_function

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
os.system("chmod -R go-rwx " + filename = path_expand("~/.cloudmesh"))
#
# cahnge permission
#

from .plugins import *


from cloudmesh_client.cloud.default import Default

import cloudmesh_base
from cloudmesh_base.util import get_python
from cloudmesh_base.util import check_python
import cloudmesh_base
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.shell.command import command

from cloudmesh_client.shell.command import PluginCommand
from cloudmesh_base.ssh_config import ssh_config

from pprint import pprint

from cloudmesh_client.common.ConfigDict import dprint

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
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if line.startswith('#') \
                or line.startswith('//') \
                or line.startswith('/*'):
            print (line)
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF' :
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
        for name in ["q", "EOF", "man"]:
            self.register_command_topic("shell", name)


    def __init__(self, context):
        cmd.Cmd.__init__(self)
        self.command_topics = {}
        self.register_topics()
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

        #
        # set default cloud and default group if they do not exist
        # use the first cloud in cloudmesh.yaml as default
        #

        filename = path_expand("~/.cloudmesh/cloudmesh.yaml")
        create_cloudmesh_yaml(filename)

        #sys,exit(1)


        value = Default.get('cloud', cloud='general')
        if value is None:
            clouds = ConfigDict(filename=filename)["cloudmesh"]["clouds"]
            cloud = clouds.keys()[0]
            Default.set('cloud', cloud, cloud='general')

        value = Default.get('default', cloud='general')
        if value is None:
            Default.set('default', 'default', cloud='general')

        cluster = 'india'  # hardcode a value if not defined
        value = Default.get('cluster', cloud='general')
        if value is None:
            try:
                hosts = ssh_config().names()
                if hosts is not None:
                    cluster = hosts[0]
            except:
                pass  # use the hardcoded cluster
        Default.set('cluster', cluster,  cloud='general')


        #
        # Read cloud details from yaml file
        #
        filename = 'cloudmesh.yaml'
        config = ConfigDict(filename=filename)["cloudmesh"]
        clouds = config["clouds"]

        defaults = {'clouds': {},
                    'key': {}}

        for cloud in clouds:
            if "default" in  config['clouds'][cloud]:
                defaults['clouds'][cloud] = config["clouds"][cloud]['default']

        if "default" in config["keys"]:
            defaults["keys"] = config["keys"]["default"]
        else:
            defaults['key'] = None


        for cloud in defaults["clouds"]:
            for default,value in defaults["clouds"][cloud].iteritems():
                Default.set(default, value, cloud=cloud)

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
        ::

            Usage:
                EOF

            Description:
                Command to the shell to terminate reading a script.
        """
        return True

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
                    Console.ok("> {:}".format(str(line)))
                    self.onecmd(line)
        else:
            Console.error('file "{:}" does not exist.'.format(filename))
            sys.exit()



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

    if len(arg['COMMAND']) ==  1:
        command = arg['COMMAND'][0]
        print (command)
        if command.endswith(".cm"):
            script_file = command

    if script_file is not None:
         cmd.do_exec(script_file)

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
