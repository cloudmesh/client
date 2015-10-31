from novaclient import client
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.cloud.iaas.CloudProviderOpenstackAPI import \
    CloudProviderOpenstackAPI
from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase
import os
import requests
requests.packages.urllib3.disable_warnings()


class CloudProvider(CloudProviderBase):

    @classmethod
    def __init__(cls, cloudname):
        cls.provider = CloudProvider.set(cloudname).nova

    @classmethod
    def set(cls, cloudname):
        try:
            d = ConfigDict("cloudmesh.yaml")
            cloud = d["cloudmesh"]["clouds"][cloudname]
            cert = None

            if cloud["cm_type"] == "openstack":
                credentials = cloud["credentials"]
                cls.provider = CloudProviderOpenstackAPI(cloudname,
                                                          cloud).nova
                return cls.provider

            elif cloud["cm_type"] == "ec2":

                raise NotImplemented("Not implemented yet. IMplemented in "
                                     "old cloudmesh")

            elif cloud["cm_type"] == "azure":

                raise NotImplemented("Not implemented yet. implemented in "
                                     "old cloudmesh")

            elif cloud["cm_type"] == "aws":

                raise NotImplemented("Not implemented yet. implemented in "
                                     "old cloudmesh")


        except Exception, e:
            raise Exception("Error in getting environment"
                            " for cloud: {}, {}".format(cloudname, e))
