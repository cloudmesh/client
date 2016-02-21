import os
from novaclient import exceptions 
from novaclient.client import Client
from novaclient.v2.quotas import QuotaSetManager
from novaclient.v2.limits import LimitsManager
from cloudmesh_client.util import path_expand
from cloudmesh_client.common.ConfigDict import ConfigDict
import sys
import json
from pprint import pprint
# from cloudmesh_client.MultiKeyDict import MultiKeyDict

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

    # #############################################
    # KEY LIST
    # #############################################

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
                result[cloud]["key"] = {}
                for i in objects:
                    result[cloud]["key"][i.name] = i.__dict__["_info"]["keypair"]
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


    # #############################################
    # IMAGE MANAGEMENT
    # #############################################
    def image_get(self, name, cloud=None):
        pass
       
    # #############################################
    # FLAVOR MANAGEMENT
    # #############################################
    def flavor_get(self, name, cloud=None):
        pass
       
    # #############################################
    # SEVER MANAGEMENT
    # #############################################

    def vm_create(self, name, flavor, image, secgroup, keypair, meta, userdata, cloud=None):
	self.client[cloud].servers.create(name, image, flavor, meta=meta,
                                          security_groups=secgroup, key_name=keypair, userdata=userdata)
        # TBD

    def vm_delete(self, name, cloud):
        self.client[cloud].servers.delete()

    def vm_set_meta(self, name, cloud=None):
        pass
       
    def vm_get_meta(self, name, cloud=None):
        pass

    def vm_set_userdata(self, name, cloud=None):
        pass
       
    def vm_get_usedata(self, name, cloud=None):
        pass

    # #############################################
    # SECURITY MANAGEMENT
    # #############################################
    def secgroup_create(self):
        pass

    def secgroup_delete(self):
        pass

    def secgroup_get(self):
        pass

    def secgroup_list(self):
        pass

    def secgroup_list_rule(self):
        pass



    # #############################################
    # KEY MANAGEMENT
    # #############################################

    def key_add(self, name, filename, cloud=None):
        keyfile = path_expand(filename)
        if self.cloud_type(cloud) == "openstack":
            with open(os.path.expanduser(filename), 'r') as public_key:
              try:
                 self.client[cloud].keypairs.create(name=name, public_key=public_key.read())
              except exceptions.Conflict, e:
                 print ("key already exists: {0}".format(str(e)))
        else:
            raise Exception("unsupported kind or cloud: " + kind + " " + str(cloud))

    def key_find(self, name, cloud=None):
        """finds the key with the given name
        :param name: name of the key
        :param cloud: name of the cloud
        :return:
        """
        pass

    def key_delete(self, name, cloud=None):
        """deletes the key with the given name
        :param name: name of the key
        :param cloud: name of the cloud
        :return:
        """
        self.client[cloud].keypairs.delete(name)

    # #############################################
    # DELETE
    # #############################################

    def delete(self, kind, name, cloud=None):
        if self.cloud_type(cloud) == "openstack":
            if kind in ["key"]:
                self.key_delete(name, cloud=cloud)
            elif kind in ["server"]:
                self.vm_delete(name, cloud=cloud)
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

kinds = ["key"]

for cloud in clouds:
    cm.authenticate(cloud)

# l = cm.list("key", cloud="india")
# pprint (l)
for cloud in clouds:
    for kind in kinds:
        l = cm.list(kind, cloud=cloud)
        pprint (l)

cm.key_delete("gregor-key", cloud='india')
print ("--------------")
pprint(cm.list("key", cloud='india'))
print ("--------------")
cm.key_add("gregor-key", "~/.ssh/id_rsa.pub", cloud='india')
pprint(cm.list("key", cloud='india'))
print ("--------------")


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


