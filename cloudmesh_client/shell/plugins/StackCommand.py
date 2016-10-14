from __future__ import print_function

import os
import time
from collections import defaultdict

from cloudmesh_client.cloud.stack import sanity_check, ProjectDB, ProjectFactory, BigDataStack
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.default import Default
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.dotdict import dotdict


def cleanup_overrides(overrides):
    """Cleanup shell-parameterized overrides definitions

    :param overrides: list of [(play:k1=v1,k2=v2)...]
    :returns: 
    :rtype: dict[play] -> dict[key] -> value
    """

    result = defaultdict(dict)
    for definition in overrides:
        play, defs = definition.split(':', 1)
        pairs = defs.split(',')
        for pair in pairs:
            k, v = pair.split('=', 1)
            result[play][k] = v

    return result



class StackCommand(PluginCommand, CloudPluginCommand):
    topics = {"stack": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command stack")


    def check(self):
        sanity_check()


    def init(self, stackname='bds', activate=True, name=None, user=None, branch=None, overrides=None, playbooks=None, ips=None, force=False):
        factory = ProjectFactory()
        factory\
            .activate(activate)\
            .set_force(force=force)

        if stackname == 'bds':
            factory.use_bds()
        else:
            raise NotImplementedError(stackname)

        if name:
            Console.debug_msg('Setting factory project name: {}'.format(name))
            factory.set_project_name(name)

        if user:
            Console.debug_msg('Setting factory user name: {}'.format(user))
            factory.set_user_name(user)

        if branch:
            Console.debug_msg('Setting factory branch: {}'.format(branch))
            factory.set_branch(branch)

        if ips:
            Console.debug_msg('Setting factory ips: {}'.format(ips))
            factory.set_ips(ips)

        if overrides:
            Console.debug_msg('Setting factory overrides: {}'.format(overrides))
            factory.set_overrides(overrides)

        if playbooks:
            Console.debug_msg('Setting factory playbooks: {}'.format(playbooks))
            factory.set_playbooks(playbooks)


        project = factory()
        Console.info('Created project {}'.format(project.name))


    def deploy(self, project_name=None):

        db = ProjectDB()
        project = db.lookup(project_name)
        project.deploy()



    # noinspection PyUnusedLocal
    @command
    def do_stack(self, args, arguments):
        """
        ::

            Usage:
              stack check
              stack init [-f] [--no-activate] [-s STACK] [-n NAME] [-u NAME] [-b NAME] [-o DEFN]... [-p PLAY] <ip>...
              stack deploy [-n NAME]

            Commands:
              check     Sanity check
              init      Initialize a stack
              deploy    Deploy a stack

            Arguments:
              STACK  Name of the stack. Options: (bds)
              NAME   Alphanumeric name
              DEFN   In the form: play1:k1=v1,k2=v2,...
              PLAY   In the form: playbook,playbook,...

           Options:

              -v --verbose
              --no-activate                 Do not activate a project upon creation
              -s STACK --stack=STACK        The stack name [default: bds]
              -n NAME --name=NAME           Name of the project (if not specified during creation, generated).
              -u NAME --user=NAME           Name of login user to cluster [default: $USER]
              -b NAME --branch=NAME         Name of the stack's branch to clone from [default: master]
              -o DEFN --overrides=DEFN      Overrides for a playbook, may be specified multiple times
              -p PLAY --playbooks=PLAY      Playbooks to run
              -f --force                    Force rerunning a command to continue

            Examples:

             The following example assumes that a cluster (Ubuntu
             14.04) has been launched already and can be accessed by
             the 'ubuntu` user at addresses 10.0.0.10, 10.0.0.11, and
             10.0.0.12.

                # verify the environment
                cm stack check

                # create a project for the cluster with given username and addresses
                cm stack init --user ubuntu 10.0.0.10 10.0.0.11 10.0.0.12

                # get the name of the project
                cm stack project

                # deploy hadoop, spark, and hbase to the cluster
                cm stack deploy play-hadoop.yml addons/spark.yml addons/hbase.yml

        """

        a = dotdict(arguments)
        print(a)


        if a.check:
            self.check()

        if a.init:
            defns = cleanup_overrides(a['--overrides']) if a['--overrides'] else None
            plays = a['--playbooks'].split(',') if a['--playbooks'] else None

            self.init(stackname = a['--stack'],
                      name      = a['--name'],
                      branch    = a['--branch'],
                      user      = a['--user'],
                      activate  = not a['--no-activate'],
                      overrides = defns,
                      playbooks = plays,
                      ips       = a['<ip>'],
                      force     = a['--force'],
            )

        if a.deploy:
            self.deploy(project_name=a['--name'])


        # elif arg.init:
        #     self.init(stackname='bds', branch=arg.branch, user=arg.user, name=arg['--name'], ips=arg.ips, activate=arg.activate)

        # elif arg.list:
        #     self.list(sort=arg['--sort'], list=arg['--list'], json=arg.json)

        # elif arg.project:
        #     self.project(name=arg.name)

        # elif arg.deploy:
        #     self.deploy(plays=arg.plays, defines=arg.define)

        return ""
