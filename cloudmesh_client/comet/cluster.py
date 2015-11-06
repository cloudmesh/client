from __future__ import print_function

import json
import requests
from cloudmesh_base.hostlist import Parameter
from cloudmesh_client.shell.console import Console
from cloudmesh_client.comet.comet import Comet
from cloudmesh_client.common.Printer import dict_printer, list_printer
from cloudmesh_base.util import banner
from cloudmesh_base.hostlist import Parameter

from pprint import pprint


class Cluster(object):
    @staticmethod
    def simple_list(id=None, format="table"):

        if id is None:
            r = Comet.get(Comet.url("cluster/"))
        else:
            r = Comet.get(Comet.url("cluster/" + id + "/"))

        result = None
        if format == "rest":
            result = r
        else:
            entry = {}
            data = {}
            id = 0
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

            result = dict_printer(data,
                                  order=[
                                      'id',
                                      'cluster',
                                      'name',
                                      'type',
                                      'ip',
                                      'kind'],
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
            banner("Cluster List")

            print(list_printer(r,
                               output=format))

            for cluster in r:
                banner("Details: Client list of Cluster " + cluster["name"])

                clients = cluster["computes"]
                print(list_printer(clients,
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

        data = {"computes":[{"name":vm,"host":"comet-{:}".format(vm)} for vm in computeids],"cluster":"%s" % id}

        if on:
            print("Issuing request to poweron nodes...")
            posturl = url
            # print(data)

            r = Comet.post(posturl, data=data)
            print("RETURNED RESULTS:")
            print(r)
        else:
            print ("finding the computesetid of the specified nodes...")
            computesets = Comet.get_computeset()
            #banner ("computesets")
            #print (computesets)

            isValidSet = False
            computsetid = -1
            for computeset in computesets:
                if computeset["cluster"] == id and computeset["state"] == "started":
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
                print ("computesetid: {}".format(computesetid))
                puturl = "{:}{:}/poweroff".format(url, computesetid)

                r = Comet.put(puturl)
                print("RETURNED RESULTS:")
                print(r)
            else:
                print("All the nodes are not in the specified cluster, or they are not running")

    @staticmethod
    def delete():
        pass
