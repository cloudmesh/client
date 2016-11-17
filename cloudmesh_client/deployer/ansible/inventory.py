
from StringIO import StringIO
from collections import defaultdict, namedtuple
from tempfile import NamedTemporaryFile

from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Group, Host, Inventory
from ansible.inventory.ini import InventoryParser
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars import VariableManager


__all__ = ['InventoryBuilder', 'Node']


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


class InventoryBuilder(object):
    """Build an inventory by dynamically adding :class:`Host`s to :class:`Group`s"""

    def __init__(self):
        self._groups = defaultdict(list)
        self._nodes = set(['all'])

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
    n1 = Node('foo', address='129.114.110.195', user='cc')
    n2 = Node('bar', address='129.114.110.127', user='cc')
    n3 = Node('baz', address='129.114.111.200', user='cc')

    b = InventoryBuilder()
    b.add_node(n1, 'a', 'b')
    b.add_node(n2, 'c')
    b.add_node(n3, 'b', 'c')

    i = b.inventory()

    Options = namedtuple('Options', ['module_path'])
    loader = DataLoader()
    variable_manager = VariableManager()
    results_callback = CallbackBase()
    variable_manager.set_inventory
    play_source = dict(
        name = 'Ansible Play',
        hosts = 'all',
        tasks = [
            dict(action=dict(module='ping'))
        ],
    )
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
    tqm = TaskQueueManager(
        inventory = i,
        variable_manager = variable_manager,
        loader = loader,
        options = Options(),
        passwords = dict(),
    )
