import os
from novaclient.client import Client
from novaclient.v2.quotas import QuotaSetManager
from novaclient.v2.limits import LimitsManager
from cloudmesh_base.util import path_expand
from cloudmesh_base.ConfigDict import ConfigDict
import sys
import json
from pprint import pprint
from cloudmesh_base.MultiKeyDict import MultiKeyDict

# disable security warning for old certs
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()



def get_nova_credentials(kind="yaml", cloud=None):

    d = {}
    if kind in ["env"]:
        d['version'] = '2'
        d['username'] = os.environ['OS_USERNAME']
        d['api_key'] = os.environ['OS_PASSWORD']
        d['auth_url'] = os.environ['OS_AUTH_URL']
        d['project_id'] = os.environ['OS_TENANT_NAME']
        d['cacert'] = path_expand(os.environ['OS_CACERT'])
    elif kind in ["yaml"]:
        if cloud is None:
            raise Exception("cloud not specified")
        config = dict(ConfigDict(filename="~/.cloudmesh/cloudmesh.yaml")["cloudmesh"]["clouds"][cloud])
        cred = dict(config["credentials"])
        d['version'] = '2'
        d['username'] = cred['OS_USERNAME']
        d['api_key'] = cred['OS_PASSWORD']
        d['auth_url'] = cred['OS_AUTH_URL']
        d['project_id'] = cred['OS_TENANT_NAME']
        if 'OS_CACERT' in cred:
            d['cacert'] = path_expand(cred['OS_CACERT'])
    else:
        raise Exception ("unsupported kind: " + kind)
    return d

'''
openstack_client_keys  = [
    ["username", "OS_USERNAME"],
    ["password", "OS_PASSWORD",  "api_key"],
    ["auth_url", "OS_AUTH_URL"],
    ["tenant_id", "OS_TENANT_ID"],
    ["region_name", "OS_REGION_NAME"],
    ["cacert", "OS_CACERT"],
    ["version", "OS_COMPUTE_API_VERSION"],
    ["project_id", "OS_TENANT_NAME"],
    ["os_version", "OS_VERSION"]
]


m = MultiKeyDict(openstack_client_keys)
m["username"] = "gregor"
print ("U", m["username"])
print ("U", m["OS_USERNAME"])

m["OS_PASSWORD"] = "1234"
print("P", m["password"])
print("P", m["OS_PASSWORD"])

# m.set(get_nova_credentials_v2())
'''


class CloudMesh(object):

    def __init__(self):
        self.config = dict(ConfigDict(filename="~/.cloudmesh/cloudmesh.yaml")["cloudmesh"]["clouds"])
        self.client = {}

    def cloud_username(self, cloud):
        if self.cloud_type(cloud) == "openstack":
            return self.config[cloud]["credentials"]["OS_USERNAME"]
        else:
            raise Exception("username for this cloud type not defined")

    def cloud_project(self, cloud):
        if self.cloud_type(cloud) == "openstack":
            return self.config[cloud]["credentials"]["OS_TENANT_NAME"]
        else:
            raise Exception("username for this cloud type not defined")


    def cloud_type(self, cloud):
        return self.config[cloud]["cm_type"]

    def credentials(self, cloud):
        if self.cloud_type(cloud) == "openstack":
            cred = get_nova_credentials(cloud=cloud)
            return dict(cred)
        else:
            print("not supported cloud type")

    def authenticate(self, cloud):
        credential = self.credentials(cloud)
        self.client[cloud] = Client(**credential)

    def list(self, kind, cloud=None):

        result = {cloud: {}}

        def insert(objects):
            for i in objects:
                result[cloud][i.name] = i.__dict__


        if self.cloud_type(cloud) == "openstack":
            if kind in ["server"]:
                objects = self.client[cloud].servers.list()
                insert(objects)
            elif kind in ["flavor"]:
                objects = self.client[cloud].flavors.list()
                insert(objects)
            elif kind in ["image"]:
                objects = self.client[cloud].images.list()
                insert(objects)
            elif kind in ["key"]:
                objects = self.client[cloud].keypairs.list()
                insert(objects)
            elif kind in ["limit"]:
                objects = self.client[cloud].limits.get()
                result[cloud]["limits"] = objects.__dict__["_info"]
            elif kind in ["quota"]:
                # username = self.cloud_username(cloud)
                project = self.cloud_project(cloud)
                # get is permission denied on india so we use by default the default
                # objects = self.client[cloud].quotas.get(username, project)
                objects = self.client[cloud].quotas.defaults(project)
                result[cloud]["quota"] = objects.__dict__["_info"]

        else:
            raise Exception("unsupported kind or cloud: " + kind + " " + str(cloud))
        return result

    def key_add(self, cloud, name, filename):
        keyfile = path_expand(filename)
        if self.cloud_type(cloud) == "openstack":
            with open(os.path.expanduser(filename), 'r') as public_key:
        #try:
                self.client[cloud].keypairs.create(name=name, public_key=public_key.read())
        # except Exception:
        #    print ("key already exists")

        else:
            raise Exception("unsupported kind or cloud: " + kind + " " + str(cloud))


#mesh = Mesh()

# cred = mesh.credentials("india")
# print("CCC", cred)


# credential = get_nova_credentials(cloud="india")
# pprint (credential)

# credential = get_nova_credentials(kind="env")
# pprint (credential)


# nova_client = Client(**credential)

# print(nova_client.servers.list())

# credential = get_nova_credentials(cloud="chameleon")

#pprint (credential)

# credential = get_nova_credentials(kind="env")
# pprint (credential)


# nova_client = Client(**credential)

# print(nova_client.servers.list())

print("===================")
cm = CloudMesh()

clouds = ["india", "chameleon"]

kinds = ["limit", "quota", "server", "flavor", "image"]

clouds = ["india"]

kinds = ["limit"]

for cloud in clouds:
    cm.authenticate(cloud)

# l = cm.list("key", cloud="india")
# pprint (l)
for cloud in clouds:
    for kind in kinds:
        l = cm.list(kind, cloud=cloud)
        pprint (l)

cm.key_add('india', "gregor-key", "~/.ssh/id_rsa.pub")


'''
export OS_USERNAME=username
export OS_PASSWORD=password
export OS_TENANT_NAME=a
export OS_AUTH_URL=https://identityHost:portNumber/v2.0
export OS_TENANT_ID=tenantIDString
export OS_REGION_NAME=regionName
export OS_CACERT=/path/to/caceratFile
export OS_COMPUTE_API_VERSION=2

username (str) - Username
api_key (str) - API Key
project_id (str) - Project ID
auth_url (str) - Auth URL
insecure (bool) - Allow insecure
timeout (float) - API timeout, None or 0 disables
proxy_tenant_id (str) - Tenant ID
proxy_token (str) - Proxy Token
region_name (str) - Region Name
endpoint_type (str) - Endpoint Type
extensions (str) - Exensions
service_type (str) - Service Type
service_name (str) - Service Name
volume_service_name (str) - Volume Service Name
timings (bool) - Timings
bypass_url (str) - Bypass URL
os_cache (bool) - OS cache
no_cache (bool) - No cache
http_log_debug (bool) - Enable debugging for HTTP connections
auth_system (str) - Auth system
auth_plugin (str) - Auth plugin
auth_token (str) - Auth token
cacert (str) - cacert
tenant_id (str) - Tenant ID
user_id (str) - User ID
connection_pool (bool) - Use a connection pool
session (str) - Session
auth (str) - Auth
'''


