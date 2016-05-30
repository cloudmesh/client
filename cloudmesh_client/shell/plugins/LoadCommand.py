from __future__ import print_function
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.limits import Limits
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.ConfigDict import ConfigDict
import os

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
                load MODULE [PYPI]


            ARGUMENTS:
               MODULE  The name of the module

            PREDEFINED MODULE NAMES:
               vbox    loads vbox command

            Examples:
                cm load cloudmesh_vagrant.cm_vbox.do_vbox
                    lists the plugins currently loaded

        """
        arg = dotdict(arguments)

        # importlib.import_module('matplotlib.text')

        plugins = ConfigDict(filename="cloudmesh.yaml")

        if arg.MODULE == "vbox":
            arg.MODULE = "cloudmesh_vagrant.cm_vbox.do_vbox"
            arg.PYPI = "cloudmesh_vagrant"

        if arg.PYPI is not None:
            try:
                import cloudmesh_vagrant
            except:
                os.system("pip install cloudmesh_vagrant")


        try:
                print("LOADING ->", arg.MODULE)
                self.load_instancemethod(arg.MODULE)

        except:
            Console.error("Problem loading module {}".format(arg.MODULE),
                          traceflag=True)
        return ""



