from __future__ import print_function
from cloudmesh_client.cloud.iaas.IndiaCloudProvider import IndiaCloudProvider
# add imports for other cloud providers in future


class Vm(object):

    @classmethod
    def get_cloud_provider(cls, name="india"):
        if name == "india":
            return IndiaCloudProvider()
        # Append checks for more clouds
