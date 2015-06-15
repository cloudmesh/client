from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security

from cloudmesh_common.ConfigDict import ConfigDict

OpenStack = get_driver(Provider.OPENSTACK)

# get cloud credential from yaml file
confd = ConfigDict("cloudmesh.yaml")
cloudcred = confd['cloudmesh']['clouds']['india']['credentials']

# set path to cacert and enable ssl connection
libcloud.security.CA_CERTS_PATH = [cloudcred['OS_CACERT']]
libcloud.security.VERIFY_SSL_CERT = True

auth_url = "%s/tokens/" % cloudcred['OS_AUTH_URL']

driver = OpenStack(cloudcred['OS_USERNAME'], cloudcred['OS_PASSWORD'],
                   ex_force_auth_url=auth_url,
                   ex_tenant_name=cloudcred['OS_TENANT_NAME'],
                   ex_force_auth_version='2.0_password',
                   ex_force_service_region='regionOne')

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
myflavor = 'm1.small'
myimage = 'futuresystems/ubuntu-14.04'

size = [s for s in sizes if s.name == myflavor][0]
image = [i for i in images if i.name == myimage][0]

# launch a new VM
node = driver.create_node(name='node from libcloud', image=image, size=size)

# check if the new VM is in the list
nodes = driver.list_nodes()
print nodes

'''
# public IPs
# get the first pool - public by default
pool = driver.ex_list_floating_ip_pools()[0]

# create an ip in the pool
floating_ip = pool.create_floating_ip()

# get the node, note: change the node id to the some id you have
node = driver.ex_get_node_details('922a4381-a18c-487f-b816-cc31c9060853')

# attach the ip to the node
driver.ex_attach_floating_ip_to_node(node, floating_ip)

# remove it from the node
driver.ex_detach_floating_ip_from_node(node, floating_ip)

# delete the ip
floating_ip.delete()
'''