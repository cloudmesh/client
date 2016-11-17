import json
import operator

from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.playbook import Playbook
from ansible.vars import VariableManager

from cloudmesh_client.common.Shell import Subprocess, SubprocessError


class AnsiblePlaybookRunner(object):

    def __init__(self, inventory, path, user=None, become=False,
                 become_user=None, forks=None, extra_vars=None):
        self._inventory = inventory
        self._path = path
        self._user = user
        self._become = become
        self._become_user = become_user
        self._forks = forks
        self._extra_vars = extra_vars

        self._subprocess_kwargs = dict()

    def set_cwd(self, path):
        self._subprocess_kwargs['cwd'] = path
        return self

    def set_stderr(self, stream):
        self._subprocess_kwargs['stderr'] = stream
        return self

    def set_stdout(self, stream):
        self._subprocess_kwargs['stdout'] = stream
        return self

    def set_env(self, environment):
        self._subprocess_kwargs['env'] = environment
        return self

    def __call__(self):
        cmd_builder_monoid = [
            ['ansible-playbook'],
            ['--inventory', self._inventory] if self._inventory else [],
            ['--user', self._user] if self._user else [],
            ['--become'] if self._become else [],
            ['--become-user', self._become_user] if self._become_user else [],
            ['--forks', str(self._forks)] if self._forks else [],
            ['--extra-vars', json.dumps(self._extra_vars)] if self._extra_vars else [],
        ]

        cmd = reduce(operator.concat, cmd_builder_monoid)
        Subprocess(cmd, **self._subprocess_kwargs)


        ################################################################



if __name__ == '__main__':
    loader = DataLoader()
    variable_manager = VariableManager()
    playbook = Playbook(loader)
    Inventory(loader, variable_manager, host_list={'a': ['foo', 'bar'], 'b': ['foo', 'baz']})
