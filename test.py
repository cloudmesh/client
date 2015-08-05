import os
from novaclient.client import Client
from cloudmesh_base.util import path_expand
import sys
import json


def get_nova_credentials_v2():
     d = {}
     d['version'] = '2'
     d['username'] = os.environ['OS_USERNAME']
     d['api_key'] = os.environ['OS_PASSWORD']
     d['auth_url'] = os.environ['OS_AUTH_URL']
     d['project_id'] = os.environ['OS_TENANT_NAME']
     d['cacert'] = path_expand(os.environ['OS_CACERT'])
     return d


openstack_client_keys  = [
    ["username", "OS_USERNAME"],
    ["password", "OS_PASSWORD",  "api_key"],
    ["auth_url", "OS_AUTH_URL"],
    ["tenant_id", "OS_TENANT_ID"],
    ["region_name", "OS_REGION_NAME"],
    ["cacert", "OS_CACERT"],
    ["version", "OS_COMPUTE_API_VERSION"],
    ["project_id", "OS_TENANT_NAME", ],
]

class MultiKeyDict(object):
    
    def __init__(self, m):
        self.element = {
            "keys" : m,
            "value" : {}
            }
           
    def dump(self):
        print(json.dumps(self.element, indent=4))


    def set(self, d):
        for key in d:
           self.__setitem__(key, d[key])

    def _getkey(self, key):
        for k in self.element["keys"]:
            if key in k:
                return k[0]
        raise Exception("key not found: " + key)

    def __getitem__(self, key):
        return self.element["value"][self._getkey(key)] 

    def __setitem__(self, key, value):
        self.element["value"][self._getkey(key)] = value
    
    def __str__(self):
        return str(dict(self.element["value"]))

m = MultiKeyDict(openstack_client_keys)

m["username"] = "gregor"
print ("U", m["username"])
print ("U", m["OS_USERNAME"])

m["OS_PASSWORD"] = "1234"
print("P", m["password"])
print("P", m["OS_PASSWORD"])



m.set(get_nova_credentials_v2())

m.dump()

sys.exit()


print (m)

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


credentials = get_nova_credentials_v2()

nova_client = Client(**credentials)

print(nova_client.servers.list())
