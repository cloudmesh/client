from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security

from cloudmesh_client.cloudmesh_common import ConfigDict
from cloudmesh_client.cloudmesh_common import Config
from time import sleep
from pprint import pprint

cls = get_driver(Provider.AZURE)

# get cloud credential from yaml file
confd = ConfigDict("cloudmesh.yaml")
cloudcred = confd['cloudmesh']['clouds']['azure']['credentials']
clouddefault = confd['cloudmesh']['clouds']['azure']['default']

pprint(cloudcred)

driver = cls(subscription_id=cloudcred['subscriptionid'],
             key_file=cloudcred['managementcertfile'])

# list VMs
nodes = driver.list_nodes()
print nodes

# obtain available images
images = driver.list_images()
# print images

# sizes/flavors
sizes = driver.list_sizes()
# print sizes

# specify flavor and image
myflavor = clouddefault['flavor']
myimage = clouddefault['image']

size = [s for s in sizes if s.id == myflavor][0]
image = [i for i in images if i.id == myimage][0]

# launch a new VM
# Username is not available in azure
# Probably need to use 'uid' from Profile?
name = "{:}-libcloud".format("aws")

node = driver.create_node(name=name, image=image, size=size)

# check if the new VM is in the list
nodes = driver.list_nodes()
print nodes

# wait the node to be ready before assigning public IP
sleep(10)

# public IPs
# get the first pool - public by default

# create an ip in the pool

# check updated VMs list to see if public ip is assigned
nodes = driver.list_nodes()
print nodes
