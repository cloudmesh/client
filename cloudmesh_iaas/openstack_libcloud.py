from __future__ import print_function
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security
import datetime
from cloudmesh_common.ConfigDict import ConfigDict
from cloudmesh_common.ConfigDict import Config
from time import sleep
from pprint import pprint

class OpenStack_libcloud(object):

    def __init__(self, cloudname, user=None):
        self.cloudname = cloudname
        self.user = user
        OpenStack = get_driver(Provider.OPENSTACK)
        self.credential = \
            ConfigDict("cloudmesh.yaml")['cloudmesh']['clouds'][cloudname]['credentials']

        libcloud.security.CA_CERTS_PATH = [Config.path_expand(self.credential['OS_CACERT'])]
        libcloud.security.VERIFY_SSL_CERT = True

        auth_url = "%s/tokens/" % self.credential['OS_AUTH_URL']

        self.driver = OpenStack(
            self.credential['OS_USERNAME'],
            self.credential['OS_PASSWORD'],
            ex_force_auth_url=auth_url,
            ex_tenant_name=self.credential['OS_TENANT_NAME'],
            ex_force_auth_version='2.0_password',
            ex_force_service_region='regionOne')

    def _list(self, nodes, kind=dict):
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + " UTC"
        result = None
        if kind == list:
            result = []
        elif kind == dict:
            result = {}
        for node in nodes:
            values = dict(node.__dict__)
            del values["_uuid"]
            del values["driver"]
            values["cm_cloud"] = self.cloudname
            values["cm_update"] = now
            values["cm_user"] = self.user
            if kind == list:
                result.append(values)
            elif kind == dict:
                result[values["id"]] = values
        return result

    def list_nodes(self, kind=dict):
        return self._list(self.driver.list_nodes(), kind)

    def list_images(self, kind=dict):
        return self._list(self.driver.list_images(), kind)

    def list_flavors(self, kind=dict):
        return self._list(self.driver.list_sizes(), kind)
