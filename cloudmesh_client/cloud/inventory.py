from __future__ import print_function

import os.path
import sys

import hostlist
import yaml

from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.util import banner
from cloudmesh_client.shell.console import Console


class Inventory(ListResource):
    def info(self):
        banner("Configuration")
        Console.ok('Object Attibutes: {:}'.format(', '.join(self.order)))
        Console.ok('Objects: {:}'.format(len(self.data)))
        Console.ok('Configuration File: {:}'.format(self.config_filename))
        Console.ok('Configuration:')

        print(self.config)

        try:
            config = ConfigDict(filename=self.config_filename)
        except Exception as e:
            Console.error("Problem reading the yaml file {:}".format(
                self.config_filename), traceflag=False)
            Console.error("Please check if the file exists or is empty", traceflag=False)
            Console.error(e.message)

        banner("")

    def __init__(self):

        self.order = [
            "host",
            "cluster",
            "label",
            "service",
            "ip",
            "project",
            "owners",
            "comment"]

        self.entry = {}
        for key in self.order:
            self.entry[key] = ""

        self.data = {}

        self.config_filename = "cloudmesh.yaml"
        self.config = ConfigDict(filename=self.config_filename)

        self.datafile = self.config["cloudmesh.system.data"]
        self.read(self.datafile)

    def read(self, filename=None, format="yaml"):
        if filename is None:
            filename = self.datafile

        if not os.path.isfile(filename):
            self.save(filename)
        stream = open(filename, "r")
        self.data = yaml.safe_load(stream)
        stream.close()

    def save(self, filename=None, format="yaml"):
        if filename is None:
            filename = self.datafile
        with open(filename, 'w') as yaml_file:
            yaml_file.write(self.list(format=format))

    def add(self, **kwargs):

        if "host" not in kwargs:
            print("ERROR no id specified")
            sys.exit(1)

        hosts = hostlist.expand_hostlist(kwargs['host'])

        for host in hosts:
            if host in self.data:
                entry = self.data[host]
            else:
                entry = dict(self.entry)
                self.data[host] = entry
            for key, value in kwargs.items():
                entry[key] = value
            entry['host'] = host
            for attribute in entry:
                self.data[host][attribute] = entry[attribute]
        self.save()

    def list(self, format='dict', sort_keys=True, order=None):
        if order is None:
            order = self.order
        return Printer.write(self.data,
                             order=order,
                             output=format,
                             sort_keys=sort_keys)

    def _str(self, data, with_empty=False):
        print
        for key in data:
            if self.data[key] is '' or self.data[key] is None:
                pass
            else:
                print(self.data[key])


# noinspection PyBroadException,PyPep8Naming
class command_system(object):
    @classmethod
    def status(cls, host):
        msg = "Unknown host"
        try:
            msg = Shell.ping("-c", "1", host)
        except:
            pass
        if "1 packets transmitted, 1 packets received" in msg:
            return True
        elif "Unknown host" in msg:
            return False
        else:
            return False


if __name__ == "__main__":
    i = Inventory()
    banner("Info")
    i.info()

    banner("changing values")
    i.add(host="i1", cluster="kilo", label="india")
    i.add(host="i2", cluster="kilo", label="gregor")
    i.add(host="d[1-4]", cluster="kilo", label="delta")

    banner("saving")
    i.save()

    for output in ['dict', 'yaml', 'csv', 'table']:
        banner(output)
        print(i.list(format=output))

    banner("reading")
    n = Inventory()
    n.read()
    print(n.list('table'))
    n.save()
