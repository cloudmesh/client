from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.cloud.iaas.provider.openstack.CloudProviderOpenstackAPI import \
    CloudProviderOpenstackAPI
from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase
import requests
from cloudmesh_client.common.Error import Error
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.cloud.iaas.provider.libcloud.CloudProviderLibcloudEC2 import CloudProviderLibcloudEC2
from cloudmesh_client.cloud.iaas.provider.azure.CloudProviderAzureAPI import CloudProviderAzureAPI
from cloudmesh_client.shell.console import Console

requests.packages.urllib3.disable_warnings()


class CloudProvider(CloudProviderBase):
    def __init__(self, cloudname, user=None, flat=True):
        super(CloudProvider, self).__init__(cloudname, user=user)

        try:
            d = ConfigDict("cloudmesh.yaml")

            if cloudname not in d["cloudmesh"]["clouds"]:
                Console.error("the cloud {} is not defined in the yaml file. failed."
                                 .format(cloudname), traceflag=False)
                return

            cloud_details = d["cloudmesh"]["clouds"][cloudname]

            if cloud_details["cm_type"] == "openstack":
                provider = CloudProviderOpenstackAPI(
                    cloudname,
                    cloud_details,
                    flat=flat)
                self.provider = provider
                self.provider_class = CloudProviderOpenstackAPI

            if cloud_details["cm_type"] == "ec2":
                provider = CloudProviderLibcloudEC2(
                    cloudname,
                    cloud_details,
                    flat=flat)
                self.provider = provider
                self.provider_class = CloudProviderLibcloudEC2

            if cloud_details["cm_type"] == "azure":
                # raise ValueError("azure cloud provider yet implemented. failed.")
                # Console.TODO("Azure provider to be implemented")
                provider = CloudProviderAzureAPI(
                    cloudname,
                    cloud_details)
                self.provider = provider
                self.provider_class = CloudProviderAzureAPI



        except Exception as e:
            Error.traceback(e)

    def get_attributes(self, kind):
        return self.provider.attributes(kind)


def main():
    from pprint import pprint

    cloud = "kilo"
    provider = CloudProvider(cloud).provider

    print(provider, type(provider))

    # pprint (provider.__dict__)
    # pprint (dir(provider))

    r = provider.list_flavor(cloud)
    pprint(r)

    for kind in ["flavor", "image", "vm", "key"]:  # "limits", "quota"]:
        r = provider.list(kind, cloud)
        pprint(r)


if __name__ == "__main__":
    main()
