from __future__ import print_function

from cloudmesh_client.db import CloudmeshDatabase


class Counter(object):
    """
    A counter is used to keep track of some value that can be increased
    and is associated with a user. Typically it is used to increment the
    vm id or the job id.
    """

    cm = CloudmeshDatabase()

    @classmethod
    def incr(cls, name='counter', user=None):
        """
        increments the counter by one

        :param name: name of the counter
        :param user: username associated with the counter
        :return:
        """

        cls.cm.counter_incr(name=name, user=user)

    @classmethod
    def get(cls, name='counter', user=None):
        """
        returns the value of the counter

        :param name: name of the counter
        :param user: username associated with the counter
        :return: the value of the counter
        """

        return cls.cm.counter_get(name=name, user=user)

    @classmethod
    def set(cls, name='counter', value=None, user=None):
        """
        sets a counter associated with a particular user
        :param name: name of the counter
        :param user: username associated with the counter
        :param value: the value
        :return:
        """

        cls.cm.counter_set(name=name, value=value, user=user)
