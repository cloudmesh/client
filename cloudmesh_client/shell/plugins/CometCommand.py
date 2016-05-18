from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command, PluginCommand, CometPluginCommand
from cloudmesh_client.comet.comet import Comet
from cloudmesh_client.comet.cluster import Cluster
from cloudmesh_client.common.hostlist import Parameter
from cloudmesh_client.common.ConfigDict import ConfigDict
import hostlist
import os
import sys
from builtins import input
from pprint import pprint

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
               comet init
               comet ll [CLUSTERID] [--format=FORMAT]
               comet cluster [CLUSTERID]
                             [--format=FORMAT]
                             [--sort=SORTKEY]
               comet computeset [COMPUTESETID]
                            [--allocation=ALLOCATION]
                            [--cluster=CLUSTERID]
                            [--state=COMPUTESESTATE]
               comet start CLUSTERID [--count=NUMNODES] [COMPUTENODEIDS]
                            [--allocation=ALLOCATION]
                            [--walltime=WALLTIME]
               comet terminate COMPUTESETID
               comet power (on|off|reboot|reset|shutdown) CLUSTERID [NODESPARAM]
               comet console CLUSTERID [COMPUTENODEID]
               comet node info CLUSTERID [COMPUTENODEID] [--format=FORMAT]
               comet node rename CLUSTERID OLDNAMES NEWNAMES
               comet iso list
               comet iso upload [--isoname=ISONAME] PATHISOFILE
               comet iso attach ISONAME CLUSTERID [COMPUTENODEIDS]
               comet iso detach CLUSTERID [COMPUTENODEIDS]

            Options:
                --format=FORMAT         Format is either table, json, yaml,
                                        csv, rest
                                        [default: table]
                --sort=SORTKEY          Sorting key for the table view
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
                --isoname=ISONAME       Name of the iso image after being stored remotely.
                                        If not specified, use the original filename
                --state=COMPUTESESTATE  List only computeset with the specified state.
                                        The state could be submitted, running, completed

            Arguments:
                CLUSTERID       The assigned name of a cluster, e.g. vc1
                COMPUTESETID    An integer identifier assigned to a computeset
                COMPUTENODEID   A compute node name, e.g., vm-vc1-0
                                If not provided, the requested action will be taken
                                on the frontend node of the specified cluster
                COMPUTENODEIDS  A set of compute node names in hostlist format,
                                e.g., vm-vc1-[0-3]
                                One single node is also acceptable: vm-vc1-0
                                If not provided, the requested action will be taken
                                on the frontend node of the specified cluster
                NODESPARAM      Specifying the node/nodes/computeset to act on.
                                In case of integer, will be intepreted as a computesetid;
                                in case of a hostlist format, e.g., vm-vc1-[0-3], a group
                                of nodes; or a single host is also acceptable,
                                e.g., vm-vc1-0
                ISONAME         Name of an iso image at remote server
                PATHISOFILE     The full path to the iso image file to be uploaded
                OLDNAMES        The list of current node names to be renamed, in hostlist
                                format. A single host is also acceptable.
                NEWNAMES        The list of new names to rename to, in hostlist format.
                                A single host is also acceptable.
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
        if arguments["init"]:
            print ("Initializing the comet configuration file...")
            config = ConfigDict("cloudmesh.yaml")
            # for unit testing only.
            cometConf = config["cloudmesh.comet"]
            endpoints = []
            # print (cometConf.keys())
            if "endpoints" in cometConf.keys():
                endpoints = cometConf["endpoints"].keys()
                if len(endpoints) < 1:
                    Console.error("No service endpoints available."\
                                  " Please check the config template")
                    return ""
            if "username" in cometConf.keys():
                default_username = cometConf['username']
                # print (default_username)
                if 'TBD' == default_username:
                    set_default_user = \
                        input("Set a default username (RETURN to skip): ")
                    if set_default_user:
                        config.data["cloudmesh"]["comet"]["username"] = \
                            set_default_user
                        config.save()
                        Console.ok("Comet default username set!")
            if "active" in cometConf.keys():
                active_endpoint = cometConf['active']
                set_active_endpoint = \
                    input("Set the active service endpoint to use. "
                          "The availalbe endpoints are - %s [%s]: "
                          % ("/".join(endpoints),
                             active_endpoint)
                          )
                if set_active_endpoint:
                    if set_active_endpoint in endpoints:
                        config.data["cloudmesh"]["comet"]["active"] = \
                            set_active_endpoint
                        config.save()
                        Console.ok("Comet active service endpoint set!")
                    else:
                        Console.error("The provided endpoint does not match any "
                                      "available service endpoints. Try %s"
                                      % "/".join(endpoints))

            if cometConf['active'] in endpoints:
                endpoint_url = cometConf["endpoints"] \
                    [cometConf['active']]["nucleus_base_url"]
                api_version = cometConf["endpoints"] \
                    [cometConf['active']]["api_version"]
                set_endpoint_url = \
                    input("Set the base url for the nucleus %s service [%s]: " \
                          % (cometConf['active'],
                             endpoint_url)
                          )
                if set_endpoint_url:
                    if set_endpoint_url != endpoint_url:
                        config.data["cloudmesh"]["comet"]["endpoints"] \
                            [cometConf['active']]["nucleus_base_url"] \
                            = set_endpoint_url
                        config.save()
                        Console.ok("Service base url set!")

                set_api_version = \
                    input("Set the api version for the nucleus %s service [%s]: " \
                          % (cometConf['active'],
                             api_version)
                          )
                if set_api_version:
                    if set_api_version != api_version:
                        config.data["cloudmesh"]["comet"]["endpoints"] \
                            [cometConf['active']]["api_version"] \
                            = set_api_version
                        config.save()
                        Console.ok("Service api version set!")
                print("Authenticating to the nucleus %s " \
                      "service and obtaining the apikey..." \
                      % cometConf['active'])
                Comet.get_apikey(cometConf['active'])

            return ''
            # Comet.get_apikey()
        try:
            logon = Comet.logon()
            if logon is False:
                Console.error("Could not logon. Please try first:\ncm comet init")
                return ""
        except:
            Console.error("Could not logon")

        output_format = arguments["--format"] or "table"

        if arguments["ll"]:
            cluster_id = arguments["CLUSTERID"] or None

            print(Cluster.simple_list(cluster_id, format=output_format))

        elif arguments["cluster"]:

            cluster_id = arguments["CLUSTERID"]
            sortkey = arguments["--sort"]
            print(Cluster.list(cluster_id, format=output_format, sort=sortkey))

        elif arguments["computeset"]:
            computeset_id = arguments["COMPUTESETID"] or None
            cluster = arguments["--cluster"] or None
            state = arguments["--state"] or None
            allocation = arguments["--allocation"] or None
            cluster = arguments["--cluster"] or None
            print (Cluster.computeset(computeset_id, cluster, state, allocation))
        elif arguments["start"]:
            clusterid = arguments["CLUSTERID"]
            numnodes = arguments["--count"] or None
            computenodeids = arguments["COMPUTENODEIDS"] or None

            # check allocation information for the cluster
            cluster = Cluster.list(clusterid, format='rest')
            try:
                allocations = cluster[0]['allocations']
            except:
                # print (cluster)
                Console.error("No allocation available for the specified cluster."\
                              "Please check with the comet help team")
                return ""

            # checking whether the computesetids is in valid hostlist format
            if computenodeids:
                try:
                    hosts_param = hostlist.expand_hostlist(computenodeids)
                except hostlist.BadHostlist:
                    Console.error("Invalid hosts list specified!",
                                  traceflag=False)
                    return ""
            elif numnodes:
                try:
                    param = int(numnodes)
                except ValueError:
                    Console.error("Invalid count value specified!", traceflag=False)
                    return ""
                if param <= 0:
                    Console.error("count value has to be greather than zero")
                    return ""
                numnodes = param
            else:
                Console.error("You have to specify either the count of nodes, " \
                              "or the names of nodes in hostlist format")
                return ""

            walltime = arguments["--walltime"] or None
            allocation = arguments["--allocation"] or None

            # validating walltime and allocation parameters
            walltime = Cluster.convert_to_mins(walltime)
            if not walltime:
                print("No valid walltime specified. " \
                      "Using system default (2 days)")
            if not allocation:
                if len(allocations) == 1:
                    allocation = allocations[0]
                else:
                    allocation = Cluster.display_get_allocation(allocations)

            # issuing call to start a computeset with specified parameters
            print(Cluster.computeset_start(clusterid,
                                           computenodeids,
                                           numnodes,
                                           allocation,
                                           walltime)
                  )
        elif arguments["terminate"]:
            computesetid = arguments["COMPUTESETID"]
            print(Cluster.computeset_terminate(computesetid))
        elif arguments["power"]:
            clusterid = arguments["CLUSTERID"] or None
            fuzzyparam = arguments["NODESPARAM"] or None

            # parsing nodesparam for proper action
            if fuzzyparam:
                try:
                    param = int(fuzzyparam)
                    subject = 'COMPUTESET'
                except ValueError:
                    param = fuzzyparam
                    try:
                        hosts_param = hostlist.expand_hostlist(fuzzyparam)
                        subject = 'HOSTS'
                    except hostlist.BadHostlist:
                        Console.error("Invalid hosts list specified!",
                                      traceflag=False)
                        return ""
            else:
                subject = 'FE'
                param = None

            if arguments["on"]:
                action = "on"
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
                                action)
                  )
        elif arguments["console"]:
            clusterid = arguments["CLUSTERID"]
            nodeid = None
            if 'COMPUTENODEID' in arguments:
                nodeid = arguments["COMPUTENODEID"]
            Comet.console(clusterid, nodeid)
        elif arguments["iso"]:
            if arguments["list"]:
                isos = (Comet.list_iso())
                idx = 0
                for iso in isos:
                    if iso.startswith("public/"):
                        iso = iso.split("/")[1]
                    idx += 1
                    print ("{}: {}".format(idx, iso))
            if arguments["upload"]:
                isofile = arguments["PATHISOFILE"]
                isofile = os.path.abspath(isofile)
                if os.path.isfile(isofile):
                    if arguments["--isoname"]:
                        filename = arguments["--isoname"]
                    else:
                        filename = os.path.basename(isofile)
                else:
                    print ("File does not exist - {}" \
                          .format(arguments["PATHISOFILE"]))
                    return ""
                print(Comet.upload_iso(filename, isofile))
            elif arguments["attach"]:
                isoname = arguments["ISONAME"]
                clusterid = arguments["CLUSTERID"]
                computenodeids = arguments["COMPUTENODEIDS"] or None
                print(Cluster.attach_iso(isoname, clusterid, computenodeids))
            elif arguments["detach"]:
                clusterid = arguments["CLUSTERID"]
                computenodeids = arguments["COMPUTENODEIDS"] or None
                print(Cluster.detach_iso(clusterid, computenodeids))
        elif arguments["node"]:
            if arguments["info"]:
                clusterid = arguments["CLUSTERID"]
                nodeid = arguments["COMPUTENODEID"]
                print (Cluster.node_info(clusterid, nodeid=nodeid, format=output_format))
            elif arguments["rename"]:
                clusterid = arguments["CLUSTERID"]
                oldnames = Parameter.expand(arguments["OLDNAMES"])
                newnames = Parameter.expand(arguments["NEWNAMES"])
                if len(oldnames) != len(newnames):
                    Console.error("Length of OLDNAMES and NEWNAMES have to be the same",
                                  traceflag=False)
                    return ""
                else:
                    for newname in newnames:
                        if newname.strip() == "":
                            Console.error("Newname cannot be empty string",
                                          traceflag=False)
                            return ""
                    cluster_data = Cluster.list(clusterid, format="rest")
                    if len(cluster_data) > 0:
                        computes = cluster_data[0]["computes"]
                        nodenames = [x["name"] for x in computes]
                    else:
                        Console.error("Error obtaining the cluster information",
                                      traceflag=False)
                        return ""
                    # check if new names ar not already taken
                    # to be implemented
                    # print (oldnames)
                    # print (newnames)
                    # print (nodenames)
                    oldset = set(oldnames)
                    newset = set(newnames)
                    currentset = set(nodenames)
                    # at least one OLDNAME does not exist
                    if  not oldset <= currentset:
                        Console.error("Not all OLDNAMES are valid", traceflag=False)
                        return ""
                    else:
                        # those unchanged nodes
                        keptset = currentset - oldset
                        # duplication between name of unchanged nodes and
                        # the requested NEWNAMES
                        if keptset & newset != set():
                            Console.error("Not proceeding as otherwise introducing "\
                                          "duplicated names",
                                          traceflag=False)
                        else:
                            for i in range(0,len(oldnames)):
                                oldname = oldnames[i]
                                newname = newnames[i]
                                print ("%s -> %s" % (oldname, newname))
                            confirm = input("Confirm batch renaming (Y/y to confirm, "\
                                            "any other key to abort):")
                            if confirm.lower() == 'y':
                                print ("Conducting batch renaming")
                                for i in range(0,len(oldnames)):
                                    oldname = oldnames[i]
                                    newname = newnames[i]
                                    print (Cluster.rename_node(clusterid,
                                                               oldname,
                                                               newname))
                            else:
                                print ("Action aborted!")

        return ""
