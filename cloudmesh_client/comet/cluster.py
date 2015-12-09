from __future__ import print_function

import requests
from cloudmesh_client.shell.console import Console
from cloudmesh_client.comet.comet import Comet
from cloudmesh_client.common.Printer import dict_printer, list_printer
import hostlist
from cloudmesh_base.hostlist import Parameter


class Cluster(object):
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
            # TODO: BUG r is list
            if 'error' in r:
                Console.error("An error occurred: {error}".format(**r))
                raise ValueError("COMET Error")
            elif 'error' in r[0]:
                Console.error("An error occurred: {error}".format(**r[0]))
                raise ValueError("COMET Error")

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
    def power(clusterid, subject, param=None, action=None):

        # print("SUBJECT to perform action on: {}".format(subject))
        # print("\ton cluster: {}".format(clusterid))
        # print("\tAction: {}".format(action))
        # print("\tParameter: {}".format(param))

        # the API is now accepting hostlist format directly
        # computeIdsHostlist = hostlist.collect_hostlist(computeids)
        # print (computeIdsHostlist)
        if 'HOSTS' == subject:
            url = Comet.url("computeset/")

            # data = {
            #    "computes": [{"name": vm, "host": "comet-{:}".format(vm)} for vm in
            #                 computeids], "cluster": "%s" % id}
            data = {"computes": "%s" % param, "cluster": "%s" % clusterid}
            # print (data)
            if "on" == action:
                # print("Issuing request to poweron nodes...")
                posturl = url
                # print (data)

                r = Comet.post(posturl, data=data)
                # print("RETURNED RESULTS:")
                # print (r)
                if 'cluster' in r:
                    if 'state' in r and 'queued' == r['state']:
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
                    ret = "An internal error occured. " \
                          "Please submit a ticket with following info:\n {}\n" \
                        .format(r)
                print(ret)
            elif action in ["off", "reboot", "reset", "shutdown"]:
                if action in ["off"]:
                    action = "power{}".format(action)
                # print("finding the computesetid of the specified nodes...")
                computesets = Comet.get_computeset()
                # print ("computesets")
                # pprint (computesets)

                is_valid_set = False
                # computesetid = -1
                for computeset in computesets:
                    if computeset["cluster"] == clusterid \
                            and computeset["state"] == "started":
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
                    # a cluster could have multiple 'started' set
                    if is_valid_set:
                        break
                if is_valid_set:
                    # print("Issuing request to poweroff nodes...")
                    # print("computesetid: {}".format(computesetid))
                    puturl = "{:}{:}/{}".format(url, computesetid, action)
                    # print (puturl)
                    r = Comet.put(puturl)
                    # print("RETURNED RESULTS:")
                    # print(r)
                    if r is not None:
                        if '' != r.strip():
                            print(r)
                        else:
                            print("Requeset Accepted. In the process of {} the nodes"
                                  .format(action))
                    else:
                        print("Unknown error: POWER, HOSTS")
                else:
                    print(
                        "All the nodes are not in the specified cluster, "
                        "or they are not running")
            else:
                print("Action not supported! Try these: on/off/reboot/reset/shutdown")
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
                        print(r)
                    else:
                        print("Requeset Accepted. In the process of {} the front end"
                              .format(action))
                else:
                    print("Problem executing the request. "
                          "Check if the cluster exists")
            else:
                print("Action not supported! Try these: on/off/reboot/reset/shutdown")
        elif 'COMPUTESET' == subject:
            url = Comet.url("computeset/")
            if 'on' == action:
                print("NOT SUPPORTED! Use hostslist to specify the hosts to power on!")
            elif action in ["off", "reboot", "reset", "shutdown"]:
                if action in ["off"]:
                    action = "power{}".format(action)
                puturl = "{:}{:}/{}".format(url, param, action)
                # print (puturl)
                r = Comet.put(puturl)
                if r is not None:
                    if '' != r.strip():
                        print(r)
                    else:
                        print("Requeset Accepted. In the process of {} the computeset"
                              .format(action))
                else:
                    print("Problem executing the request. "
                          "Check if the computeset exists")
            else:
                print("Action not supported! Try these: on/off/reboot/reset/shutdown")
        elif 'HOST' == subject:
            url = Comet.url("cluster/{}/compute/{}/".format(clusterid, param))
            if action in ["on", "off", "reboot", "reset", "shutdown"]:
                if action in ["on", "off"]:
                    action = "power{}".format(action)
                puturl = "{}{}".format(url, action)
                # print (puturl)
                r = Comet.put(puturl)
                if r is not None:
                    if '' != r.strip():
                        print(r)
                    else:
                        print("Requeset Accepted. In the process of {} the host"
                              .format(action))
                else:
                    print("Problem executing the request. "
                          "Check if the node belongs to the cluster")
            else:
                print("Action not supported! Try these: on/off/reboot/reset/shutdown")

    @staticmethod
    def delete():
        pass
