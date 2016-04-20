from cloudmesh_client.default import Default

from cloudmesh_client.common.ConfigDict import ConfigDict


class VMName(object):
    @staticmethod
    def format(name=None):
        """
        given a name that returns the following information as a tuple.

            prefix - the prefix of the vm name
            index - the current index
            padding - the padding factor to fill the index with leading 0

        The input name format is as follows prefix-0011 upon return you will get

            (prefix, 11, 4)

        if None is specified the current os user name will be used,
        the index will start as 1, and we will use four digits all in all
        for the padding.

        :param name: the name that derives a format for
        :return: prefix, index, padding
        """
        raise ValueError("implement me")

    @staticmethod
    def get(prefix=None, idx=None, user=None):
        """Return a vm name to use next time. prefix or index can be
        given to update a vm name (optional)

        Args:
            prefix (str, optional): the name of prefix
            idx (int, str, optional): the index to increment. This can be a
            digit or arithmetic e.g. +5 or -3 can be used

        """
        user = user or ConfigDict("cloudmesh.yaml")["cloudmesh.profile.user"]
        prefix = prefix or user
        if type(idx) is not int:
            idx = int(idx)
        Default.set('index', idx)
        return "%{:}_%{:}".format()

    @staticmethod
    def next():
        return VMName.vmname(idx="+1")


"""

def vm_name(username, index, n=10000):
    length = len(str(n))
    name = "{0}-{1:0" + str(length) + "d}"
    return name.format(username, index)


def server_name_analyzer(name):
    '''
    standard vm name, unless user gives the name, is prefix_index such as abc_11, this
    function returns vm name's prefix and index [prefix, index], if the name is not in
    standard form, returns [input, None]
    '''
    res = [x for x in name.split('_')]
    l = len(res)
    if l == 1:
        return [name, None]

    index = None
    try:
        index = int(res[-1])
    except:
        pass
    if index is None:
        return [name, None]

    prefix = None
    if l > 2:
        del res[-1]
        prefix = "_".join(res)
    else:
        prefix = res[0]
        return [prefix, index]

"""
