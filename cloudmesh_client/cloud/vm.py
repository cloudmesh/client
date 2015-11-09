from __future__ import print_function
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.cloud.iaas.CloudProviderOpenstackAPI import \
    CloudProviderOpenstackAPI

from cloudmesh_client.common.todo import TODO
# add imports for other cloud providers in future
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider


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
    def boot(cls, **kwargs):
        cloud_provider = CloudProvider(kwargs["cloud"]).provider
        vm_id = cloud_provider.boot_vm(kwargs["name"], kwargs["image"], kwargs["flavor"], key=kwargs["key_name"],
                                       secgroup=kwargs["secgroup_list"])
        print("Machine {:} is being booted on {:} Cloud...".format(kwargs["name"], cloud_provider.cloud))

        # Explicit refresh called after VM boot, to update db.
        cls.refresh(cloud=kwargs["cloud"])

        return vm_id

    @classmethod
    def delete(cls, **kwargs):
        cloud_provider = CloudProvider(kwargs["cloud"]).provider
        for server in kwargs["servers"]:
            cloud_provider.delete_vm(server)
            print("Machine {:} is being deleted on {:} Cloud...".format(server, cloud_provider.cloud))

        # Explicit refresh called after VM delete, to update db.
        cls.refresh(cloud=kwargs["cloud"])

    @classmethod
    def info(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def list(cls, **kwargs):
        """
        This method lists all VMs of the cloud
        :param cloud: the cloud name
        """

        try:
            elements = cls.cm.find("vm", cloud=kwargs["cloud"])

            # print(elements)

            # order = ['id', 'uuid', 'name', 'cloud']
            (order, header) = CloudProvider(kwargs["cloud"]).get_attributes("vm")

            # order = None
            return dict_printer(elements,
                                order=order,
                                output=kwargs["output_format"])
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def clear(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def refresh(cls, **kwargs):
        # print("Inside refresh")
        return cls.cm.refresh("vm", kwargs["cloud"])
