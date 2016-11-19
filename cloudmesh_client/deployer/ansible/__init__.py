from .role import AnsibleRole


class AnsibleDeployer(object):

    def __init__(self, roles=None, inventory=None):
        self.roles = roles or []
        self.inventory = inventory

    def generate_playbook(self):
        pass

    def run(self):
        raise NotImplemented
