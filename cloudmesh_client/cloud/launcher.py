from __future__ import print_function

from cloudmesh_client.common import Printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.ListResource import ListResource
from pprint import pprint
import os
import subprocess


class Launcher(ListResource):
    # cm = CloudmeshDatabase()

    def get_command_output(self, action):

        # Running command
        proc = subprocess.Popen(['echo', 'Running ' + action + ' on ' + os.environ["HOSTNAME"]], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        output, err = proc.communicate()
        return output

    def info(self, **kwargs):
        return self.get_command_output("info")

    def list(self, **kwargs):
        return self.get_command_output("list")

    def run(self, **kwargs):
        return self.get_command_output("run")

    def resume(self, **kwargs):
        return self.get_command_output("resume")

    def suspend(self, **kwargs):
        return self.get_command_output("suspend")

    def kill(self, **kwargs):
        return self.get_command_output("kill")

    def details(self, **kwargs):
        return self.get_command_output("details")

    def clear(self, **kwargs):
        return self.get_command_output("clear")

    def refresh(self, **kwargs):
        return self.get_command_output("refresh")
