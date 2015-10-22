import webbrowser
import os

from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command
from cloudmesh_client.comet.comet import Comet
from cloudmesh_client.comet.cluster import Cluster
from cloudmesh_base.hostlist import Parameter

from pprint import pprint
"""



            ARGUMENTS:
                FILENAME  the file to open in the cwd if . is
                          specified. If file in in cwd
                          you must specify it with ./FILENAME
"""

# noinspection PyUnusedLocal
class CometCommand:
    topics = {"comet": "comet"}

    def __init__(self, context):
        self.context = context
        self.context.comet_token = None
        if self.context.debug:
            Console.ok("init comet command")

    @command
    def do_comet(self, args, arguments):
        """
        ::

            Usage:
               comet status
               comet tunnel start
               comet tunnel stop
               comet tunnel status
               comet logon
               comet logoff
               comet ll [ID] [--format=FORMAT]
               comet docs
               comet info [--user=USER]
                            [--project=PROJECT]
                            [--format=FORMAT]
               comet list [ID][--name=NAMES]
                            [--user=USER]
                            [--project=PROJECT]
                            [--hosts=HOSTS]
                            [--start=TIME_START]
                            [--end=TIME_END]
                            [--hosts=HOSTS]
                            [--format=FORMAT]
               comet start ID
               comet stop ID
               comet power (on|off) CLUSTERID COMPUTEIDS
               comet delete [all]
                              [--user=USER]
                              [--project=PROJECT]
                              [--name=NAMES]
                              [--hosts=HOSTS]
                              [--start=TIME_START]
                              [--end=TIME_END]
                              [--host=HOST]
               comet delete --file=FILE
               comet update [--name=NAMES]
                              [--hosts=HOSTS]
                              [--start=TIME_START]
                              [--end=TIME_END]
               comet add [--user=USER]
                           [--project=PROJECT]
                           [--host=HOST]
                           [--description=DESCRIPTION]
                           [--start=TIME_START]
                           [--end=TIME_END]
                           NAME
               comet add --file=FILENAME

            Options:
                --user=USER           user name
                --name=NAMES          Names of the vcluster
                --start=TIME_START    Start time of the vcluster, in
                                      YYYY/MM/DD HH:MM:SS format.
                                      [default: 1901-01-01]
                --end=TIME_END        End time of the vcluster, in YYYY/MM/DD
                                      HH:MM:SS format. In addition a duratio
                                      can be specified if the + sign is the
                                      first sig The duration will than be
                                      added to the start time.
                                      [default: 2100-12-31]
                --project=PROJECT     project id
                --host=HOST           host name
                --description=DESCRIPTION  description summary of the vcluster
                --file=FILE           Adding multiple vclusters from one file
                --format=FORMAT       Format is either table, json, yaml,
                                      csv, rest
                                      [default: table]

            Arguments:
                FILENAME  the file to open in the cwd if . is
                          specified. If file in in cwd
                          you must specify it with ./FILENAME

            Opens the given URL in a browser window.
        """

        try:
            logon = Comet.logon()
            if logon is False:
                Console.error("Could not logon")
                return
        except:
            Console.error("Could not logon")
        # pprint (arguments)
        output_format = arguments["--format"] or "table"

        if arguments["status"]:

            Comet.state()

        elif arguments["tunnel"] and arguments["start"]:

            Comet.tunnel(True)

        elif arguments["tunnel"] and arguments["stop"]:

            Comet.tunnel(False)

        elif arguments["tunnel"] and arguments["status"]:

            Comet.state()

        elif arguments["logon"]:

            if self.context.comet_token is None:
                if Comet.logon():
                    Console.ok("logging on")
                    self.context.comet_token = Comet.token
                else:
                    Console.error("could not logon")
            else:
                Console.error("already logged on")

        elif arguments["logoff"]:


            if self.context.comet_token is None:
                Console.error("not logged in")
            else:
                if Comet.logoff():
                    Console.ok("Logging off")
                    self.context.comet_token = None
                else:
                    Console.error("some issue while logging off. Maybe comet not reachable")

        elif arguments["ll"]:

            id = arguments["ID"] or None

            print(Cluster.simple_list(id, format=output_format))

        elif arguments["docs"]:

            Comet.docs()


        elif arguments["list"]:

            id = arguments["ID"]
            Cluster.list(id, format=output_format)

        elif arguments["info"]:

            Console.error("not yet implemented")

        elif arguments["add"]:

            print ("add the cluster")


        elif arguments["start"]:

            id = arguments["ID"]
            print("start", id)
            Cluster.start(id)

        elif arguments["stop"]:

            id = arguments["ID"]
            print("stop", id)
            Cluster.stop(id)


        elif arguments["power"]:

            clusterid = arguments["CLUSTERID"]
            computeids = Parameter.expand(arguments["COMPUTEIDS"])

            if arguments["on"]:
                on = True
            else:
                on = False

            Cluster.power(clusterid, computeids, on)
