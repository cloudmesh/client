class cluster(object):  // list abstraction see other commands


    def __init__(self):
        pass

    def list(self):
        pass

    def delete(self):
        pass

    def create(self):
        pass

    def add(self):
        "add nodes to the cluster"
        pass


    def remove(self):
        "add nodes to the cluster"
        pass

    def modify(self):
        "modifies nodes to the cluster"
        pass


    def terminate(self):
        "is same as delete?"
        pass

    def suspend(self):
        "is same as delete?"
        pass

    def resume(self):
        "is same as delete?"
        pass

    def add_key(self):
        pass

    def remove_key(self):
        pass

    def enable_cross_ssh_login(self):
        "create keys on each node"
        pass

    def disable_cross_ssh_login(self):
        pass

    def delete_key(self):
        pass

    """

    Parameter.expand

    cluster
        name
        node+
                        (some object in models)
            label
            name
            ip+
            private key
            ssh authorized keys
            owner
            user

    type cluster
    type node

    """