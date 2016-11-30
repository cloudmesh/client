from __future__ import print_function

import os
import time
from collections import defaultdict

from cloudmesh_client.cloud.stack import sanity_check, ProjectDB, ProjectFactory
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
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


class Command(object):

    def check(self):
        sanity_check()

    def init(self, stackname='bds', activate=True, name=None,
             username=None, branch=None, overrides=None, playbooks=None, ips=None,
             force=False, update=False):
        factory = ProjectFactory()

        if stackname == 'bds':
            factory.use_bds()
        else:
            raise NotImplementedError(stackname)

        factory\
            .set_project_name(name)\
            .set_user_name(os.getenv('USER') if username is '$USER' else username)\
            .set_branch(branch)\
            .set_ips(ips)\
            .set_overrides(overrides)\
            .set_playbooks(playbooks)\
            .activate(activate)\
            .set_force(force=force)\
            .set_update(update)

        project = factory()
        Console.info('Created project {}'.format(project.name))

    def deploy(self, project_name=None, force=False):

        db = ProjectDB()
        project = db.lookup(project_name)
        project.deploy(force=force)
        db.update(project)

    def project(self, list_projects=False, name=None):

        db = ProjectDB()

        # set if name is given
        if name:
            project = db.lookup(name)
            db.activate(project)

        # list of asked to do so
        if list_projects:
            for project in db:
                isactive = '>' if db.isactive(project) else ''
                ctime = time.strftime('%Y-%m-%d %H:%M:%S', project.ctime)
                msg = ''
                msg += '{isactive:3s}'
                msg += '{project.name:10s}'
                msg += 'created: {ctime}'
                msg += 'stack: {project.stack.__class__.__name__:16s}'
                msg += 'deployed: {project.is_deployed}'
                msg = msg.format(isactive=isactive,
                                 project=project, ctime=ctime)
                Console.info(msg)

class StackCommand(PluginCommand, CloudPluginCommand):
    topics = {"stack": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command stack")


    # noinspection PyUnusedLocal
    @command
    def do_stack(self, args, arguments):
        """
        ::

            Usage:
              stack check
              stack init [-fU] [--no-activate] [-s STACK] [-n NAME] [-u NAME] [-b NAME] [-o DEFN]... [-p PLAY] <ip>...
              stack deploy [-f] [-n NAME]
              stack project [-l] [<name>]

            Commands:
              check     Sanity check
              init      Initialize a stack
              deploy    Deploy a stack
              project   List and activate projects

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
              -u NAME --username=NAME       Name of login user to cluster [default: $USER]
              -b NAME --branch=NAME         Name of the stack's branch to clone from [default: master]
              -o DEFN --overrides=DEFN      Overrides for a playbook, may be specified multiple times
              -p PLAY --playbooks=PLAY      Playbooks to run
              -f --force                    Force rerunning a command to continue
              -U --update                   Update the stack
              -l --list                     List

            Examples:

             The following example assumes that a cluster (Ubuntu
             14.04) has been launched already and can be accessed by
             the 'ubuntu` user at addresses 10.0.0.10, 10.0.0.11, and
             10.0.0.12.

                # verify the environment
                cm stack check

                # create a project for the cluster with given username and addresses
                cm stack init -u ubuntu -p play-hadoop.yml,addons/spark.yml 10.0.0.10 10.0.0.11 10.0.0.12

                # deploy hadoop, spark to the cluster
                cm stack deploy

        """

        a = dotdict(arguments)
        cmd = Command()
        print(a)

        if a.check:
            cmd.check()

        if a.init:
            defns = cleanup_overrides(
                a['--overrides']) if a['--overrides'] else None
            plays = a['--playbooks'].split(',') if a['--playbooks'] else None

            cmd.init(stackname=a['--stack'],
                     name=a['--name'],
                     branch=a['--branch'],
                     username=a['--username'],
                     activate=not a['--no-activate'],
                     overrides=defns,
                     playbooks=plays,
                     ips=a['<ip>'],
                     force=a['--force'],
                     update=a['--update'],
            )

        if a.deploy:
            cmd.deploy(project_name=a['--name'],
                       force=a['--force'],
            )

        if a.project:
            cmd.project(list_projects=a['--list'],
                        name=a['<name>'],
            )

        return ""
