from novaclient import client
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.cloud.iaas.CloudProviderOpenstack import CloudProviderOpenstack
from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase
import os
import requests
requests.packages.urllib3.disable_warnings()


#
# TODO: this class is in the wrong directory, it belongs in iaas for openstack
# TODO: the name get environment is quite awkward
# TODO: what implication would there if the cloud would not be openstack,
# we should make at least provisions for that the others are not
# implemented, but in general authentication should take a provider and use
# the provider to authenticate and not reimplementing what a provider is
# supposed to do.

#
# This was duplicated all over and it will not work as we also have to unset
#  the variables
#
def set_os_environ(cloudname):
    """Set os environment variables on a given cloudname"""
    try:
        d = ConfigDict("cloudmesh.yaml")
        credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]
        for key, value in credentials.iteritems():
            if key == "OS_CACERT":
                os.environ[key] = Config.path_expand(value)
            else:
                os.environ[key] = value
    except Exception, e:
        print(e)


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
                cls.provider = CloudProviderOpenstack(cloudname,
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
