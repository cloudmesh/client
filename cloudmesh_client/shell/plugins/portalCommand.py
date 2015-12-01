from __future__ import print_function
from cloudmesh_client.cloud.default import Default
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import PluginCommand, CloudCommand

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_base.setup import os_execute

class PortalCommand(PluginCommand, CloudCommand):
    topics = {"portal": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command portal")

    def get_conf(self):
        config = ConfigDict("cloudmesh.yaml")
        data = dict(config["cloudmesh.portal"])
        print (data)
        return data

    @command
    def do_portal(self, args, arguments):
        """
        ::

            Usage:
                portal start
                portal stop

            Examples:
                portal start
                    starts the portal and opens the default web page

                portal stop
                    stops the portal

        """
        if arguments["start"]:
            ValueError("Not yet implemented")

            data = self.get_conf()
            commands = """
                cd {location}; make run &
                cd {location}; make view &
                """.format(**data)
            print (data)
            os_execute(commands)

        if arguments["start"]:
            ValueError("Not yet implemented")

            data = self.get_conf()
            commands = """
                cd {location}; make run
                """.format(**data)
            print (data)
            os_execute(commands)


        elif arguments["stop"]:
            ValueError("Not yet implemented")

        return ""


if __name__ == '__main__':
    command = cm_shell_portal()
    command.do_portal("list")
    command.do_portal("a=x")
    command.do_portal("x")
