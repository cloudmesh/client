from __future__ import print_function

import os
import time

from cloudmesh_client.cloud.stack import sanity_check, ProjectDB, Project, BigDataStack
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import PluginCommand, CloudPluginCommand
from cloudmesh_client.default import Default
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.dotdict import dotdict



class StackCommand(PluginCommand, CloudPluginCommand):
    topics = {"stack": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command stack")


    def check(self):
        sanity_check()


    def init(self, stackname='bds', activate=True, name=None, user=None, branch=None, **kwargs):
        factory = ProjectFactory()
        factory.activate(activate)

        if stackname == 'bds':
            factory.use_bds()
        else:
            raise NotImplementedError(stackname)

        if name:
            factory.set_project_name(name)

        if user:
            factory.set_user_name(user)

        if branch:
            factory.set_branch(branch)

        if ips:
            factory.set_ips(ips)


        project = factory()



    def init_bds(self, branch=None, ips=None, user=None, name=None):
        stack = BigDataStack()
        stack.initialize(ips, user=user, branch=branch)
        project = BDSProject(ips=ips, user=user, name=name, branch=branch)
        return project


    def list(self, sort=None, list=None, json=False):
        """List the deployment stacks and projects

        :param sort: field to sort by
        :param list: comma-separated subset of {'stack', 'project'}
        :param json: output in json-format
        """

        projectlist = ProjectList.load()

        print ('Projects')
        for project in projectlist:
            activated = '>' if projectlist.isactive(project) else ' '
            name = project.name
            stack = project.__class__.__name__ # FIXME: temporary workaround
            date = time.strftime('%Y-%m-%d %H:%M:%S UTC', project.ctime)
            path = os.path.join(projectlist.prefix(), project.name)
            msg = '- {activated} {name:10} {stack:10} {date:24} {path}'.format(
                activated=activated,
                name=name,
                stack=stack,
                date=date,
                path=path,
            )
            print (msg)


    def project(self, name=None):
        """View or set the current active project

        :param name: active this project
        """

        projectlist = ProjectList.load()

        if name is None:
            print (projectlist.getactive().name)

        else:
            project = projectlist.lookup(name)
            projectlist.activate(project)
            projectlist.sync()
            print ('Switched to project {}'.format(project.name))


    def deploy(self, **kwargs):
        """Deploy the currently active project

        :param **kwargs: passed to the implementing method (eg deploy_bds)
        """

        print (42)
        print (kwargs)

        projectlist = ProjectList.load()
        project = projectlist.getactive()
        path = projectlist.projectdir(project.name)
        if isinstance(project, BDSProject):
            project.deploy(path, **kwargs)
        else:
            raise ValueError('Unknown project type {}'.format(type(project)))




    # noinspection PyUnusedLocal
    @command
    def do_stack(self, args, arguments):
        """
        ::

            Usage:
                stack check [--stack=bds]
                stack init [--no-activate] [--branch=master] [--user=$USER] [--name=<project>] <ip>...
                stack list [--sort=<field=date>] [--list=<field,...=all>] [--json]
                stack project [<name>]
                stack deploy [<play>...] [--define=<define>...]


            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name

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

        ################################################## cleanup
        arg = dotdict(arguments)
        arg.ips = arguments['<ip>']

        # arg.cloud = arguments["--cloud"] or Default.cloud
        # arg.FORMAT = arguments["--format"] or "table"

        ##################################################  defaults
        arg.stack = arguments['--stack'] or 'bds'

        if arg.init:
            arg.branch = arguments['--branch'] or 'master'
            arg.user = arguments['--user'] or os.getenv('USER')
            arg.activate = not arguments['--no-activate']

        ################################################## list
        if arg.list:
            arg.sort = arguments['--sort']
            arg.listparts = arguments['--list']

        ##################################################
        arg.name = arguments['<name>']

        ##################################################
        if arg.deploy:
            arg.plays = arguments['<play>']
            arg.define = arguments['--define']


        print (arg)

        if arg.check:
            self.check()

        elif arg.init:
            self.init(stackname='bds', branch=arg.branch, user=arg.user, name=arg['--name'], ips=arg.ips, activate=arg.activate)

        elif arg.list:
            self.list(sort=arg['--sort'], list=arg['--list'], json=arg.json)

        elif arg.project:
            self.project(name=arg.name)

        elif arg.deploy:
            self.deploy(plays=arg.plays, defines=arg.define)

        return ""
