from __future__ import absolute_import, print_function

import json

import os
import os.path
from subprocess import check_call, check_output, CalledProcessError
from .ClusterCommand2 import Command as ClusterCommand

from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.db import CloudmeshDatabase, SPECIFICATION
from cloudmesh_client.default import Default, Names
from cloudmesh_client.shell.command import CloudPluginCommand, PluginCommand, \
    command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.util import exponential_backoff

# DB = CloudmeshDatabase()


class Command(object):

    def fingerprint(self, workdir=None, clustername=None, username=None, provision=True):

        workdir = workdir or os.getcwd()
        repo = 'git://github.com/cloudmesh/example-project-nist-fingerprint-matching'
        local_name = 'nist-fingerprint-matching'
        local_path = os.path.join(workdir, local_name)
        bds = os.path.join(local_path, 'big-data-stack')
        inventory = os.path.join(bds, 'inventory.txt')
        venv = os.path.join(local_path, 'venv')
        vpip = os.path.join(venv, 'bin', 'pip')
        vpython = os.path.join(venv, 'bin', 'python')
        vansible = os.path.join(venv, 'bin', 'ansible')
        vansible_playbook = os.path.join(venv, 'bin', 'ansible-playbook')

        ################################################################ 

        if os.path.exists(local_path) and not os.path.isdir(local_path):
            raise OSError('{} exists but is not a directory'.format(local_path))

        elif os.path.exists(local_path) and os.path.isdir(local_path):
            Console.ok('Fetching upstream changes')
            check_call(['git', 'fetch', 'origin'], cwd=local_path)

            Console.ok('Rebasing any local changes')
            check_call(['git', 'rebase', 'origin/master'], cwd=local_path)


        elif not os.path.exists(local_path):
            Console.info('Cloning fingerprint example')
            check_call(['git', 'clone', '--recursive', repo, local_path])

        ################################################################

        Console.ok('Getting cluster')
        cluster_cmd = ClusterCommand()
        cluster = cluster_cmd.allocate(clustername=clustername)
        user = username or cluster.username
        ips = [vm.floating_ip for vm in cluster.list()]

        if provision:

            Console.ok('Creating virtualenv')
            check_call(['virtualenv', venv])

            Console.ok('Installing dependencies')
            check_call([vpip, 'install', '-U',
                        '-r', os.path.join(local_path, 'big-data-stack', 'requirements.txt')])

            Console.ok('Generating inventory file')
            mkinventory = [vpython, 'mk-inventory', '-n', cluster.name+'-'] + ips
            Console.debug_msg(' '.join(mkinventory))
            i = check_output(mkinventory, cwd=bds)
            with open(inventory, 'w') as fd:
                fd.write(i)
            print(i)

            Console.ok('Ping nodes')

            def wait_for_ping():
                ping = [vansible, 'all', '-m', 'ping', '-u', user]
                Console.debug_msg(' '.join(ping))
                try:
                    check_call(ping, cwd=bds)
                    return True
                except CalledProcessError:
                    return False

            exponential_backoff(wait_for_ping)

            Console.ok('Provisioning')
            cmd = [vansible_playbook,
                   '-u', user,
                   'play-hadoop.yml',
                   'addons/zookeeper.yml',
                   'addons/spark.yml',
                   'addons/hbase.yml',
                   'addons/drill.yml',
                   '../software.yml',
                   '../dataset.yml',
                   '-e', 'drill_with_hbase=True',
            ]
            Console.debug_msg(' '.join(cmd))
            check_call(cmd, cwd=bds)

        ################################################################

        Console.ok('Running Fingerprint matching')
        cmd = [vansible_playbook, '-u', user, '../match.yml']
        Console.debug_msg(' '.join(cmd))
        check_call(cmd, cwd=bds)

        ################################################################

        # This doesn't use Ansible since we want to see the result of
        # the query
        Console.ok('Querying for matches')
        cmd = ['ssh', '-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no',
               '-l', 'hadoop',
               cluster.list()[0].floating_ip,
               '/tmp/query.sh']
        Console.debug_msg(' '.join(cmd))
        check_call(cmd)


class NistCommand(PluginCommand, CloudPluginCommand):

    topics = {"nist": "nist"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command nist")

    @command
    def do_nist(self, arg, arguments):
        """
        ::

           Usage:
             nist fingerprint [-c CLUSTER] [-u TEXT] [-N]

           Arguments:

             CLUSTER         Name of a cluster
             TEXT            String

           Commands:

             fingerprint     Run the fingerprint example

           Options:

             -c --cluster=CLUSTER  Name of a defined cluster
             -u --username=TEXT    Username to log in with
             -N --no-provision     Do not provision
        """

        arguments = dotdict(arguments)
        cmd = Command()

        if arguments.fingerprint:
            cmd.fingerprint(clustername=arguments['--cluster'],
                            username=arguments['--username'],
                            provision=not arguments['--no-provision'],
            )

