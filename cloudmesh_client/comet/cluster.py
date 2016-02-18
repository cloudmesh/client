from __future__ import print_function

import requests
import hostlist

from cloudmesh_client.shell.console import Console
from cloudmesh_client.comet.comet import Comet
from cloudmesh_client.common.Printer import dict_printer, list_printer

from cloudmesh_client.common.hostlist import Parameter


class Cluster(object):
    WALLTIME_MINS = 120
    N_ALLOCATIONS_PER_LINE = 5
    MINS_PER_UNIT = {"m": 1, "h": 60, "d": 1440, "w": 10080}

    @staticmethod
    def simple_list(id=None, format="table"):
        result = ""
        if id is None:
            r = Comet.get(Comet.url("cluster/"))
        else:
            r = Comet.get(Comet.url("cluster/" + id + "/"))
            if r is None:
                Console.error("Could not find cluster `{}`"
                              .format(id))
                return result
            r = [r]

        if r is not None:
            if 'error' in r:
                Console.error("An error occurred: {error}".format(**r))
                raise ValueError("COMET Error")
            elif 'error' in r[0]:
                Console.error("An error occurred: {error}".format(**r[0]))
                raise ValueError("COMET Error")

            if format == "rest":
                result = r
            else:
                elements = {}
                for cluster in r:
                    element = {}
                    for attribute in ["project", "name", "description"]:
                        element[attribute] = cluster[attribute]
                        element["nodes"] = len(cluster["computes"])
                    for attribute in cluster["frontend"].keys():
                        element["frontend " + attribute] = cluster["frontend"][
                            attribute]
                    names = []
                    for compute in cluster["computes"]:
                        names.append(compute["name"])

                    element["computes"] = hostlist.collect_hostlist(names)

                    elements[cluster["name"]] = element

                result = dict_printer(elements,
                                      order=[
                                          "name",
                                          "project",
                                          "nodes",
                                          "computes",
                                          "frontend name",
                                          "frontend state",
                                          "frontend type",
                                          "description",
                                      ],
                                      header=[
                                          "Name",
                                          "Project",
                                          "Count",
                                          "Nodes",
                                          "Frontend (Fe)",
                                          "State (Fe)",
                                          "Type (Fe)",
                                          "Description",
                                      ],

                                      output=format)
            return result

    @staticmethod
    def list(id=None, format="table"):

        def check_for_error(r):
            if r is not None:
                if 'error' in r:
                    Console.error("An error occurred: {error}".format(**r))
                    raise ValueError("COMET Error")

        result = ""
        if id is None:
            r = Comet.get(Comet.url("cluster/"))
            check_for_error(r)
        else:
            r = Comet.get(Comet.url("cluster/" + id + "/"))
            check_for_error(r)
            if r is None:
                Console.error("Could not find cluster `{}`"
                              .format(id))
                return result
            r = [r]

        if r is not None:
            if format == "rest":
                result = r
            else:

                data = []

                empty = {
                    'cluster': None,
                    'cpus': None,
                    'host': None,
                    "mac": None,
                    'ip': None,
                    'memory': None,
                    'name': None,
                    'state': None,
                    'type': None,
                    'kind': 'frontend'
                }

                for cluster in r:

                    clients = cluster["computes"]
                    for client in clients:
                        client["kind"] = "compute"
                    frontend = dict(empty)
                    frontend.update(cluster["frontend"])
                    data += [frontend]
                    data += clients

                for anode in data:
                    for attribute in anode.keys():
                        if "interface" == attribute:
                            macs = []
                            ips = []
                            for ipaddr in anode["interface"]:
                                macs.append(ipaddr["mac"])
                                ips.append(ipaddr["ip"] or "N/A")
                            anode["mac"] = "; ".join(macs)
                            anode["ip"] = "; ".join(ips)
                    del anode["interface"]

                result = list_printer(data,
                                      order=[
                                          "name",
                                          "state",
                                          "kind",
                                          "type",
                                          "mac",
                                          "ip",
                                          "cpus",
                                          "cluster",
                                          "memory",
                                      ],
                                      output=format)
            return result

    @staticmethod
    def display_get_allocation(allocations):
        allocation = None
        allocations_sorted = sorted(allocations)
        i = 1
        while i < len(allocations_sorted) + 1:
            for j in range(0, Cluster.N_ALLOCATIONS_PER_LINE):
                if i < len(allocations_sorted) + 1:
                    print ("{}: {}".format(i, allocations_sorted[i - 1]),
                           end="\t")
                    i += 1
            print ("")
        print ("")
        chosen_alloc = -1
        while chosen_alloc < 0:
            allocation_input = raw_input("Pick an allocation by specifying its index: ")
            try:
                chosen_alloc = int(allocation_input)
                if 0 < chosen_alloc < len(allocations_sorted) + 1:
                    allocation = allocations_sorted[chosen_alloc - 1]
                else:
                    chosen_alloc = -1
                    print ("Invalid index specified. "
                           "Please choose between 1 and {}"
                           .format(len(allocations_sorted))
                           )
            except:
                if allocation_input in allocations_sorted:
                    chosen_alloc = 0
                    allocation = allocation_input
        return allocation

    @staticmethod
    def info():
        Console.error("comet cluster info: to be implemented")
        pass

    @staticmethod
    def add():
        pass

    @staticmethod
    def start(id):
        data = {"id": id}
        r = requests.post(Comet.url("cluster/{id}/start".format(**data)))
        print(r)

    @staticmethod
    def stop(id):
        data = {"id": id}
        r = requests.post(Comet.url("cluster/{id}/stop".format(**data)))
        print(r)

    @staticmethod
    def computeset(id=None):
        computesets = Comet.get_computeset(id)
        if computesets is not None:
            if 'cluster' in computesets:
                result = Cluster.output_computeset(computesets)
            else:
                result = ''
                for acomputeset in computesets:
                    result += Cluster.output_computeset(acomputeset)
        else:
            result = "No computeset exists with the specified ID"
        return result

    @staticmethod
    def output_computeset(computesetdict):
        result = ""
        if computesetdict["state"] not in ["completed"]:
            result += "\nCluster: {}\tComputesetID: {}\t State: {}\n" \
                .format(computesetdict["cluster"],
                        computesetdict["id"],
                        computesetdict["state"]
                        )
            data = computesetdict["computes"]
            for anode in data:
                for attribute in anode.keys():
                    if "interface" == attribute:
                        macs = []
                        ips = []
                        for ipaddr in anode["interface"]:
                            macs.append(ipaddr["mac"])
                            ips.append(ipaddr["ip"] or "N/A")
                        anode["mac"] = "; ".join(macs)
                        anode["ip"] = "; ".join(ips)
                del anode["interface"]
            result += str(list_printer(data,
                                       order=[
                                           "name",
                                           "state",
                                           "type",
                                           "mac",
                                           "ip",
                                           "cpus",
                                           "cluster",
                                           "host",
                                           "memory",
                                       ],
                                       output="table"))
        return result

    @staticmethod
    def convert_to_mins(s):
        mins = None
        if s is not None:
            s = s.lower()
            if s[-1] in Cluster.MINS_PER_UNIT.keys():
                mins = int(s[:-1]) * Cluster.MINS_PER_UNIT[s[-1]]
        return mins

    @staticmethod
    def power(clusterid, subject, param=None, action=None,
              allocation=None, walltime=None, numnodes=None):

        # print("SUBJECT to perform action on: {}".format(subject))
        # print("\ton cluster: {}".format(clusterid))
        # print("\tAction: {}".format(action))
        # print("\tParameter: {}".format(param))
        # print("\tAllocation: {}".format(allocation))
        # print("\tWalltime: {}".format(walltime))

        # the API is now accepting hostlist format directly
        # computeIdsHostlist = hostlist.collect_hostlist(computeids)
        # print (computeIdsHostlist)
        ret = ''

        #
        # Now it accepts
        # {"cluster":"vc3","computes":"compute[1-2]"},
        # {"cluster":"vc3","computes":["compute1","compute2"]} and
        # {"cluster":"vc3","count":2}
        #
        if subject in ['HOSTS', 'HOST']:
            # power on N arbitrary nodes
            if numnodes:
                if "on" == action:
                    if not allocation:
                        cluster = Cluster.list(clusterid, format='rest')
                        # use the first one if no provided
                        allocation = cluster[0]['allocations'][0]
                    if not walltime:
                        walltime = Cluster.WALLTIME_MINS

                    posturl = Comet.url("computeset/")
                    data = {"cluster":"%s" % clusterid, "count": "%s" % numnodes}

                    r = Comet.post(posturl, data=data)
                    # print("RETURNED RESULTS:")
                    # print (r)
                    if 'cluster' in r:
                        if 'state' in r and \
                           ('queued' == r['state'] or 'submitted' == r['state']):
                            computesetid = r['id']
                            ret = 'Request accepted! Check status with:\n' \
                                  'comet cluster {}\n'.format(clusterid) + \
                                  'or:\n' \
                                  'comet computeset {}\n'.format(computesetid)
                        else:
                            # in case of some internal problem
                            ret = ''
                    elif 'error' in r:
                        ret = "An error occurred: {}".format(r['error'])
                    else:
                        ret = "An internal error occured. "\
                              "Please submit a ticket with the "\
                              "following info:\n {}\n"\
                              .format(r)
                # cannot power off or reboot N arbitrary nodes
                else:
                    ret = "Action NOT SUPPORTED! Try with explicit "\
                          "node name(s) or computeset id"
            # parse based on NODEPARAM parameter
            # could be computeset id; front end; or hostlist named compute nodes
            else:
                hosts_param = hostlist.expand_hostlist(param)
                hosts_param_set = set(hosts_param)
                nodes_free = True
                nodes_allocated = False
                nodes_checked = False
                # computesetid = -1
                computesets = Comet.get_computeset()
                for computeset in computesets:
                    if computeset["cluster"] == clusterid \
                            and (computeset["state"] == "started" or
                                 computeset["state"] == "running"):
                        computesetid = computeset["id"]
                        # print (computesetid)
                        hosts = set()
                        for compute in computeset["computes"]:
                            hosts.add(compute["name"])
                        # print (hosts)
                        if hosts_param_set <= hosts:
                            nodes_allocated = True
                            nodes_free = False
                            nodes_checked = True
                        # at least one specified host not in any Active computeset
                        else:
                            for host in hosts_param:
                                # some specified nodes are in Active computeset
                                if host in hosts:
                                    nodes_free = False
                                    nodes_checked = True
                                    break
                    # a cluster could have multiple 'started' set
                    if nodes_checked:
                        break
                # print ("nodes_checked: %s" % nodes_checked)
                # print ("nodes_allocated: %s" % nodes_allocated)
                # print ("nodes_free: %s" % nodes_free)
                if not (nodes_free or nodes_allocated):
                    ret = "Error: Some nodes are already in active computesets"
                else:
                    if "on" == action:
                        if not allocation:
                            cluster = Cluster.list(clusterid, format='rest')
                            # use the first one if no provided
                            allocation = cluster[0]['allocations'][0]
                        if not walltime:
                            walltime = Cluster.WALLTIME_MINS

                        data = {"computes": "%s" % param,
                                "cluster": "%s" % clusterid,
                                "walltime_mins": "%s" % walltime,
                                "allocation": "%s" % allocation}

                        if nodes_free:
                            # print("Issuing request to poweron nodes...")
                            url = Comet.url("computeset/")
                            posturl = url
                            # print (data)

                            r = Comet.post(posturl, data=data)
                            # print("RETURNED RESULTS:")
                            # print (r)
                            if 'cluster' in r:
                                if 'state' in r and \
                                   ('queued' == r['state'] or 'submitted' == r['state']):
                                    computesetid = r['id']
                                    ret = 'Request accepted! Check status with:\n' \
                                          'comet cluster {}\n'.format(clusterid) + \
                                          'or:\n' \
                                          'comet computeset {}\n'.format(computesetid)
                                else:
                                    # in case of some internal problem
                                    ret = ''
                            elif 'error' in r:
                                ret = "An error occurred: {}".format(r['error'])
                            else:
                                ret = "An internal error occured. "\
                                      "Please submit a ticket with the "\
                                      "following info:\n {}\n"\
                                      .format(r)
                        elif nodes_allocated:
                            ret = ""
                            for host in hosts_param:
                                url = Comet.url("cluster/{}/compute/{}/"
                                                .format(clusterid, host))
                                action = "poweron"
                                puturl = "{}{}".format(url, action)
                                # print (puturl)
                                r = Comet.put(puturl)
                                if r is not None:
                                    if '' != r.strip():
                                        ret += r
                                    else:
                                        ret += "Requeset Accepted. "\
                                               "In the process of power on node {}\n"\
                                               .format(host)
                                else:
                                    ret += "Problem executing the request. "\
                                        "Check if the node {} belongs to the cluster"\
                                        .format(host)
                        # print(ret)
                    elif action in ["off", "reboot", "reset", "shutdown"]:
                        if action in ["off"]:
                            action = "power{}".format(action)
                        if nodes_allocated:
                            ret = ""
                            for host in hosts_param:
                                url = Comet.url("cluster/{}/compute/{}/"
                                                .format(clusterid, host))
                                puturl = "{}{}".format(url, action)
                                # print (puturl)
                                r = Comet.put(puturl)
                                if r is not None:
                                    if '' != r.strip():
                                        ret = r
                                    else:
                                        ret += "Requeset Accepted. "\
                                            "In the process of {} node {}\n"\
                                            .format(action, host)
                                else:
                                    ret += "Problem executing the request. "\
                                        "Check if the node {} belongs to the cluster"\
                                        .format(host)
                        elif nodes_free:
                            ret = "Error: The specified nodes are "\
                                  "not in active computesets"
                    else:
                        ret = "Action not supported! Try these: "\
                              "on/off/reboot/reset/shutdown"
        elif 'FE' == subject:
            url = Comet.url("cluster/{}/frontend/".format(clusterid))
            if action in ["on", "off", "reboot", "reset", "shutdown"]:
                if action in ["on", "off"]:
                    action = "power{}".format(action)
                puturl = "{}{}".format(url, action)
                # print (puturl)
                r = Comet.put(puturl)
                if r is not None:
                    if '' != r.strip():
                        ret = r
                    else:
                        ret = "Requeset Accepted. "\
                              "In the process of {} the front-end node".format(action)
                else:
                    ret = "Problem executing the request. "\
                          "Check if the cluster exists"
            else:
                ret = "Action not supported! Try these: on/off/reboot/reset/shutdown"
        elif 'COMPUTESET' == subject:
            url = Comet.url("computeset/")
            if 'on' == action:
                ret = "NOT SUPPORTED! Use hostslist to specify the hosts to power on!"
            elif action in ["off", "reboot", "reset", "shutdown"]:
                if action in ["off"]:
                    action = "power{}".format(action)
                puturl = "{:}{:}/{}".format(url, param, action)
                # print (puturl)
                r = Comet.put(puturl)
                if r is not None:
                    if '' != r.strip():
                        ret = r
                    else:
                        ret = "Requeset Accepted. "\
                              "In the process of {} the nodes".format(action)
                else:
                    ret = "Problem executing the request. "\
                          "Check if the computeset exists"
            else:
                ret = "Action not supported! Try these: on/off/reboot/reset/shutdown"
        '''
        elif 'HOST' == subject:
            computesets = Comet.get_computeset()
            pprint (computesets)
            for computeset in computesets:
                if computeset["cluster"] == clusterid \
                        and (computeset["state"] == "started" \
                             or computeset["state"] == "running"):
                    computesetid = computeset["id"]
                    # print (computesetid)
                    hosts = set()
                    for compute in computeset["computes"]:
                        hosts.add(compute["name"])
                    # print (hosts)
                    is_valid_set = True
                    hostsparam = Parameter.expand(param)
                    for host in hostsparam:
                        if host not in hosts:
                            is_valid_set = False
                            break 
            url = Comet.url("cluster/{}/compute/{}/".format(clusterid, param))
            if action in ["on", "off", "reboot", "reset", "shutdown"]:
                if action in ["on", "off"]:
                    action = "power{}".format(action)
                puturl = "{}{}".format(url, action)
                # print (puturl)
                r = Comet.put(puturl)
                if r is not None:
                    if '' != r.strip():
                        ret = r
                    else:
                        ret = "Requeset Accepted. "\
                              "In the process of {} the nodes".format(action)
                else:
                    ret = "Problem executing the request. "\
                          "Check if the node belongs to the cluster"
            else:
                ret = "Action not supported! Try these: on/off/reboot/reset/shutdown"
        '''
        # """
        return ret

    @staticmethod
    def detach_iso(clusterid, nodeids=None, action='Detaching'):
        return Cluster.attach_iso('', clusterid, nodeids, action='Detaching')

    @staticmethod
    def attach_iso(isoname, clusterid, nodeids=None, action='Attaching'):
        ret = ''
        # print ("Attaching ISO image")
        # print ("isoname: %s" % isoname)
        #print ("cluster: %s" % clusterid)
        # print ("node: %s" % nodeid)

        if isoname != '':
            isoname = "public/{}".format(isoname)

        urls = {}
        # attaching to compute node
        if nodeids:
            nodeids = hostlist.expand_hostlist(nodeids)
            for nodeid in nodeids:
                url = Comet.url("cluster/{}/compute/{}/attach_iso?iso_name={}")\
                                .format(clusterid, nodeid, isoname)
                urls["Node {}".format(nodeid)] = url
        else:
            # attaching to fronend node
            url = Comet.url("cluster/{}/frontend/attach_iso?iso_name={}")\
                            .format(clusterid, isoname)
            urls['Frontend'] = url
        #data = {"iso_name": "%s" % isoname}
        # print ("url: %s" % url)
        #print ("data: %s" % data)
        tofrom = {}
        tofrom['Attaching'] = 'to'
        tofrom['Detaching'] = 'from'
        for node, url in urls.iteritems():
            r = Comet.put(url)
            # print (r)
            if r is not None:
                if '' != r.strip():
                    ret += r
                else:
                    ret += "Requeset Accepted. {} the image {} {} of cluster {}\n"\
                            .format(action, tofrom[action], node, clusterid)
            else:
                ret += "Something wrong during {} the image {} {} of cluster {}!"\
                       "Please check the command and try again\n"\
                       .format(action, tofrom[action], node, clusterid)
        return ret

    @staticmethod
    def rename_node(clusterid, old_compute_name, new_compute_name):
        url = Comet.url("cluster/{}/compute/{}/rename"\
                        .format(clusterid, old_compute_name))
        data = {"name":"%s" % new_compute_name}
        ret = ""
        r = Comet.post(url, data=data)
        print (r)
        if r is not None:
            if '' != r.strip():
                ret = r
            else:
                ret = "Requeset Accepted."
        return ret

    @staticmethod
    def delete():
        pass
