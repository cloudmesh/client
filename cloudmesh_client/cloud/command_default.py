from __future__ import print_function
from cmd3.console import Console
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.db.models import DEFAULT
from cloudmesh_client.db.models import dict_printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from pprint import pprint


class command_default(object):
    
    @classmethod
    def list(cls, format="table"):
        cm = CloudmeshDatabase()
        d = cm.all(DEFAULT)
        return(dict_printer(d, order=['cm_user',
                                      'cm_cloud',
                                      'name',
                                      'value'], output=format))

    @classmethod
    def set(cls, key, value, cloud):
        cm = CloudmeshDatabase()
        d = cm.dict(DEFAULT)
        cm.set_default(key, value, cloud)

    @classmethod
    def get(cls, key, cloud):
        cm = CloudmeshDatabase()
        return(cm.get_default(key, cloud))

    @classmethod
    def delete(cls, key, cloud):
        cm = CloudmeshDatabase()
        _id = cm.getID("default", key, cloud)
        e = cm.find(DEFAULT, cm_id=_id).first()
        if e is not None:
            cm.delete(e)
