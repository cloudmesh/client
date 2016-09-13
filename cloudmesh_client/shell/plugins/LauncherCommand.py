# -*- coding: utf-8 -*- 
from __future__ import print_function

from pprint import pprint

from cloudmesh_client.cloud.launcher import Launcher
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import command, PluginCommand, \
    CloudPluginCommand, CometPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.hostlist import Parameter
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Printer import Printer

# Assume we have some kind of file called

# launcher.yml

#which includes so far a single variable

#name: mylauncher


#This is places in a repo called

#cloudmesh/launcher/mylauncher/launcher.yml

#We need a command that adds this to cloudmesh_launcher.yaml

#with the following functionality:

#loudmesh_launcher.yaml


#cm launcher repo add [--name launchera] https://github..../cloudmesh_launcher/test_launcher_a
#cm launcher repo delete --name launchera
#cm launcher repo list
#Reason we need the name is as we also want to be able to integrate bitbucket and others, so name of the file could be duplicated and thus we need to specify
#the actual name in the yaml file and not derive it from the repo name.
#Other ideas to come:
#cm launcher add repo nist_example_fingerprint
#cm launcher execute nist_example_fingerprint —parameters ....
#cm launcher benchmark -n 10 … (same as execute, but repeated 10 times and derive automatically some statistics on the run

"""
cm_launcher.yaml:

meta:
  version: 4.1
  kind: launcher
  filename: /Users/big/.cloudmesh/cm_launcher.yaml
  location: /Users/big/.cloudmesh/cm_launcher.yaml
  prefix: null
cloudmesh:
    repo:
      mylauncher:
          location: "https://github.com/cloudmesh/launcher/mylauncher"
      launcherb:
          location: "https://github.com/cloudmesh_launcher/test_launcher_b"
"""


class LauncherCommand(PluginCommand, CloudPluginCommand, CometPluginCommand):
    topics = {"launcher": "todo"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command launcher")

    # noinspection PyUnusedLocal
    @command
    def do_launcher(self, args, arguments):
        """
        ::

          Usage:
              launcher repo add NAME URL
              launcher repo delete NAME
              launcher repo list
              launcher repo
              launcher list [NAMES] [--cloud=CLOUD] [--format=FORMAT] [--source=db|dir]
              launcher add NAME SOURCE
              launcher delete [NAMES] [--cloud=CLOUD]
              launcher clear
              launcher run [NAME]
              launcher resume [NAME]
              launcher suspend [NAME]
              launcher refresh
              launcher log [NAME]
              launcher status [NAME]


          Arguments:

            KEY    the name of the launcher

          Options:

             --cloud=CLOUD    the name of the cloud
             --format=FORMAT  the output format [launcher: table]
             --all            lists all the launcher values

        Description:

        Launcher is a command line tool to test the portal launch
        functionalities through command line.

        The current launcher values can by listed with --all option:(
        if you have a launcher cloud specified. You can also add a
        cloud parameter to apply the command to a specific cloud)

               launcher list

            A launcher can be deleted with

                launcher delete KEY


        Examples:
            launcher list --all
            launcher list --cloud=general
            launcher delete <KEY>
        """

        print ("AAA")
        arg = dotdict(arguments)
        if arg.NAMES is not None:
            arg.names = Parameter.expand(arg.NAMES)
        else:
            arg.names = None
        if arg.name == ["all"]:
            arg.names = None
        arg.cloud = arguments["--cloud"] or Default.cloud
        arg.output = arguments['--format'] or 'table'
        arg.source = arguments['--source'] or 'db'
        print ("BBB")

        pprint(arg)

        # arg.cloud = arguments["--cloud"] or Default.cloud
        # c = arg.list
        # print ("Hallo {cloud} is list={list}".format(**arg))
        # launcher = Launcher(kind=None)

        if arg.cloud is None:
            Console.error("Default arg.cloud not set")
            return

        result = ""

        if arguments["repo"] and arguments["list"]:
            print("repo list")
            launchers = ConfigDict(filename="cm_launcher.yaml")["cloudmesh"]["repo"]
            print("repo add")
            d = {}
            for name in launchers:
                location = launchers[name]["location"]
                d[name] = {"name": name,
                           "location": location}
            print (Printer.dict_table(d))
            return ""

        elif arguments["repo"] and arguments["add"]:
            launchers = ConfigDict(filename="cm_launcher.yaml")
            print("repo add")
            print(launchers)
            return ""

        elif arguments["repo"] and arguments["delete"]:
            print("repo delete")
            return ""

        elif arguments["repo"] and not arguments["list"]:
            print(arg.names)
            result = Launcher.list(name=arg.names, output=arg.output)

        elif arguments["add"]:
            result = Launcher.add(name=arg.NAME, source=arg.SOURCE)

        elif arguments["delete"]:

            # if arg.name is not None:
            #    result = Launcher.delete(name=arg.name, category=arg.cloud)
            # else:
            #    result = Launcher.delete(name=None)

            for name in arg.names:
                result = Launcher.delete(name=name, category=arg.cloud)

        elif arguments["run"]:
            result = Launcher.run()

        elif arguments["resume"]:
            result = Launcher.resume(name=arg.name)

        elif arguments["suspend"]:
            result = Launcher.suspend(name=arg.name)

        elif arguments["details"]:
            result = Launcher.details(name=arg.name)

        elif arguments["clear"]:
            result = Launcher.clear()

        elif arguments["refresh"]:
            result = Launcher.refresh(name=arg.name)

        print(result)
