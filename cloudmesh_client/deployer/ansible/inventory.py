
from StringIO import StringIO
from collections import defaultdict



__all__ = ['Inventory', 'Node']


class Node(object):

    def __init__(self, name, address=None, user=None):
        self._name = name
        self._address = address or name
        self._user = user or None
        self._variables = dict()

    ################################################################ main api

    def add_var(self, key, value):
        """Add a variable and value to a node

        :param str key:
        :param str value:
        """

        self._variables[key] = value

    ################################################################ properties

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def user(self):
        return self._user

    @property
    def variables(self):
        """Get the dictionary of variables

        :rtype: :class:`dict`
        """

        d = dict(
            ansible_ssh_host=self._address
        )
        d.update(self._variables)
        if self.user:
            d['ansible_ssh_user'] = self.user

        return d


################################################################################


class Inventory(object):
    """Build an inventory by dynamically adding :class:`Host`s to :class:`Group`s"""

    def __init__(self):
        self._groups = defaultdict(list)
        self._nodes = set(['all'])

    @classmethod
    def from_cluster(cls, cluster):
        """Creates an inventory from a :class:`Cluster`

        :param cls:
        :param cluster:
        :returns:
        :rtype:
        """

        inventory = cls()
        for instance in cluster:
            node = Node(
                name = instance.name,
                address = instance.floating_ip or instance.static_ip,
                user = instance.username or None
            )
            inventory.add_node(node)

        return inventory

    def add_node(self, node, *groupnames):
        """Add a host to the inventory

        :param str groupname:
        :param Node host:
        """

        groupnames = groupnames or ['all']

        for groupname in groupnames:
            self._groups[groupname].append(node)

        self._nodes.add(node)

    def ini(self):
        """Generates the ansible inventory file

        :returns: the inventory as ini format
        :rtype: :class:`str`
        """

        builder = StringIO()
        for groupname, nodes in self._groups.iteritems():
            builder.write('[{}]\n'.format(groupname))
            for node in nodes:
                builder.write('{}'.format(node.name))
                for k, v in node.variables.iteritems():
                    builder.write(' {}="{}"'.format(k, v))
                builder.write('\n')
            builder.write('\n')

        ini = builder.getvalue().strip()
        builder.close()

        return ini

        # ################################
        # ## initialize the root Group, ## needed for the call to InventoryParser constructor

        # groups = {'all': Group('all')}

        # ################################
        # ## write the inventory to a temp file, then read it in using ansible API

        # with NamedTemporaryFile() as fd:
        #     fd.write(ini)
        #     fd.flush()
        #     inventory = InventoryParser(None, groups, filename=fd.name)
        #     return inventory




if __name__ == '__main__':
    from cloudmesh_client.default import Default
    cluster = Default.active_cluster
    i = Inventory.from_cluster(cluster)
    print(i.ini())

    n1 = Node('foo', address='129.114.110.195', user='cc')
    n2 = Node('bar', address='129.114.110.127', user='cc')
    n3 = Node('baz', address='129.114.111.200', user='cc')

    inventory = Inventory()
    inventory.add_node(n1, 'a', 'b')
    inventory.add_node(n2, 'c')
    inventory.add_node(n3, 'b', 'c')

    i = inventory.ini()
    print(i)
