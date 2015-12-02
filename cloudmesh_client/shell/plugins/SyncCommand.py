from __future__ import print_function

from cloudmesh_base.logger import LOGGER
from cloudmesh_base.Shell import Shell
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.default import Default

from cloudmesh_client.shell.command import PluginCommand, CloudCommand

log = LOGGER(__file__)


class SyncCommand(PluginCommand, CloudCommand):
    topics = {"sync": "system",
              "rsync": "system"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command sync")

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

    @command
    def do_sync(self, args, arguments):
        """
        ::
        
            Usage:
                sync put [--cloud=CLOUD] [--group=GROUP] LOCALDIR [REMOTEDIR]
                sync get [--cloud=CLOUD] [--group=GROUP] REMOTEDIR LOCALDIR
                sync put [--server=SERVER] [--group=GROUP] LOCALDIR [REMOTEDIR]
                sync get [--server=SERVER] [--group=GROUP] REMOTEDIR LOCALDIR

            A simple wrapper for the openstack nova command

            Arguments:
                LOCALDIR        A directory on local machine
                REMOTEDIR       A directory on remote machine

            Options:
                --cloud=CLOUD   Sync with cloud

        """
        cloudname = arguments["--cloud"] \
                    or Default.get_cloud()

        if cloudname is None:
            Console.error("Default cloud has not been set!"
                          "Please use the following to set it:\n"
                          "cm default cloud=CLOUDNAME\n"
                          "or provide it via the --cloud=CLOUDNAME argument.")
            return

        if arguments["put"]:
            TODO.implement("Yet to implement sync-put command!")
            Shell.rsync()
            pass
        elif arguments["get"]:
            TODO.implement("Yet to implement sync-get command!")
            pass

        return ""
