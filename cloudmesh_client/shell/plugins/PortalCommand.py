from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.setup import os_execute


class PortalCommand(PluginCommand, CloudPluginCommand):
    topics = {"portal": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command portal")

    def get_conf(self):
        config = ConfigDict("cloudmesh.yaml")
        data = dict(config["cloudmesh.portal"])
        print(data)
        return data

    # noinspection PyUnusedLocal
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
            print(data)
            os_execute(commands)

        if arguments["start"]:
            ValueError("Not yet implemented")

            data = self.get_conf()
            commands = """
                cd {location}; make run
                """.format(**data)
            print(data)
            os_execute(commands)

        elif arguments["stop"]:
            ValueError("Not yet implemented")

        return ""

