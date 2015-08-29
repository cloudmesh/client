#!/usr/bin/env python

import os
import sys

OS_AUTH_URL = os.environ['OS_AUTH_URL']
OS_USERNAME = os.environ['OS_USERNAME']
OS_PASSWORD = os.environ['OS_PASSWORD']
OS_TENANT_NAME = os.environ['OS_TENANT_NAME']
OS_CACERT = os.environ['OS_CACERT']
VERSION = 2

COMMANDARG = sys.argv[1]
SERVER_ID = sys.argv[2]

from novaclient import client
nova = client.Client(VERSION, OS_USERNAME, OS_PASSWORD, OS_TENANT_NAME, OS_AUTH_URL, OS_CACERT)

print "Following are the running servers"
servers = nova.servers.list()
print servers

if COMMANDARG != "create":
    server = nova.servers.get(SERVER_ID)

if COMMANDARG == "create":
    INST_NAME = sys.argv[2]
    INST_IMAGE = sys.argv[3]
    image = nova.images.find(id=INST_IMAGE)
    INST_FLAVOR = sys.argv[4]
    flavor = nova.flavors.find(id=INST_FLAVOR)
    nova.servers.create(INST_NAME, INST_IMAGE, INST_FLAVOR)
    print "Machine creation issued"

elif COMMANDARG == "start":
    server.start()
    print "%s start issued" %server

elif COMMANDARG == "stop":
    server.stop()
    print "%s stop issued" %server

elif COMMANDARG == "delete":
    server.delete()
    print "%s delete issued" %server