from __future__ import print_function

#from cloudmesh_client.common import Printer
#from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
#from cloudmesh_client.cloud.ListResource import ListResource
#from pprint import pprint
import os
import subprocess


class Launcher():
    # cm = CloudmeshDatabase()

    def list(self, **kwargs):
        proc = subprocess.Popen(['echo', 'Running list on ' + os.environ["HOSTNAME"]], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        output, err = proc.communicate()
        return output

    def run(self, **kwargs):
        proc = subprocess.Popen(['echo', 'Running run on ' + os.environ["HOSTNAME"]], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        output, err = proc.communicate()
        return output

    def resume(self, **kwargs):
        proc = subprocess.Popen(['echo', 'Running resume on ' + os.environ["HOSTNAME"]], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        output, err = proc.communicate()
        return output

    def suspend(self, **kwargs):
        proc = subprocess.Popen(['echo', 'Running suspend on ' + os.environ["HOSTNAME"]], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        output, err = proc.communicate()
        return output

    def kill(self, **kwargs):
        proc = subprocess.Popen(['echo', 'Running kill on ' + os.environ["HOSTNAME"]], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        output, err = proc.communicate()
        return output

    def details(self, **kwargs):
        proc = subprocess.Popen(['echo', 'Running details on ' + os.environ["HOSTNAME"]], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        output, err = proc.communicate()
        return output

    def clear(self, **kwargs):
        proc = subprocess.Popen(['echo', 'Running clear on ' + os.environ["HOSTNAME"]], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        output, err = proc.communicate()
        return output

    def refresh(self, **kwargs):
        proc = subprocess.Popen(['echo', 'Running refresh on ' + os.environ["HOSTNAME"]], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        output, err = proc.communicate()
        return output


launch = Launcher()

launch.list()