#!/usr/bin/env python

"""USAGE:
    launchCluster.py <NUMBER_OF_WORKERS> <CLOUD_NAME>

    Spawns a master and worker cluster on the target cloud,
    indicated by CLOUD_NAME

    NUMBER_OF_WORKERS: Any integer number
    CLOUD_NAME: vagrant | india | docker | none

    In case of CLOUD_NAME='none' cluster specification would be generated,
    however the actual machine spawning would be skipped.

    Examples:-
      ./launchCluster.py 1 vagrant
      ./launchCluster.py 10 india
"""
# TODO: introduce class and than use it for the command.
# TODO: use the @command and the Bar example for the plugin
# TODO: move the command plugin into the plugins dir when finished
#
# class launcher(object):
#  "abstarct class for laounching"
#  def configure ...
#  def start
#  def stop
#  def status
#
# TODO: create class for managing spec file
#
import os
import sys
import yaml
from docopt import docopt

version = '1.0.0cr2'
if sys.argv[1] == "--help":
    print(docopt(__doc__, version=version))

number_of_workers = sys.argv[1]
cloud = sys.argv[2]

# TODO: Check for null values

spec_file = "spec.yaml"

workers_ip_subnet_bytes = "10.10.10"
workers_init_offset = 4
workers_final_offset = workers_init_offset + int(number_of_workers)

specFile = open(spec_file, 'a')

# Empty the spec yaml
specFile.seek(0)
specFile.truncate()

# Create Master Spec
specFile.write("master:\n")
specFile.write("  - name: master\n")
specFile.write("    hostname: \"master\"\n")
specFile.write("    ipaddress: \"10.10.10.3\"\n")

# Create Workers specs
specFile.write("worker:\n")
for x in range(workers_init_offset, workers_final_offset, 1):
    specFile.write("  - name: worker00%d\n" % (x))
    specFile.write("    hostname: \"worker00%d\"\n" % (x))
    specFile.write("    ipaddress: \"10.10.10.%d\"\n" % (x))

specFile.close()


def spawn_vm_cluster_on_india_cloud():
    machine_image_id = "f63a996c-ea69-4a56-830e-c190bca2f828"
    machine_flavor_id = "1"

    with open(spec_file, "r") as stream:
        specStream = yaml.load(stream)
    print(specStream['master'][0]['hostname'])
    # TODO: Check if machine already exists
    # Spawn master VM
    commandString = "./manageVMsOnIndia.py create {0} {1} {2}".format(specStream['master'][0]['hostname'],
                                                                      machine_image_id, machine_flavor_id)
    # print commandString
    os.system(commandString)

    # Spawn workers
    for worker_index in range(len(specStream['worker'])):
        # TODO: Check if machine already exists
        commandString = "./manageVMsOnIndia.py create {0} {1} {2}".format(
            specStream['worker'][worker_index]['hostname'],
            machine_image_id,
            machine_flavor_id)
        # print commandString
        os.system(commandString)


if cloud == "vagrant":
    print("Issuing vagrant up")
    os.system("sudo vagrant up")
elif cloud == "india":
    print("Issuing vm start on India")
    spawn_vm_cluster_on_india_cloud()
elif cloud == "docker":
    print("TO BE IMPLEMENTED")
elif cloud == "none":
    sys.exit(0)
else:
    print(docopt(__doc__, version=version))
