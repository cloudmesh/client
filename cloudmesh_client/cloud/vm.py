from __future__ import print_function
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.cloud.iaas.CloudProviderOpenstackAPI import \
    CloudProviderOpenstackAPI

from cloudmesh_client.common.todo import TODO
# add imports for other cloud providers in future
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase


class Vm(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def construct_ip_dict(cls, ip_addr, name="india"):
        try:
            d = ConfigDict("cloudmesh.yaml")
            cloud_details = d["cloudmesh"]["clouds"][name]

            # Handle Openstack Specific Output
            if cloud_details["cm_type"] == "openstack":
                ipaddr = {}
                for network in ip_addr:
                    index = 0
                    for ip in ip_addr[network]:
                        ipaddr[index] = {}
                        ipaddr[index]["network"] = network
                        ipaddr[index]["version"] = ip["version"]
                        ipaddr[index]["addr"] = ip["addr"]
                        index += 1
                return ipaddr

            # Handle EC2 Specific Output
            if cloud_details["cm_type"] == "ec2":
                print("ec2 ip dict yet to be implemented")
                TODO.implement()

            # Handle Azure Specific Output
            if cloud_details["cm_type"] == "azure":
                print("azure ip dict yet to be implemented")
                TODO.implement()

        except Exception, e:
            import traceback
            print(traceback.format_exc())
            print(e)

    @classmethod
    def info(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def list(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def clear(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def refresh(cls, **kwargs):
        # print("Inside refresh")
        return cls.cm.refresh("vm", kwargs["cloud"])
