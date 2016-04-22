from __future__ import print_function

import os
from pprint import pprint

from cloudmesh_client.common.ConfigDict import path_expand
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.ssh_config import ssh_config
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.common.util import banner
from cloudmesh_client.shell.command import PluginCommand, ShellPluginCommand, \
    CometPluginCommand
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console


class SecureShellCommand(PluginCommand, ShellPluginCommand, CometPluginCommand):
    # def activate_cm_shell_ssh(self):

    topics = {"ssh": "security"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command ssh")

    # noinspection PyUnusedLocal
    @command
    def do_ssh(self, args, arguments):
        """
        ::

            Usage:
                ssh table
                ssh list [--format=FORMAT]
                ssh cat
                ssh register NAME PARAMETERS
                ssh ARGUMENTS


            conducts a ssh login on a machine while using a set of
            registered machines specified in ~/.ssh/config

            Arguments:

              NAME        Name or ip of the machine to log in
              list        Lists the machines that are registered and
                          the commands to login to them
              PARAMETERS  Register te resource and add the given
                          parameters to the ssh config file.  if the
                          resoource exists, it will be overwritten. The
                          information will be written in /.ssh/config

            Options:

               -v       verbose mode
               --format=FORMAT   the format in which this list is given
                                 formats incluse table, json, yaml, dict
                                 [default: table]

               --user=USER       overwrites the username that is
                                 specified in ~/.ssh/config

               --key=KEY         The keyname as defined in the key list
                                 or a location that contains a pblic key

            Description:

                ssh list
                    lists the hostsnames  that are present in the
                    ~/.ssh/config file

                ssh cat
                    prints the ~/.ssh/config file

                ssh table
                    prints contents of the ~/.ssh/config file in table format

                ssh register NAME PARAMETERS
                    registers a host i ~/.ssh/config file
                    Parameters are attribute=value pairs
                    Note: Note yet implemented

                ssh ARGUMENTS
                    executes the ssh command with the given arguments
                    Example:
                        ssh myhost

                            conducts an ssh login to myhost if it is defined in
                            ~/.ssh/config file
        """
        # pprint(arguments)

        def read(filename=None):
            if filename is None:
                filename = "~/.ssh/config"
            with open(path_expand("~/.ssh/config"), "r") as f:
                content = f.readlines()
            return "".join(content)

        if arguments["list"]:

            output_format = arguments["--format"]
            banner('List SSH config hosts')
            hosts = ssh_config()
            for host in hosts.list():
                print(host)

        elif arguments["table"]:

            content = read(filename="~/.ssh/config").split("\n")

            entries = [
            ]

            def empty():
                return {
                    "host": None,
                    "hostname": None,
                    "user": None,
                    "proxycommand": None,
                    "serveraliveinterval": None,
                    "localforward": None,
                    "forwardx11": None
                }

            entry = empty()
            for line in content:
                line = line.strip()
                if line.startswith("#"):
                    pass
                elif line.strip() == "":
                    pass
                elif "Host " in line:
                    hostname = line.strip().split("Host")[1]
                    entry["host"] = hostname.strip()
                    if entry is not None:
                        entries.append(entry)
                    entry = empty()
                else:
                    attribute, value = line.strip().split(" ", 1)
                    entry[attribute.lower()] = value.strip()

            pprint(entries)
            order = ["host",
                     "hostname",
                     "user",
                     "proxycommand",
                     "serveraliveinterval",
                     "localforward",
                     "forwardx11"]

            print(Printer.list(entries, order=order))

        elif arguments["cat"]:

            print(read(filename="~/.ssh/config"))

        elif arguments["register"]:

            name = arguments["NAME"]
            parameters = arguments["PARAMETERS"]
            Console.ok('register {} {}'.format(name, parameters))
            TODO.implement("Not implemented")

        else:  # ssh ARGUMENTS...

            args = arguments["ARGUMENTS"]
            os.system("ssh {}".format(args))
            return ""

        return ""

