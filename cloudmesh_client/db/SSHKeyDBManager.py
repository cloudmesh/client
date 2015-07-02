import CloudmeshDatabase
from cloudmesh_client.keys.SSHKeyManager import SSHKeyManager, SSHkey
from cloudmesh_client.db.models import KEY
from cloudmesh_client.common.tables import dict_printer
from cloudmesh_base.util import path_expand
import os.path

class SSHKeyDBManager(object):
    def __init__(self, cm_user=None):
        self.db = CloudmeshDatabase.CloudmeshDatabase(cm_user)
        self.mykeys = SSHKeyManager()
        self.mykeys.get_from_dir("~/.ssh")

    def add(self, keyname):
        key_obj = KEY(cm_name=keyname)

        if os.path.isfile(path_expand(keyname)):
            sshkey = SSHkey(path_expand(keyname))
            key_obj.name = sshkey.__key__['comment']
            key_obj.value = sshkey.__key__['string']
        else:
            sshkey = self.mykeys.__keys__[keyname]
            key_obj.name = sshkey['comment']
            key_obj.value = sshkey['string']

        self.db.add([key_obj])
        self.db.save()


    def delete(self, keyname):
        self.db.delete_by_name(KEY, name=keyname)

    def find(self, keyname):
        return self.db.find_by_name(KEY,keyname)

    def dict(self):
        return self.db.dict(KEY)

    def update(self):
        print 'update'
