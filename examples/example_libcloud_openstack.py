from __future__ import print_function
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.ConfigDict import Config
from time import sleep
from pprint import pprint

OpenStack = get_driver(Provider.OPENSTACK)

# get cloud credential from yaml file
config = ConfigDict("cloudmesh.yaml")
credential = config['cloudmesh']['clouds']['kilo']['credentials']

pprint(dict(credential))

# set path to cacert and enable ssl connection
# libcloud.security.CA_CERTS_PATH = [Config.path_expand(credential['OS_CACERT'])]
# libcloud.security.VERIFY_SSL_CERT = True

auth_url = "%s/tokens/" % credential['OS_AUTH_URL']
auth_url = auth_url.split("/v3")[0]

print (auth_url)


driver = OpenStack(
    credential['OS_USERNAME'],
    credential['OS_PASSWORD'],
    ex_force_auth_version='3.x_password',
    ex_force_auth_url=auth_url,
    # ex_force_service_type='compute',
    ex_force_service_region='RegionOne',
    ex_tenant_name=credential['OS_TENANT_NAME'])


# list VMs
nodes = driver.list_nodes()
pprint (nodes)

# obtain available images
images = driver.list_images()
pprint (images)

# sizes/flavors
sizes = driver.list_sizes()
pprint (sizes)

# specify flavor and image
myflavor = 'm1.small'
myimage = 'Ubuntu-Server-14.04-LTS'


size = [s for s in sizes if s.id == myflavor][0]
image = [i for i in images if i.name == myimage][0]



pprint (driver.ex_list_floating_ip_pools())
print("NNNN")


networks= driver.ex_list_networks()
pprint (networks)



mynetworkname = "%s-net" % credential['OS_TENANT_NAME']
mynetwork = [i for i in networks if i.name == mynetworkname][0]

# launch a new VM
name = "{:}-libcloud".format(credential['OS_USERNAME'])
node = driver.create_node(name=name, image=image, size=size, networks=[mynetwork])

# check if the new VM is in the list
nodes = driver.list_nodes()
pprint (nodes)

# wait the node to be ready before assigning public IP
sleep(10)

# public IPs
# get the first pool - public by default
pool = driver.ex_list_floating_ip_pools()[0]

# create an ip in the pool
floating_ip = pool.create_floating_ip()

# get the node
mynodeid = [n for n in nodes if n.name == name][0].id
# print mynodeid
node = driver.ex_get_node_details(mynodeid)
# print node

# attach the ip to the node
driver.ex_attach_floating_ip_to_node(node, floating_ip)

# check updated VMs list to see if public ip is assigned
nodes = driver.list_nodes()
pprint (nodes)

# remove it from the node
driver.ex_detach_floating_ip_from_node(node, floating_ip)

# delete the ip
floating_ip.delete()
