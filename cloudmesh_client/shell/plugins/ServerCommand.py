#! /usr/bin/env python

import os

from sandman import app
from cloudmesh_client.shell.command import command
from cloudmesh_client.common.ConfigDict import Config


class ServerCommand(object):

    topics = {"server": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command server")

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

        filename = "sqlite:///{}".format(Config.path_expand(os.path.join("~", ".cloudmesh", "cloudmesh.db")))

        print("database: {}".format(filename))
        app.config['SQLALCHEMY_DATABASE_URI'] = filename

        from sandman.model import activate

        activate()

        app.run()

if __name__ == "__main__":
    main()