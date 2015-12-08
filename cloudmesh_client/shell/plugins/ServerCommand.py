#! /usr/bin/env python

import os

from cloudmesh_client.shell.command import command
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand


class ServerCommand(PluginCommand, CloudPluginCommand):
    topics = {"server": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command server")

    # noinspection PyUnusedLocal
    @command
    def do_server(self, args, arguments):
        """
        Usage:
            server

        Options:
          -h --help
          -v       verbose mode

        Description:
          Starts up a REST service and a WEB GUI so one can browse the data in an
          existing cloudmesh database.

          The location of the database is supposed to be in

            ~/.cloud,esh/cloudmesh.db

        """

        # import warnings
        # with warnings.catch_warnings():
        #    warnings.filter("ignore")
        # ignore "SQLALCHEMY_TRACK_MODIFICATIONS")

        from sandman import app
        from sandman.model import activate

        filename = "sqlite:///{}".format(Config.path_expand(
            os.path.join("~", ".cloudmesh", "cloudmesh.db")))

        print("database: {}".format(filename))

        app.config['SQLALCHEMY_DATABASE_URI'] = filename
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        activate()

        app.run()

