from __future__ import print_function
from cmd3.console import Console
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.db.models import DEFAULT
from cloudmesh_client.db.models import dict_printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from pprint import pprint

class command_default(object):
    @classmethod
    def list(cls, output="table"):
        cm = CloudmeshDatabase()
        d= cm.all(DEFAULT)
        print (dict_printer(d, order=['cm_cloud','name','value'],output=output))


    @classmethod
    def set(cls, key, value, cloud):
        cm = CloudmeshDatabase()
        d = cm.dict(DEFAULT)
        cm.set_default(key, value, cloud)

    @classmethod
    def get(cls, key, cloud):
        cm = CloudmeshDatabase()
        d= cm.dict(DEFAULT)
        print(cm.get_default(key, cloud))
