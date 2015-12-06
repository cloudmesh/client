from __future__ import print_function
from cloudmesh_client.common.ConfigDict import ConfigDict

from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.ListResource import ListResource


class Counter(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def incr(cls):

        # make sure counter is there, this coudl be done cleaner
        prefix, data = Counter.get()

        d = ConfigDict("cloudmesh.yaml")

        if "username" not in d["cloudmesh"]["profile"]:
            raise RuntimeError("Profile username is not set in yaml file.")

        username = d["cloudmesh"]["profile"]["username"]

        element = cls.cm.find("PREFIXCOUNT", prefix=username)

        if element is None or len(element) == 0:
            raise RuntimeError("ERROR while incrementing prefix count. Prefix not found in database\
                                for username {}".format(username))

        # Incrementing the count here
        count = element[username]["count"]
        count += 1

        cls.cm.update_prefix(prefix=username, count=count)
        cls.cm.save()

    @classmethod
    def get(cls):
        """
        Function that returns the prefix username and count for vm naming.
        If it is not present in db, it creates a new entry.
        :return:
        """
        d = ConfigDict("cloudmesh.yaml")

        if "username" not in d["cloudmesh"]["profile"]:
            raise RuntimeError("Profile username is not set in yaml file.")

        username = d["cloudmesh"]["profile"]["username"]

        element = cls.cm.find("PREFIXCOUNT", prefix=username)

        # If prefix entry not present, add it.
        if element is None or len(element) == 0:
            element_dict = cls.cm.db_obj_dict("PREFIXCOUNT", prefix=username, count=1)
            count = 1
            cls.cm.add_obj(element_dict)
            cls.cm.save()
        else:
            count = element[username]["count"]

        # print(element)
        return username, count
