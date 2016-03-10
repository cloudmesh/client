from __future__ import print_function
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security
import re
from cloudmesh_client.common.ConfigDict import ConfigDict
from time import sleep
from pprint import pprint


cloud = "chameleon-ec2"
config = ConfigDict("cloudmesh.yaml")
credential = config['cloudmesh']['clouds'][cloud]['credentials']
clouddefault = config['cloudmesh']['clouds'][cloud]['default']
# pprint(dict(credential))

auth_url = credential["EC2_URL"]

data = re.match(r'^http[s]?://(.+):([0-9]+)/([a-zA-Z/]*)',
                auth_url,
                re.M | re.I)
host, port, path = data.group(1),data.group(2),data.group(3)
print("host: " + host)
print("port: " + port)
print("path: " + path)

extra_args = {'path': path}
cls = get_driver(Provider.EC2_US_EAST)
driver = cls(
    credential['EC2_ACCESS_KEY'],
    credential['EC2_SECRET_KEY'],
    host=host,
    port=port,
    **extra_args)

print ("DRIVER", driver)

pprint(dict(credential))

# list VMs
nodes = driver.list_nodes()
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
print (nodes)

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
print (nodes)

# remove it from the node

# delete the ip

# delete vm
node.destroy()
