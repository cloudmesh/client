from __future__ import print_function

from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase


class Counter(object):
    cm = CloudmeshDatabase()

    @classmethod
    def incr(cls, name='counter', user=None):
        cls.cm.counter_incr(name=name, user=user)

    @classmethod
    def get(cls, name='counter', user=None):
        return cls.cm.counter_get(name=name, user=user)

    @classmethod
    def set(cls, name='counter', value=None, user=None):
        cls.cm.counter_set(name=name, value=value, user=user)
