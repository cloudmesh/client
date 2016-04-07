from __future__ import print_function
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command, PluginCommand, \
    CloudPluginCommand, CometPluginCommand
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.launcher import Launcher
from pprint import pprint
from cloudmesh_client.common.dotdict import dotdict

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
              launcher delete [NAME] [--cloud=CLOUD]
              launcher run [NAME]
              launcher resume [NAME]
              launcher suspend [NAME]
              launcher clear
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

        c = data.list
        data.cloud = arguments["--cloud"] or Default.cloud

        print ("CCCC", c, data.NAME, data.cloud)

        print ("Hallo {cloud} is list={list}".format(**data))

        cloud = arguments["--cloud"] or Default.cloud
        launcher = Launcher(kind=None)

        if cloud is None:
            Console.error("Default cloud not set")
            return

        if arguments["list"]:

            print("CLOUD", cloud)

            # result = launcher.list(name=data.name,
            #                       category=data.cloud,
            #
            #output=data.format)
            # print(result)

        elif arguments["delete"]:

            if arguments['NAME'] is not None:
                # name = arguments["NAME"]
                # delete a launcher by name
                # remember if cloud is specified only delete it on that cloud
                # result = launcher.delete(name=name, category=cloud)
                pass
            else:
                # delete all launchers
                # remember if cloud is specified only delete it on that cloud
                pass

            #result = launcher.delete()
            #print(result)

        elif arguments["run"]:
            result = launcher.run()
            print(result)

        elif arguments["resume"]:
            result = launcher.resume()
            print(result)

        elif arguments["suspend"]:
            result = launcher.suspend()
            print(result)

        elif arguments["details"]:
            result = launcher.details()
            print(result)

        elif arguments["clear"]:
            result = launcher.clear()
            print(result)

        elif arguments["refresh"]:
            result = launcher.refresh()
            print(result)
