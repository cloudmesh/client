from __future__ import absolute_import, print_function

import os.path

from .ClusterCommand2 import Command as ClusterCommand
from .StackCommand import Command as StackCommand
from cloudmesh_client.cloud.stack import SanityCheckError
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.shell.command import (CloudPluginCommand, PluginCommand,
    command)
from cloudmesh_client.shell.console import Console


class Command(object):

    def start(self, count=3, addons=None, flavor=None, image=None, username=None):
        """Start a hadoop cluster

        :param int count: number of nodes to use (minimum of 3)
        :param list(str) addons: names of addons to deploy as well
        :param str flavor: instance flavor
        :param str image: image name
        :param str username: login user name
        """

        clustercmd = ClusterCommand()
        cluster = clustercmd.create(
            count=count,
            username=username,
            flavor=flavor,
            image=image,
        )

        stackcmd = StackCommand()

        addons = addons or []
        playbooks = ['play-hadoop.yml'] + \
                    [os.path.join('addons', name) for name in addons]

        stackcmd.init(
            username=username,
            playbooks=playbooks,
            ips=clustercmd.get('floating_ip', cluster=cluster),
        )

        try:
            stackcmd.deploy()
        except SanityCheckError:
            return None

    def list(self):
        """List the known deployments

        :returns: 
        :rtype: 

        """

        Console.error('hadoop.list not implemented')
        raise NotImplementedError()

    def switch(self, name):
        """Switch active deployments

        :param str name: name of deployment to switch to
        :returns: 
        :rtype: 

        """

        Console.error('hadoop.switch not implemented')
        raise NotImplementedError()

    def delete(self, names, all=False):
        """Delete deployments.

        If no names are specified, delete the currently active
        deployment.

        :param list names: names of deployments to delete
        :param bool all: delete all deployments
        :returns: 
        :rtype:

        """

        Console.error('hadoop.delete not implemented')
        raise NotImplementedError()


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
             hadoop start [-f NAME] [-i NAME] [-u NAME] [COUNT] [ADDON]...
             hadoop list
             hadoop switch NAME
             hadoop delete [-a] [NAME]...

           Arguments:

             COUNT
             ADDON
             NAME

           Options:

             -a --all
             -f --flavor=NAME
             -i --image=NAME
             -u --username=NAME

        """

        arguments = dotdict(arguments)
        cmd = Command()

        if arguments.start:

            cmd.start(
                count=arguments.COUNT or 3,
                addons=arguments.ADDON,
                flavor=arguments['--flavor'],
                image=arguments['--image'],
                username=arguments['--username'],
            )

        elif arguments.list:

            cmd.list()

        elif arguments.switch:

            cmd.switch(arguments.NAME)

        elif arguments.delete:

            cmd.delete(arguments.NAME, all=arguments['--all'])

