from __future__ import print_function

from cloudmesh_client.logger import LOGGER
from cloudmesh_client.cloud.sync import Sync
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default

from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand

log = LOGGER(__file__)


class SyncCommand(PluginCommand, CloudPluginCommand):
    topics = {"sync": "system",
              "rsync": "system"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command sync")

    # noinspection PyUnusedLocal
    @command
    def do_rsync(self, args, arguments):
        """
        ::

            Usage:
                rsync ARGUMENTS...

            A simple wrapper for rsync command

            Arguments:
                ARGUMENTS       The arguments passed to nova

            Options:
                -v              verbose mode

        """
        return "Not implemented yet."

    # noinspection PyUnusedLocal
    @command
    def do_sync(self, args, arguments):
        """
        ::
        
            Usage:
                sync put [--cloud=CLOUD] LOCALDIR [REMOTEDIR]
                sync get [--cloud=CLOUD] REMOTEDIR LOCALDIR

            A simple wrapper for the openstack nova command

            Arguments:
                LOCALDIR        A directory on local machine
                REMOTEDIR       A directory on remote machine

            Options:
                --cloud=CLOUD   Sync with cloud

        """
        cloudname = arguments["--cloud"] or Default.cloud

        if cloudname is None:
            Console.error("Default cloud has not been set!"
                          "Please use the following to set it:\n"
                          "cm default cloud=CLOUDNAME\n"
                          "or provide it via the --cloud=CLOUDNAME argument.")
            return

        # Get the arguments
        # group = arguments["--group"] or Default.get("group", cloudname)

        localdir = arguments["LOCALDIR"]
        remotedir = arguments["REMOTEDIR"]

        if arguments["put"]:
            # validate local directory exists
            if localdir is None:
                Console.error("Please provide the [LOCALDIR] argument.")
                return ""

            result = Sync.sync(cloudname=cloudname,
                               localdir=localdir,
                               remotedir=remotedir,
                               operation="put")

            if result is not None:
                Console.ok("Successuly synced local and remote directories.")

        elif arguments["get"]:
            # validate local directory exists
            if localdir is None:
                Console.error("Please provide the [LOCALDIR] argument.")
                return ""

            result = Sync.sync(cloudname=cloudname,
                               localdir=localdir,
                               remotedir=remotedir,
                               operation="get")

            if result is not None:
                Console.ok("Successuly synced local and remote directories.")

        return ""
