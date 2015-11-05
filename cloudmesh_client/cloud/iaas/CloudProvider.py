from novaclient import client
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.cloud.iaas.CloudProviderOpenstackAPI import \
    CloudProviderOpenstackAPI
from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase
import os
import requests

from cloudmesh_client.common.todo import TODO

requests.packages.urllib3.disable_warnings()


class CloudProvider(CloudProviderBase):

    @classmethod
    def __init__(cls, cloudname):
        cls.provider = CloudProvider.set(cloudname).nova

    @classmethod
    def set(cls, cloudname):
        try:
            d = ConfigDict("cloudmesh.yaml")
            cloud_details = d["cloudmesh"]["clouds"][cloudname]

            if cloud_details["cm_type"] == "openstack":
                return CloudProviderOpenstackAPI(cloudname, cloud_details)

            if cloud_details["cm_type"] == "ec2":
                print("ec2 cloud provider yet to be implemented")
                TODO.implement()

            if cloud_details["cm_type"] == "azure":
                print("azure cloud provider yet to be implemented")
                TODO.implement()

        except Exception, e:
            import traceback
            print(traceback.format_exc())
            print(e)
