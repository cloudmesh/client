from __future__ import print_function

from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.common.ConfigDict import ConfigDict
from pprint import pprint


class CloudCommand(PluginCommand, CloudPluginCommand):
    topics = {"cloud": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command cloud")

    # noinspection PyUnusedLocal
    @command
    def do_cloud(self, args, arguments):
        """
        ::

          Usage:
              cloud list [--cloud=CLOUD] [--format=FORMAT]
              cloud logon CLOUD
              cloud logout CLOUD
              cloud activate CLOUD
              cloud deactivate CLOUD
              cloud info CLOUD

          managing the admins test test test test

          Arguments:
            KEY    the name of the admin
            VALUE  the value to set the key to

          Options:
             --cloud=CLOUD    the name of the cloud
             --format=FORMAT  the output format [default: table]

          Description:
             Cloudmesh contains a cloudmesh.yaml file that contains
             templates for multiple clouds that you may or may not have
             access to. Hence it is useful to activate and deactivate clouds
             you like to use in other commands.

             To activate a cloud a user can simply use the activate
             command followed by the name of the cloud to be
             activated. To find out which clouds are available you can
             use the list command that will provide you with some
             basic information. As default it will print a table. Thus
             the commands::

               cloud activate india
               cloud deactivate aws

             Will result in

                +----------------------+--------+-------------------+
                | Cloud name           | Active | Type              |
                +----------------------+--------+-------------------+
                | india                | True   | Openstack         |
                +----------------------+--------+-------------------+
                | aws                  | False  | AWS               |
                +----------------------+--------+-------------------+

             To get ore information about the cloud you can use the command

                cloud info CLOUD

             It will call internally also the command uses in register

          See also:
             register
        """

        cloudname = arguments["--cloud"] or Default.cloud

        if arguments["logon"]:
            cloudname = arguments["CLOUD"]
            provider = CloudProvider(cloudname).provider
            provider.logon(cloudname)
            Console.ok("Logged into cloud: " + cloudname)

        elif arguments["logout"]:
            cloudname = arguments["CLOUD"]
            provider = CloudProvider(cloudname).provider
            provider.logout(cloudname)
            Console.ok("Logged out of cloud: " + cloudname)

        elif arguments["activate"]:
            cloudname = arguments["CLOUD"]
            provider = CloudProvider(cloudname).provider
            provider.activate(cloudname)
            Console.ok("Activated cloud: " + cloudname)

        elif arguments["deactivate"]:
            cloudname = arguments["CLOUD"]
            provider = CloudProvider(cloudname).provider
            provider.deactivate(cloudname)
            Console.ok("Deactivated cloud: " + cloudname)

        elif arguments["list"]:
            provider = CloudProvider(cloudname).provider
            clouds = provider.list_clouds()
            default = Default.cloud
            active = ConfigDict("cloudmesh.yaml")["cloudmesh"]["active"]
            key = Default.get_key()

            def yes(state):
                if state:
                    return "*"
                else:
                    return " "

            for index in clouds:
                cloud = clouds[index]
                cloud["active"] = yes(cloud["cloud"] in active)
                cloud["default"] = yes(cloud["cloud"] == default)
                cloud["key"] = key
                cloud["id"] = index

            (order, header) = CloudProvider(cloudname).get_attributes("clouds")

            Console.msg(Printer.write(clouds, order=order, header=header))
        return ""
