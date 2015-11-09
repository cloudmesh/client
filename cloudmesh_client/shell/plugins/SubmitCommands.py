from __future__ import print_function
from cloudmesh_client.shell.command import PluginCommand

class SubmitCommands(PluginCommand):

    topics = {"submit": "tbd"}

    def __init__(self, context):
        super(self.__class__, self).__init__()
        self.context = context
        if self.context.debug:
            print("init SubmitCommands")

    def do_submit(self, args):
        print("executing key")
