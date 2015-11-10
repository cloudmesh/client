from __future__ import print_function

from pprint import pprint

import requests
from cloudmesh_client.shell.console import Console
from cloudmesh_client.comet.comet import Comet
from cloudmesh_client.common.Printer import dict_printer, list_printer
from cloudmesh_base.util import banner
import hostlist


class Cluster(object):
    @staticmethod
    def simple_list(id=None, format="table"):

        if id is None:
            r = Comet.get(Comet.url("cluster/"))
        else:
            r = Comet.get(Comet.url("cluster/" + id + "/"))
            if r is None:
                Console.error("Could not find cluster `{}`"
                              .format(id))
                return ""
            r = [r]

        result = None
        if format == "rest":
            result = r
        else:
            entry = {}
            data = {}
            id = 0

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

            data = elements

            """
            for cluster in r:
                id += 1
                name = cluster['name']
                data[id] = {'id': id}
                for a in ['name', 'ip', 'frontend']:
                    data[id][a] = cluster[a]
                data[id]['kind'] = 'frontend'
                data[id]['type'] = 'frontend'
                data[id]['cluster'] = name

                for client in cluster['clients']:
                    id += 1
                    data[id] = client
                    data[id]['cluster'] = name
                    data[id]['id'] = id
                    data[id]['kind'] = 'client'
                    data[id]['frontend'] = cluster['name']
            """
            result = dict_printer(data,
                                  order=[
                                      "name",
                                      "project",
                                      "nodes",
                                      "computes",
                                      "frontend name",
                                      "frontend state",
                                      "frontend type",
                                      "frontend rocks_name",
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
                                      "Rocks name (Fe)",
                                      "Description",
                                  ],

                                  output=format)
            return result

    @staticmethod
    def list(id=None, format="table"):

        if id is None:
            r = Comet.get(Comet.url("cluster/"))
        else:
            r = Comet.get(Comet.url("cluster/" + id + "/"))

        if format == "rest":
            pprint(r)
        else:

            data = []

            empty = {
                'cluster': None,
                'cpus': None,
                'host': None,
                'ip': None,
                'memory': None,
                'name': None,
                'rocks_name': None,
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

            print(list_printer(data,
                               order=[
                                   "name",
                                   "state",
                                   "kind",
                                   "type"
                                   "ip",
                                   "rocks_name",
                                   "cpus",
                                   "cluster",
                                   "host",
                                   "memory",
                                   ],
                               output=format))

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
        r = requests.post(_url("cluster/{id}/start".format(**data)))
        print(r)

    @staticmethod
    def stop(id):
        data = {"id": id}
        r = requests.post(_url("cluster/{id}/stop".format(**data)))
        print(r)

    @staticmethod
    def power(id, computeids=None, on=True):

        print("power " + str(on))
        print(id)
        print(computeids)

        url = Comet.url("computeset/")

        vmhosts = {}

        data = {
            "computes": [{"name": vm, "host": "comet-{:}".format(vm)} for vm in
                         computeids], "cluster": "%s" % id}

        if on:
            print("Issuing request to poweron nodes...")
            posturl = url
            # print(data)

            r = Comet.post(posturl, data=data)
            print("RETURNED RESULTS:")
            print(r)
        else:
            print("finding the computesetid of the specified nodes...")
            computesets = Comet.get_computeset()
            # banner ("computesets")
            # print (computesets)

            isValidSet = False
            computsetid = -1
            for computeset in computesets:
                if computeset["cluster"] == id and computeset[
                    "state"] == "started":
                    computesetid = computeset["id"]
                    hosts = set()
                    for compute in computeset["computes"]:
                        hosts.add(compute["name"])
                    isValidSet = True
                    for computeid in computeids:
                        if computeid not in hosts:
                            isValidSet = False
                            break
            if isValidSet:
                print("Issuing request to poweroff nodes...")
                print("computesetid: {}".format(computesetid))
                puturl = "{:}{:}/poweroff".format(url, computesetid)

                r = Comet.put(puturl)
                print("RETURNED RESULTS:")
                print(r)
            else:
                print(
                    "All the nodes are not in the specified cluster, or they are not running")

    @staticmethod
    def delete():
        pass
