from __future__ import print_function

import os
import time

from cloudmesh_client.cloud.stack import BigDataStack, BDSProject, ProjectList
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


    def check(self, stackname='bds'):
        if stackname == 'bds':
            stack = BigDataStack()
        else:
            raise NotImplementedError(stackname)

        stack.sanity_check()


    def init(self, stackname='bds', activate=True, **kwargs):
        if stackname == 'bds':
            project = self.init_bds(**kwargs)
        else:
            raise NotImplementedError(stackname)

        projectlist = ProjectList.load()
        projectlist.add(project)

        if activate:
            projectlist.activate(project)

        projectlist.sync()


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


    # noinspection PyUnusedLocal
    @command
    def do_stack(self, args, arguments):
        """
        ::

            Usage:
                stack check [--stack=bds]
                stack init bds [--no-activate] [--branch=master] [--user=$USER] [--name=<project>] <ip>...
                stack list [--sort=<field=date>] [--list=<field,...=all>] [--json]
                stack project [<name>]


            Options:
               --format=FORMAT  the output format [default: table]
               --cloud=CLOUD    the cloud name

            Examples:
                cm stack bds init

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


        print (arg)

        if arg.check:
            self.check(stackname=arg.stack)

        elif arg.init and arg.bds:
            self.init(stackname='bds', branch=arg.branch, user=arg.user, name=arg['--name'], ips=arg.ips, activate=arg.activate)

        elif arg.list:
            self.list(sort=arg['--sort'], list=arg['--list'], json=arg.json)

        elif arg.project:
            self.project(name=arg.name)

        """
        # TAKEN FRO INFO COMMAND TO DEMONSTRATE SOME SIMPLE USAGE

        d = {
            "cloud": arg.cloud,
            "key": Default.key,
            "user": Default.user,
            "vm": Default.vm,
            "group": Default.group,
            "secgroup": Default.secgroup,
            "counter": Default.get_counter(name="name"),
            "image": Default.get_image(category=arg.cloud),
            "flavor": Default.get_flavor(category=arg.cloud),
            "refresh": str(Default.refresh),
            "debug": str(Default.debug),
            "interactive": str(Default.interactive),
            "purge": str(Default.purge),

        }
        order = ["cloud", "key", "user", "vm", "group", "secgroup",
                 "counter", "image", "flavor", "refresh", "debug", "interactive", "purge"]
        print(Printer.attribute(d, order=order, output=arg.FORMAT, sort_keys=False))

        if d["key"] in ["TBD", ""] or d["user"] in ["TBD", ""]:
            msg = "Please replace the TBD values"
            msg = msg + "\nSee Also: \n\n" \
                  + "    cm register profile \n" \
                  + "    cm default user=YOURUSERNAME\n"
            Console.error(msg, traceflag=False)
        """
        return ""
