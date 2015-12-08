from __future__ import print_function
from cloudmesh_client.shell.command import command, PluginCommand, CloudPluginCommand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.default import Default


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
              cloud activate CLOUD
              cloud deactivate CLOUD
              cloud info CLOUD

          managing the admins test test test test

          Arguments:
            KEY    the name of the admin
            VALUE  the value to set the key to

          Options:
             --cloud=CLOUD    the name of the cloud [default: general]
             --format=FORMAT  the output format [default: table]

          Description:
             Cloudmesh contains a cloudmesh.yaml file that contains
             templates for multiple clouds that you may or may not have
             access to. Hence it is useful to activate and deacivate clouds
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
        # pprint(arguments)
        cloud = arguments["--cloud"] or Default.get_cloud()
        output_format = arguments["--format"]
        Console.error("TODO: Command not yet implemented.")
        pass


