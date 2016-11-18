

import os.path
import shutil
import tempfile

import yaml

from cloudmesh_client.deployer.ansible.playbook import AnsiblePlaybookRunner


class AnsibleRole(object):

    def __init__(self, path, become=True, variables=None):
        assert path is not None

        self.path = path
        self.name = os.path.basename(self.path)
        self.directory = os.path.dirname(self.path)
        self.become = become
        self.variables = variables or {}


    def run(self, inventory, user=None):
        tempdir = tempfile.mkdtemp()

        playbook = [{
            'name': 'Cloudmesh Role: ' + self.path,
            'hosts': 'all',
            'become': True if self.become else False,
            'roles': [dict(role=self.path,
                           **self.variables)]
        }]

        y = yaml.dump(playbook, default_flow_style=False)
        play = os.path.join(tempdir, 'playbook.yml')
        with open(play, 'w') as fd:
            fd.write(y)

        inventory_file = os.path.join(tempdir, 'inventory.txt')
        with open(inventory_file, 'w') as fd:
            fd.write(inventory)

        runner = AnsiblePlaybookRunner(inventory_file, play, user=user, modifyKnownHosts=False)
        runner.set_cwd(tempdir)

        # don't hide ansible's stderr/stdout
        runner.set_stderr(None)
        runner.set_stdout(None)

        runner()

        shutil.rmtree(tempdir)
