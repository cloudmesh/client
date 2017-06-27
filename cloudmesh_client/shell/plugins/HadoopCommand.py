from __future__ import absolute_import, print_function

import json

import os.path
from .ClusterCommand2 import Command as ClusterCommand
from .StackCommand import Command as StackCommand

from cloudmesh_client.cloud.stack import BigDataStack, ProjectDB, \
    ProjectFactory, SanityCheckError
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.db import CloudmeshDatabase, SPECIFICATION
from cloudmesh_client.default import Default, Names
from cloudmesh_client.shell.command import CloudPluginCommand, PluginCommand, \
    command
from cloudmesh_client.shell.console import Console


db = CloudmeshDatabase()


class Command(object):

    def sync(self, stackname=None):

        name = stackname or Default.active_stack

        try:
            spec = db.select(SPECIFICATION, type='stack', name=name)[0]
        except IndexError:
            Console.error('No project defined. Use `cm hadoop define` first')
            return

        kwargs = spec.get()
        path = kwargs.pop('local_path')
        stack = BigDataStack(path, **kwargs)
        stack.init(force=True, update=True)
        stack.sync_metadata()

    def define(self, name=None, **kwargs):
            """Define a hadoop stack.

            """

            stackname = name or Default.generate_name(Names.STACK_COUNTER)

            # remove None to defer default definitions to latter
            for k in kwargs.keys():
                if kwargs[k] is None:
                    del kwargs[k]

            kwargs['local_path'] = os.path.join(os.path.expanduser('~/.cloudmesh/stacks'), stackname)

            try:
                spec = db.select(SPECIFICATION, name=stackname, type='stack')[0]
                spec.update(kwargs)
                db.updateObj(spec)
            except IndexError:
                spec = SPECIFICATION(stackname, 'stack', kwargs)
                db.insert(spec)

            Default.set_stack(stackname)
            Console.ok('Defined stack {}'.format(stackname))

    def addons(self):
        """List the addons available

        :returns: list of addons
        :rtype: list
        """

        # FIXME: don't hardcode the list of available stack addons
        #
        # The list of addons should ideally be dynamically
        # discoverable from the current active stack. This hardcoding
        # is intended to be a temporary workaround.
        #
        # The list of addons are in the addons subdir of the BDS repo:
        # https://github.com/futuresystems/big-data-stack/tree/master/addons
        addons = [
            'hbase',
            'hive',
            'pig',
            'spark',
        ]

        return addons

    def deploy(self, clustername=None, stackname=None):

        stackname = stackname or Default.active_stack
        spec = db.select(SPECIFICATION, name=stackname, type='stack')[0]
        opts = spec.get()

        cluster_cmd = ClusterCommand()
        cluster = cluster_cmd.allocate(clustername=clustername)
        user = cluster.username

        stack = BigDataStack.load(opts.get('local_path'))
        stack.deploy(
            ips = [node.floating_ip or node.static_ip for node in cluster],
            name = stackname,
            user = user,
            playbooks = ['play-hadoop.yml'] + ['addons/%s.yml' % addon for addon in opts['addons']],
            defines = opts.get('defines', None),
        )

    def avail(self):

        specs = db.select(SPECIFICATION, type='stack')
        active = Default.active_stack

        return active, specs

    def use(self, specname):
        """Activate the given specification

        :param specname: namne of the specification
        """
        spec = db.select(SPECIFICATION, type='stack', name=specname)[0]
        Default.set_stack(spec.name)


class HadoopCommand(PluginCommand, CloudPluginCommand):

    topics = {"hadoop": "cluster"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command hadoop")

    @command
    def do_hadoop(self, arg, arguments):
        """
        ::

           Usage:
             hadoop sync
             hadoop addons
             hadoop define [-r REPO] [-b NAME] [-d COUNT] [ADDON]...
             hadoop undefine [NAME]...
             hadoop avail
             hadoop use NAME
             hadoop deploy

           Arguments:

             REPO            Repository location
             CLUSTER         Name of a cluster
             ADDON           Big Data Stack addon (eg: spark, hbase, pig)
             NAME            Alphanumeric name
             COUNT           Integer greater than zero

           Commands:

             sync       Checkout / synchronize the Big Data Stack
             addons     List available addons
             define     Create a deployment specification
             undefine   Delete the active or given specifications
             avail      Show available deployment specifications
             use        Activate the specification with the given name
             deploy     Deploy the active specification onto the active cluster

           Options:

             -r --repo=REPO        Location of the repository
             -b --branch=NAME      Branch to use
             -d --depth=COUNT      Clone depth

        """

        arguments = dotdict(arguments)
        cmd = Command()

        if arguments.sync:

            cmd.sync()

        elif arguments.addons:

            addons = cmd.addons()
            for name in addons:
                print(name)

        elif arguments.define:

            cmd.define(
                addons=arguments['ADDON'],
                repo=arguments['--repo'],
                branch=arguments['--branch'],
                depth=arguments['--depth'],
            )

        elif arguments.undefine:

            cmd.undefine(
                names=arguments['NAME']
            )

        elif arguments.avail:

            active, specs = cmd.avail()

            for spec in specs:
                marker = '>' if spec.name == active else ' '
                print('{} {}'.format(marker, spec.name))
                for k, v in spec.get().iteritems():
                    print('{:>4}{:<30}: {}'.format('', k, v))


        elif arguments.use:

            cmd.use(arguments['NAME'][0])

        elif arguments.deploy:

            cmd.deploy()

        else:
            raise NotImplementedError(args, arguments)
