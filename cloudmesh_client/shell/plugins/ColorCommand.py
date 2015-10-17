from __future__ import print_function
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command
from cloudmesh_client.common.ConfigDict import ConfigDict


class ColorCommand(object):
    topics = {"color": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command color")

    @command
    def do_color(self, args, arguments):
        """
        ::

            Usage:
                color mode FLAG

            Arguments:

                FLAG    color mode flag ON/OFF

            Description:

                Global switch for the console color mode.
                One can switch the color mode on/off with
                    cm color mode ON
                    cm color mode OFF

                By default, the color mode is ON

            Examples:
                color mode ON
                color mode OFF
        """

        # default mode is ON
        color_mode = True

        if arguments["mode"]:
            flag = arguments["FLAG"]
            if flag == "ON":
                color_mode = True
            elif flag == "OFF":
                color_mode = False
            else:
                Console.error("Invalid Flag")
                return

        # Update the cloudmesh.yaml file
        config = ConfigDict("cloudmesh.yaml")
        config["cloudmesh"]["system"]["console_color"] = color_mode
        config.save()

        Console.color = color_mode
        Console.ok("Color Mode Changed Successfully!")

        pass