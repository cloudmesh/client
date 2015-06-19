from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security

from cloudmesh_common.ConfigDict import ConfigDict
from cloudmesh_common.ConfigDict import Config
from time import sleep
from pprint import pprint

# AWS to load EC2 from US_EAST
cls = get_driver(Provider.EC2_US_EAST)

# get cloud credential from yaml file
confd = ConfigDict("cloudmesh.yaml")
cloudcred = confd['cloudmesh']['clouds']['aws']['credentials']
clouddefault = confd['cloudmesh']['clouds']['aws']['default']

pprint(cloudcred)

# set path to cacert and enable ssl connection
#libcloud.security.CA_CERTS_PATH = [Config.path_expand(cloudcred['OS_CACERT'])]
#libcloud.security.VERIFY_SSL_CERT = True

#auth_url = "%s/tokens/" % cloudcred['OS_AUTH_URL']

# AWS needs two values for authentication
driver = cls(cloudcred['EC2_ACCESS_KEY'],
             cloudcred['EC2_SECRET_KEY'])


# list VMs
nodes = driver.list_nodes()
print nodes

# THIS FUNCTION TAKES TIME TO LOAD 40K+ IMAGES
# obtain available images
images = driver.list_images()
# print images

# sizes/flavors
sizes = driver.list_sizes()
# print sizes

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
