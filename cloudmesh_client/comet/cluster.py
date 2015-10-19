from __future__ import print_function

import json
import requests
from cloudmesh_base.hostlist import Parameter
from cloudmesh_client.shell.console import Console
from cloudmesh_client.comet.comet import Comet
from cloudmesh_client.common.tables import dict_printer, list_printer
from cloudmesh_base.util import banner

from pprint import pprint

class Cluster(object):

    @staticmethod
    def list(id=None):

        if id is None:
            r = Comet.get(Comet.url("cluster/"))
        else:
            r = Comet.get(Comet.url("cluster/" + id + "/"))

        banner("Cluster List")

        print (list_printer(r,
                            order=["name", "frontend", "ip"]))

        for cluster in r:
            banner("Details: Client list of Cluster " + cluster["name"])

            clients= cluster["clients"]
            print(list_printer(clients))


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
        print (r)

    @staticmethod
    def stop(id):
        data = {"id": id}
        r = requests.post(_url("cluster/{id}/stop".format(**data)))
        print (r)

    @staticmethod
    def power(clusterid, computeids=None,  on=True):
        print("power " + on)
        print(clusterid)
        print(computeids)

    @staticmethod
    def delete():
        pass

