# this is where the stack class is implemented

from __future__ import print_function

import requests

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.LibcloudDict import LibcloudDict
from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.default import Default

requests.packages.urllib3.disable_warnings()


class Stack(ListResource):

    cm = CloudmeshDatabase()


    @classmethod
    def refresh(cls, cloud):
        print ("TBD")

    @classmethod
    def list(cls,
             kind,
             cloud,
             user=None,
             tenant=None,
             order=None,
             header=None,
             output="table"):
        print ("TBD")

