from __future__ import print_function

from pprint import pprint

from cloudmesh_client.cloud.launcher import Launcher
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import command, PluginCommand, \
    CloudPluginCommand, CometPluginCommand
from cloudmesh_client.shell.console import Console

class LauncherCommand(PluginCommand, CloudPluginCommand, CometPluginCommand):
    topics = {"launcher": "cloud"}

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
              launcher list [NAME] [--cloud=CLOUD] [--format=FORMAT] [--all]
              launcher add NAME SOURCE
              launcher delete [NAME] [--cloud=CLOUD]
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

        Launcher is a command line tool to test the portal launch functionalities through command

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
        pprint(arguments)

        data = dotdict(arguments)
        cloud = arguments["--cloud"] or Default.cloud
        name = data.NAME
        # data.cloud = arguments["--cloud"] or Default.cloud
        # c = data.list
        # print ("CCCC", c, data.NAME, data.cloud)
        # print ("Hallo {cloud} is list={list}".format(**data))
        # launcher = Launcher(kind=None)

        if cloud is None:
            Console.error("Default cloud not set")
            return

        result = ""

        if arguments["delete"]:
            if name is not None:
                result = Launcher.delete(name=name, category=cloud)
            else:
                result = Launcher.delete(name=None)

        elif arguments["run"]:
            result = Launcher.run()

        elif arguments["list"]:
            data.format = arguments.get("--format", "table")
            result = Launcher.list(name=name, output=data.format, category=cloud)

        elif arguments["resume"]:
            result = Launcher.resume(name=name)

        elif arguments["suspend"]:
            result = Launcher.suspend(name=name)

        elif arguments["details"]:
            result = Launcher.details(name=name)

        elif arguments["clear"]:
            result = Launcher.clear(name=name)

        elif arguments["refresh"]:
            result = Launcher.refresh(name=name)

        print(result)