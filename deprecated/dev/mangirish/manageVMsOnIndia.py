#!/usr/bin/env python

import os
import sys
from novaclient import client

# TODO: make it possible that we read from ConfigDict ~/.cloudmesh.yaml as we have more than one cloud
# TODO: possibly we need to think about an option to read form os.environm as alternative

OS_AUTH_URL = os.environ['OS_AUTH_URL']
OS_USERNAME = os.environ['OS_USERNAME']
OS_PASSWORD = os.environ['OS_PASSWORD']
OS_TENANT_NAME = os.environ['OS_TENANT_NAME']
OS_CACERT = os.environ['OS_CACERT']
VERSION = 2

# Use docopt
COMMANDARG = sys.argv[1]
SERVER_ID = sys.argv[2]

nova = client.Client(VERSION, OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME, OS_AUTH_URL, OS_CACERT)

print("Following are the running servers")
servers = nova.servers.list()
print(servers)

# TODO: make this a class and use the Bar as example so we can integrate into the shell
# TODO: move that to plugins in the cloudmesh_client

if COMMANDARG != "create":
    server = nova.servers.get(SERVER_ID)

if COMMANDARG == "create":
    INST_NAME = sys.argv[2]
    INST_IMAGE = sys.argv[3]
    image = nova.images.find(id=INST_IMAGE)
    INST_FLAVOR = sys.argv[4]
    flavor = nova.flavors.find(id=INST_FLAVOR)
    nova.servers.create(INST_NAME, INST_IMAGE, INST_FLAVOR)
    print ("Machine creation issued")

elif COMMANDARG == "start":
    server.start()
    print ("{0} start issued".format(server))

elif COMMANDARG == "stop":
    server.stop()
    print ("{0} stop issued".format(server))

elif COMMANDARG == "delete":
    server.delete()
    print ("{0} delete issued".format(server))
