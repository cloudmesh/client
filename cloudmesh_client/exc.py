"""
This module contains the exceptions
"""


class UnrecoverableErrorException(Exception):
    """Occurs on an error that cannot be recovered automatically.
    Requires user interaction to change the state.
    """

    pass


class NoActiveClusterException(Exception):
    """Occurs when an active cluster is requested but non is set_cloud"""


class ClusterNameClashException(Exception):
    """Occurs when a cluster is created with a preexisting name
    """

    def __init__(self, tablename, name):
        self.tablename = tablename
        self.name = name

    def __str__(self):
        return 'Cluster {} already exists'.format(self.name)
