from __future__ import absolute_import, print_function

from .ClusterCommand2 import Cluster2Command
from .StackCommand import StackCommand
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.shell.command import (CloudPluginCommand, PluginCommand,
    command)
from cloudmesh_client.shell.console import Console


class HadoopCommand(PluginCommand, CloudPluginCommand):

    topics = {"hadoop": "cluster"}

    def start(self, count=3, addons=None, flavor=None, image=None, user=None):
        """Start a hadoop cluster

        :param int count: number of nodes to use (minimum of 3)
        :param list(str) addons: names of addons to deploy as well
        :param str flavor: instance flavor
        :param str image: image name
        :param str user: login user name
        """

        Console.error('hadoop.start not implemented')
        raise NotImplementedError()

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
             -u --user=NAME

        """

        arguments = dotdict(arguments)

        if arguments.start:

            self.start(count=arguments.COUNT, addons=arguments.ADDON)

        elif arguments.list:

            self.list()

        elif arguments.switch:

            self.switch(arguments.NAME)

        elif arguments.delete:

            self.delete(arguments.NAME, all=arguments['--all'])

