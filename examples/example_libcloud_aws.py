from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security

from cloudmesh_client.common.ConfigDict import ConfigDict
from time import sleep
from pprint import pprint

# AWS to load EC2 from US_EAST
cls = get_driver(Provider.EC2_US_EAST)

# get cloud credential from yaml file
confd = ConfigDict("cloudmesh.yaml")
cloudcred = confd['cloudmesh']['clouds']['aws']['credentials']
clouddefault = confd['cloudmesh']['clouds']['aws']['default']

PROXY_URL_NO_AUTH_1 = 'https://openstack.tacc.chameleoncloud.org:8773/services/Cloud'

pprint(cloudcred)
extra_args= {'path' : '/services/Cloud'}

# AWS needs two values for authentication
driver = cls(cloudcred['EC2_ACCESS_KEY'],
             cloudcred['EC2_SECRET_KEY'], host='openstack.tacc.chameleoncloud.org', port=8773, **extra_args)

# list VMs
print 'Printing nodes'
nodes = driver.list_nodes()
for anode in nodes:
    print anode
print 'DONE Printing nodes'
#print nodes

# THIS FUNCTION TAKES TIME TO LOAD 40K+ IMAGES
# obtain available images
images = driver.list_images()
#print images[0]

# sizes/flavors
sizes = driver.list_sizes()
#print sizes

# specify flavor and image
myflavor = clouddefault['flavor']
myimage = clouddefault['image']

# Changed "name" -> "id" (diff from openstack)
size = [s for s in sizes if s.id == myflavor][0]
image = [i for i in images if i.id == myimage][0]

# launch a new VM
name = "{:}-libcloud".format(cloudcred['userid'])
node = driver.create_node(name=name, image=image, size=size)

# check if the new VM is in the list
nodes = driver.list_nodes()
print nodes

# wait the node to be ready before assigning public IP
sleep(10)

# public IPs
# get the first pool - public by default
# create an ip in the pool
elastic_ip = driver.ex_allocate_address()

# attach the ip to the node
driver.ex_associate_address_with_node(node, elastic_ip)

# check updated VMs list to see if public ip is assigned
nodes = driver.list_nodes()
print nodes

# remove it from the node

# delete the ip

# delete vm
node.destroy()
