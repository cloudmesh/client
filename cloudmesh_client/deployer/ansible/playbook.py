import json
import operator
import tempfile

import yaml

from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.playbook import Playbook
from ansible.vars import VariableManager

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Shell import Subprocess


class AnsiblePlaybook(object):

    def __init__(self, inventory, roles=None, path=None, username=None, become=False,
                 become_user=None, forks=None, modifyKnownHosts=True,
                 extra_vars=None, subprocess_kwargs=None):
        self._inventory = inventory
        self._roles = roles or []
        self._path = path
        self._username = username
        self._become = become
        self._become_user = become_user
        self._forks = forks
        self._modifyKnownHosts = modifyKnownHosts
        self._extra_vars = extra_vars
        self._subprocess_kwargs = subprocess_kwargs or dict()

        ################################################################ rest of setup

        self._inventory_file = tempfile.NamedTemporaryFile()
        self._playbook_file  = tempfile.NamedTemporaryFile()

        # write inventory
        self._inventory_file.write(self._inventory.ini())
        self._inventory_file.flush()

        Console.debug_msg('Inventory:\n' + self._inventory.ini())

        # write playbook
        playbook = [{
            'name': role.name,
            'hosts': role.hosts,
            'become': role.become,
            'roles': [dict(role=role.path,
                           **role.variables)]}
                    for role in roles]
        yml = yaml.dump(playbook)
        self._playbook_file.write(yml)
        self._playbook_file.flush()

        Console.debug_msg('Playbook:\n' + yml)

    def run(self):
        return self()

    def __call__(self):

        cmd_builder_monoid = [
            ['ansible-playbook'],

            ['--inventory', self._inventory_file.name]
            if self._inventory else [],

            ['--user', self._username]
            if self._username else [],

            ['--become']
            if self._become else [],

            ['--become-user', self._become_user]
            if self._become_user else [],

            ['--forks', str(self._forks)]
            if self._forks else [],

            ['--ssh-extra-args', '-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no']
            if not self._modifyKnownHosts else []

            ['--extra-vars', json.dumps(self._extra_vars)]
            if self._extra_vars else [],

            [self._playbook_file.name],
        ]

        cmd = reduce(operator.concat, cmd_builder_monoid)
        Subprocess(cmd, **self._subprocess_kwargs)


        ################################################################



if __name__ == '__main__':
    loader = DataLoader()
    variable_manager = VariableManager()
    playbook = Playbook(loader)
    Inventory(loader, variable_manager, host_list={'a': ['foo', 'bar'], 'b': ['foo', 'baz']})
