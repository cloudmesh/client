from __future__ import absolute_import
from pprint import pprint

from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_base.menu import menu_return_num
from cloudmesh_client.keys.SSHKeyManager import SSHkey
from cloudmesh_client.db.model import KEY, KEYCLOUDMAP
from cloudmesh_client.db import CloudmeshDatabase

from sqlite3 import IntegrityError

# noinspection PyBroadException
class SSHKeyDBManager(object):
    def __init__(self, user=None):
        self.db = CloudmeshDatabase.CloudmeshDatabase(user)

    def add(self, key_path, keyname=None, user=None, source=None, uri=None):
        """
        Adds the key to the database based on the path

        :param keyname: name of the key or path to the key
        :return:
        """

        sshkey = SSHkey(Config.path_expand(key_path))

        self.add_from_sshkey(sshkey.__key__,
                             keyname, user,
                             source=source,
                             uri=uri)

    def _add(self, obj):
        try:
            self.db.add(obj)
            self.db.save()
        except IntegrityError, e:
            raise ValueError("Key already exists")


    def add_from_dict(self, d):
        pprint(d)

        key_obj = KEY(name='{keyname}'.format(**d),
                      uri='{uri}'.format(**d),
                      source='{source}'.format(**d),
                      comment='{comment}'.format(**d),
                      cloud="general",
                      user='{user}'.format(**d),
                      fingerprint='{fingerprint}'.format(**d),
                      value='{string} {comment}'.format(**d),
                      )

        self._add([key_obj])

    def add_from_sshkey(self,
                        sshkey,
                        keyname=None,
                        user=None,
                        source=None,
                        uri=None):

        if keyname is None:
            try:
                keyname = sshkey['name']
            except:
                pass
        if keyname is None:
            print ("ERROR: keyname is None")

        # pprint(sshkey)


        # find if the key with fingerprint already exists

        # if so return warning and return command


        key_obj = KEY(
            keyname,
            sshkey['string'],
            uri=sshkey['uri'],
            source=sshkey['source'],
            fingerprint=sshkey['fingerprint'],
            comment=sshkey['comment'],
            type="sshkey",
            # group=None,
            cloud="general",
            user=user)

        # pprint(key_obj.__dict__)
        self._add(key_obj)

    def delete(self, keyname):
        """
        Deletes the key from the database based on the keyname

        :param keyname: name of the key to be delete
        :return:
        """
        self.db.delete_by_name(KEY, name=keyname)

    def set_default(self, keyname):
        default_key = self.get_default()
        if default_key:
            default_key.is_default = 'False'
        self.find(keyname).is_default = 'True'
        self.db.save()

    def get_default(self):
        value = "True"
        return self.db.get(KEY, is_default=value)

    def find(self, keyname):
        """
        Finds the key on the database based on the keyname

        :param keyname: name of the key to be found
        :return: Query object of the search
        """
        return self.db.find_by_name(KEY, name=keyname)

    def find_all(self):
        """

        :return: Query object from all the entries
        """
        return self.db.find(KEY)

    def table_dict(self):
        """

        :return: dict from all elements in the table KEY
        """
        return self.db.dict(KEY)

    def update(self, clouds):
        # i'm not sure how this function works
        self.db.update("key", clouds)

    def delete_all(self):
        """
        Deletes all the entries from KEY table

        :return:
        """
        self.db.delete_all(KEY)

    def select(self):
        options = []
        d = self.table_dict()
        for i in d:
            # print ('i:', i)
            line = '{}: {}'.format(d[i]['name'], d[i]['fingerprint'])
            options.append(line)
        num = menu_return_num('KEYS', options)
        if num != 'q':
            return options[num]
        return num

    def object_to_dict(self, obj):
        """

        :param obj: object to be converted to dict
        :return: dict from the object
        """
        return self.db.object_to_dict(obj)

    def add_key_cloud_map_entry(self, user, keyname, cloud, name_on_cloud):
        """
        Adds an entry to Key-Cloud map table.
        :param keyname: Name of the key in db.
        :param cloud: Cloud on which the key is being uploaded.
        :param name_on_cloud: Name of the key on cloud.
        :return:
        """

        keycloudmap = self.db.find(KEYCLOUDMAP, output="object", user=user, key_name=keyname, cloud_name=cloud)
        keycloudmapdict = self.db.object_to_dict(keycloudmap)
        # print(keycloudmap)
        if keycloudmapdict is not None and len(keycloudmapdict) != 0:
            keycloudmap.update({'user': user,
                                'key_name': keyname,
                                'cloud_name': cloud,
                                'key_name_on_cloud': name_on_cloud})
            self.db.save()
        else:
            keycloudmap = KEYCLOUDMAP(user, keyname, cloud, name_on_cloud)
            self._add(keycloudmap)

    def get_key_cloud_maps(self):
        """
        Returns entries in Key-Cloud map table.
        :param keyname: Name of the key in db.
        :return:
        """

        keycloudmap = self.db.find(KEYCLOUDMAP)

        return keycloudmap

    def get_key_cloud_map_entry(self, keyname):
        """
        Returns entries in Key-Cloud map table.
        :param keyname: Name of the key in db.
        :return:
        """

        keycloudmap = self.db.find(KEYCLOUDMAP, key_name=keyname)

        return keycloudmap

    def delete_key_cloud_map_entry(self, keyname):
        """
        Deletes an entry to Key-Cloud map table.
        :param keyname: Name of the key in db.
        :return:
        """

        keycloudmap = self.db.find(KEYCLOUDMAP, output="object", key_name=keyname)
        # print(keycloudmap.values())
        for key in keycloudmap:
            # print("Deleting: {:}".format(key))
            self.db.delete(key)
