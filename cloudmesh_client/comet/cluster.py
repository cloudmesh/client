from __future__ import print_function

import requests
from cloudmesh_base.hostlist import Parameter
from cloudmesh_client.shell.console import Console

rest_version = "v1"
base_url = "http://127.0.0.1:8000/" + rest_version + "/"


def _url(endpoint):
    return base_url + endpoint

class Cluster(object):

    @staticmethod
    def list(id=None):

        if id is None:
            r = requests.get(_url("cluster"))
        else:
            r = requests.get(_url("cluster/" + id))
        print(r.status_code)
        print(r.text)

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
        print (r.text)

    @staticmethod
    def stop(id):
        data = {"id": id}
        r = requests.post(_url("cluster/{id}/stop".format(**data)))
        print (r.text)

    @staticmethod
    def power(clusterid, computeids=None,  on=True):
        print("power " + on)
        print(clusterid)
        print(computeids)

    @staticmethod
    def delete():
        pass

