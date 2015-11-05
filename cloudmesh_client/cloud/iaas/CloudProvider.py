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

    def __init__(self, cloudname, user=None):
        super( CloudProvider, self ).__init__(cloudname, user=user)

        try:
            d = ConfigDict("cloudmesh.yaml")
            cloud_details = d["cloudmesh"]["clouds"][cloudname]

            if cloud_details["cm_type"] == "openstack":

                provider = CloudProviderOpenstackAPI(
                    cloudname,
                    cloud_details)
                self.provider = provider

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



def main():
    from pprint import pprint

    cloud = "juno"
    provider = CloudProvider(cloud)
    print (provider, type(provider))

    #pprint (provider.__dict__)
    #pprint (dir(provider))


    r = provider.provider.list("flavor", cloud)

    print (r)
    # print(dir(provider.provider))

    #provider.list_flavor(cloud)
    #provider.list("flavor", cloud)

if __name__ == "__main__":
    main()
