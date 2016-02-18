from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command, PluginCommand, CometPluginCommand
from cloudmesh_client.comet.comet import Comet
from cloudmesh_client.comet.cluster import Cluster
from cloudmesh_client.common.hostlist import Parameter
import hostlist
import os
import sys

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
               comet power on CLUSTERID [--count=NUMNODES] [NODESPARAM]
                            [--allocation=ALLOCATION]
                            [--walltime=WALLTIME]
               comet power (off|reboot|reset|shutdown) CLUSTERID [NODESPARAM]
               comet console CLUSTERID [COMPUTENODEID]
               comet image list
               comet image upload [--imagename=IMAGENAME] PATHIMAGEFILE
               comet image attach IMAGENAME CLUSTERID [COMPUTENODEIDS]
               comet image detach CLUSTERID [COMPUTENODEIDS]
               comet node rename CLUSTERID OLDNAME NEWNAME

            Options:
                --format=FORMAT         Format is either table, json, yaml,
                                        csv, rest
                                        [default: table]
                --count=NUMNODES        Number of nodes to be powered on.
                                        When this option is used, the comet system
                                        will find a NUMNODES number of arbitrary nodes
                                        that are available to boot as a computeset
                --allocation=ALLOCATION     Allocation to charge when power on
                                            node(s)
                --walltime=WALLTIME     Walltime requested for the node(s).
                                        Walltime could be an integer value followed
                                        by a unit (m, h, d, w, for minute, hour, day,
                                        and week, respectively). E.g., 3h, 2d
                --imagename=IMAGENAME   Name of the image after being stored remotely.
                                        If not specified, use the original filename

            Arguments:
                CLUSTERID       The assigned name of a cluster, e.g. vc1
                COMPUTESETID    An integer identifier assigned to a computeset
                NODESPARAM      Specifying the node/nodes/computeset to act on.
                                In case of integer, will be intepreted as a computesetid;
                                in case of a hostlist format, e.g., vm-vc1-[0-3], a group
                                of nodes; or a single host is also acceptable,
                                e.g., vm-vc1-0
                                If not provided, the requested action will be taken
                                on the frontend node of the specified cluster
                COMPUTENODEID   A compute node name, e.g., vm-vc1-0
                                If not provided, the requested action will be taken
                                on the frontend node of the specified cluster
                COMPUTENODEIDS  A set of compute node names in hostlist format,
                                e.g., vm-vc1-[0-3]
                                One single node is also acceptable: vm-vc1-0
                                If not provided, the requested action will be taken
                                on the frontend node of the specified cluster
                IMAGENAME       Name of an image at remote server
                PATHIMAGEFILE   The full path to the image file to be uploaded
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
            numnodes = arguments["--count"] or None
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

            if not numnodes:
                fuzzyparam = None
                if 'NODESPARAM' in arguments:
                    fuzzyparam = arguments["NODESPARAM"]
                param = fuzzyparam

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
            else:
                try:
                    param = int(numnodes)
                except ValueError:
                    Console.error("Invalid count value specified!", traceflag=False)
                    return ""
                if param > 0:
                    subject = "HOSTS"
                    param = None
                else:
                    Console.error("count value has to be greather than zero")
                    return ""
            walltime = arguments["--walltime"] or None
            allocation = arguments["--allocation"] or None
            if arguments["on"]:
                action = "on"
                if subject in ["HOSTS", "HOST"]:
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
            print (Cluster.power(clusterid,
                                 subject,
                                 param,
                                 action,
                                 allocation,
                                 walltime,
                                 numnodes)
                  )
        elif arguments["console"]:
            clusterid = arguments["CLUSTERID"]
            nodeid = None
            if 'COMPUTENODEID' in arguments:
                nodeid = arguments["COMPUTENODEID"]
            Comet.console(clusterid, nodeid)
        elif arguments["image"]:
            if arguments["list"]:
                images = (Comet.list_image())
                idx = 0
                for image in images:
                    if image.startswith("public/"):
                        image = image.split("/")[1]
                    idx += 1
                    print ("{}: {}".format(idx, image))
            if arguments["upload"]:
                imagefile = arguments["PATHIMAGEFILE"]
                imagefile = os.path.abspath(imagefile)
                if os.path.isfile(imagefile):
                    if arguments["--imagename"]:
                        filename = arguments["--imagename"]
                    else:
                        filename = os.path.basename(imagefile)
                else:
                    print ("File does not exist - {}"\
                                  .format(arguments["PATHIMAGEFILE"]))
                    return ""
                print (Comet.upload_image(filename, imagefile))
            elif arguments["attach"]:
                imagename = arguments["IMAGENAME"]
                clusterid = arguments["CLUSTERID"]
                computenodeids = arguments["COMPUTENODEIDS"] or None
                print (Cluster.attach_iso(imagename, clusterid, computenodeids))
            elif arguments["detach"]:
                clusterid = arguments["CLUSTERID"]
                computenodeids = arguments["COMPUTENODEIDS"] or None
                print (Cluster.detach_iso(clusterid, computenodeids))
        elif arguments["node"]:
            if arguments["rename"]:
                clusterid = arguments["CLUSTERID"]
                oldname = arguments["OLDNAME"]
                newname = arguments["NEWNAME"]
                if newname is None or newname == '':
                    print ("New node name cannot be empty")
                else:
                    print (Cluster.rename_node(clusterid, oldname, newname))

            '''
            # bulk rename

            if arguments["rename"]:
               oldnames = Parameter.expand(arguments["OLDNAME"])
               newnames = Parameter.expand(arguments["NEWNAME"])

               # check if new names ar not already taken
               # to be implemented

               if len(oldnames) == len(newnames):
                   for i in range(0,len(oldnames)):
                       oldname = oldnames[i]
                       newname = newnames[i]
                   if newname is None or newname == '':
                       print ("New node name cannot be empty")
                   else:
                       print (Cluster.rename_node(clusterid, oldname, newname))
            '''

        return ""
