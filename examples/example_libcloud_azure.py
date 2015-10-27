from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security

from cloudmesh_client.common.ConfigDict import ConfigDict
#from cloudmesh_client.common import Config
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

# obtain available images
images = driver.list()
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
# Cloud Service is required prior to start a VM
cloudname = name
# Return type:  bool
boolean = driver.ex_create_cloud_service(cloudname, clouddefault['location'])
# Wait 10 seconds until Cloud Service is ready
sleep(10)
node = driver.create_node(name=name, image=image, size=size)

# check if the new VM is in the list
nodes = driver.list_nodes(cloudname)
print nodes

for node in nodes:
    for public_ip in node.public_ips:
        print node.name +  ": " + public_ip

# Return type:  bool
# Terminate VM
boolean = driver.destroy_node(node, cloudname)
# Delete Cloud Service
boolean = ex_destroy_cloud_service(cloudname)
