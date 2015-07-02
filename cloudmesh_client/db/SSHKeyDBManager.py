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
        """
        Adds the key to the database based on the keyname (from SSHKeyManaager) or path

        :param keyname: name of the key or path to the key
        :return:
        """
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
        """
        Deletes the key from the database based on the keyname

        :param keyname: name of the key to be delete
        :return:
        """
        self.db.delete_by_name(KEY, name=keyname)

    def find(self, keyname):
        """
        Finds the key on the database based on the keyname

        :param keyname: name of the key to be found
        :return: Query object of the search
        """
        return self.db.find_by_name(KEY,keyname)

    def find_all(self):
        """

        :return: Query object from all the entries
        """
        return self.db.find(KEY).all()

    def dict(self):
        """

        :return: dict from all elements in the table KEY
        """
        return self.db.dict(KEY)

    def update(self, clouds):
        #i'm not sure how this function works
        self.db.update("key", clouds)

    def delete_all(self):
        """
        Deletes all the entries from KEY table

        :return:
        """
        self.db.delete_all(['KEY'])

    def object_to_dict(self, obj):
        """

        :param obj: object to be converted to dict
        :return: dict from the object
        """
        return self.db.object_to_dict(obj)