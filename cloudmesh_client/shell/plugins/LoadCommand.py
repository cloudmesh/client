from __future__ import print_function
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.limits import Limits
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand


class LoadCommand(PluginCommand, CloudPluginCommand):
    topics = {"load": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command load")

    # noinspection PyUnusedLocal
    @command
    def do_load(self, args, arguments):
        """
        ::

            Usage:
                load list [--format=FORMAT]
                load reset
                load --base=MODULE PLUGINS...
                load --delete --base=MODULE PLUGINS...

                loads a plugins into the cloudmesh command shell


            OPTIONS:
                --base=MODULE  the prefix of the modules [default: cloudmesh_client.shell.plugins]
                --format=FORMAT  the output format

            ARGUMENTS:
               PLUGINS        the list of plugins to be loaded

            Examples:
                cm load list
                    lists the plugins currently loaded

                cm load reset
                    unloads all plugins that are not part of the standard plugin
                    load list

                cm load load workflow graphviz
                    loads the modules workflow and graphviz
                    the plugins are classes defined with

                        class CheckCommand(PluginCommand, CloudPluginCommand)

                    If they are located in a different moduel, the module name can either be
                    specified as part of the PLUGIN anem, or if
                     multiple modules are loaded as part of the MODULE parameter

                cm load list --format=csv
                    list sthe loaded plugins in csv format

                cm load --delete load workflow graphviz
                    the oposite of load


        """
        # print (arguments)
        Console.error("This method is not yet implemented", traceflag=False)
        return ""



