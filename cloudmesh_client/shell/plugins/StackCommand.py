from __future__ import print_function

import os

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
        stack.initialize(ips, user=user, branch=branch, name=name)
        project = BDSProject(ips=ips, user=user, name=name, branch=branch)
        return project


    # noinspection PyUnusedLocal
    @command
    def do_stack(self, args, arguments):
        """
        ::

            Usage:
                stack check [--stack=bds]
                stack init bds [--no-activate] [--branch=master] [--user=$USER] [--name=<project>] <ip>...


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

        # init
        arg.branch = arguments['--branch'] or 'master'
        arg.user = arguments['--user'] or os.getenv('USER')
        arg.activate = not arguments['--no-activate']

        print (arg)

        if arg.check:
            self.check(stackname=arg.stack)

        elif arg.init and arg.bds:
            self.init(stackname='bds', branch=arg.branch, user=arg.user, name=arg.name, ips=arg.ips, activate=arg.activate)


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
