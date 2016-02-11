from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command, PluginCommand, CometPluginCommand
from cloudmesh_client.comet.comet import Comet
from cloudmesh_client.comet.cluster import Cluster
import hostlist


# noinspection PyUnusedLocal,PyBroadException
class CometCommand(PluginCommand, CometPluginCommand):
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
               comet ll [CLUSTERID] [--format=FORMAT]
               comet cluster [CLUSTERID]
                             [--format=FORMAT]
               comet computeset [COMPUTESETID]
               comet power on CLUSTERID [NODESPARAM]
                            [--allocation=ALLOCATION]
                            [--walltime=WALLTIME]
               comet power (off|reboot|reset|shutdown) CLUSTERID [NODESPARAM]
               comet console CLUSTERID [COMPUTENODEID]

            Options:
                --format=FORMAT       Format is either table, json, yaml,
                                      csv, rest
                                      [default: table]
                --allocation=ALLOCATION     Allocation to charge when power on
                                            node(s)
                --walltime=WALLTIME     Walltime requested for the node(s).
                                        Walltime could be an integer value followed
                                        by a unit (m, h, d, w, for minute, hour, day,
                                        and week, respectively). E.g., 3h, 2d

            Arguments:
                CLUSTERID       The assigned name of a cluster, e.g. vc1
                COMPUTESETID    An integer identifier assigned to a computeset
                NODESPARAM      Specifying the node/nodes/computeset to act on.
                                In case of integer, will be intepreted as a computesetid;
                                in case of a hostlist format, e.g., vm-vc1-[0-3], a group
                                of nodes; or a single host is also accepptable, 
                                e.g., vm-vc1-0
                COMPUTENODEID   A compute node name, e.g., vm-vc1-0
        """
        # back up of all the proposed commands/options
        """
               comet status
               comet tunnel start
               comet tunnel stop
               comet tunnel status
               comet logon
               comet logoff
               comet ll [CLUSTERID] [--format=FORMAT]
               comet docs
               comet info [--user=USER]
                            [--project=PROJECT]
                            [--format=FORMAT]
               comet cluster [CLUSTERID][--name=NAMES]
                            [--user=USER]
                            [--project=PROJECT]
                            [--hosts=HOSTS]
                            [--start=TIME_START]
                            [--end=TIME_END]
                            [--hosts=HOSTS]
                            [--format=FORMAT]
               comet computeset [COMPUTESETID]
               comet start ID
               comet stop ID
               comet power on CLUSTERID [NODESPARAM]
                            [--allocation=ALLOCATION]
                            [--walltime=WALLTIME]
               comet power (off|reboot|reset|shutdown) CLUSTERID [NODESPARAM]
               comet console CLUSTERID [COMPUTENODEID]
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
                --allocation=ALLOCATION     Allocation to charge when power on
                                            node(s)
                --walltime=WALLTIME     Walltime requested for the node(s)

            Arguments:
                FILENAME  the file to open in the cwd if . is
                          specified. If file in in cwd
                          you must specify it with ./FILENAME

            Opens the given URL in a browser window.
        """

        """
        if not arguments["tunnel"] and Comet.tunnelled and not Comet.is_tunnel():
            Console.error("Please establish a tunnel first with:")
            print
            print ("    comet tunnel start")
            print
            return ""

        try:

            if not arguments["tunnel"]:
                logon = Comet.logon()
                if logon is False:
                    Console.error("Could not logon")
                    return ""
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
                    Console.error(
                        "some issue while logging off. Maybe comet not reachable")

        elif arguments["docs"]:

            Comet.docs()

        elif arguments["info"]:

            Console.error("not yet implemented")

        elif arguments["add"]:

            print ("add the cluster")

        elif arguments["start"]:

            cluster_id = arguments["ID"]
            print("start", cluster_id)
            Cluster.start(cluster_id)

        elif arguments["stop"]:

            cluster_id = arguments["ID"]
            print("stop", cluster_id)
            Cluster.stop(cluster_id)

        elif arguments["ll"]:

        """
        try:
            logon = Comet.logon()
            if logon is False:
                Console.error("Could not logon")
                return ""
        except:
            Console.error("Could not logon")

        output_format = arguments["--format"] or "table"

        if arguments["ll"]:
            cluster_id = arguments["CLUSTERID"] or None

            print(Cluster.simple_list(cluster_id, format=output_format))

        elif arguments["cluster"]:

            cluster_id = arguments["CLUSTERID"]
            print(Cluster.list(cluster_id, format=output_format))

        elif arguments["computeset"]:
            computeset_id = arguments["COMPUTESETID"]
            print (Cluster.computeset(computeset_id))

        elif arguments["power"]:

            clusterid = arguments["CLUSTERID"]
            fuzzyparam = None
            if 'NODESPARAM' in arguments:
                fuzzyparam = arguments["NODESPARAM"]
            param = fuzzyparam

            cluster = Cluster.list(clusterid, format='rest')
            try:
                allocations = cluster[0]['allocations']
            except:
                print (cluster)
                return ""
            # for testing only
            '''
            allocations = ['sys200',
                           'sys100',
                           'sys300',
                           'sys400',
                           'sys500',
                           'sys050',
                           'tst010',
                           'tst001']
            '''
            # no nodes param provided, action on front end
            if not fuzzyparam:
                subject = "FE"
                param = None
            # parse the nodes param
            else:
                try:
                    param = int(fuzzyparam)
                    subject = "COMPUTESET"
                    param = str(param)
                except ValueError:
                    if '[' in fuzzyparam and ']' in fuzzyparam:
                        try:
                            hosts_param = hostlist.expand_hostlist(fuzzyparam)
                        except hostlist.BadHostlist:
                            Console.error("Invalid hosts list specified!", traceflag=False)
                            return ""
                        subject = "HOSTS"
                    else:
                        subject = "HOST"

            walltime = arguments["--walltime"] or None
            allocation = arguments["--allocation"] or None
            if arguments["on"]:
                action = "on"
                walltime = Cluster.convert_to_mins(walltime)
                if not walltime:
                    print ("No valid walltime specified. Using system default")
                if not allocation:
                    if len(allocations) == 1:
                        allocation = allocations[0]
                    else:
                        allocation = Cluster.display_get_allocation(allocations)
            elif arguments["off"]:
                action = "off"
            elif arguments["reboot"]:
                action = "reboot"
            elif arguments["reset"]:
                action = "reset"
            elif arguments["shutdown"]:
                action = "shutdown"
            else:
                action = None
            print (Cluster.power(clusterid, subject, param, action, allocation, walltime))
        elif arguments["console"]:
            clusterid = arguments["CLUSTERID"]
            nodeid = None
            if 'COMPUTENODEID' in arguments:
                nodeid = arguments["COMPUTENODEID"]
            Comet.console(clusterid, nodeid)
        return ""
