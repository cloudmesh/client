from __future__ import print_function

from pprint import pprint
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.Printer import attribute_printer
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase


class Network(ListResource):
    @classmethod
    def get_fixed_ip(cls, cloudname, fixed_ip_addr):
        try:
            cloud_provider = CloudProvider(cloudname).provider
            result = cloud_provider.get_fixed_ip(fixed_ip_addr=fixed_ip_addr)

            return attribute_printer(result,
                                     header=[
                                         "name",
                                         "value"
                                     ])
        except Exception as ex:
            Console.error(ex.message, ex)

        return

    @classmethod
    def get_floating_ip(cls, cloudname, floating_ip_id):
        try:
            cloud_provider = CloudProvider(cloudname).provider
            result = cloud_provider.get_floating_ip(floating_ip_id=floating_ip_id)

            return attribute_printer(result,
                                     header=[
                                         "name",
                                         "value"
                                     ])
        except Exception as ex:
            Console.error(ex.message, ex)

        return

    @classmethod
    def fixed_ip_reserve(cls, cloud, fixed_ip):
        pass

    @classmethod
    def fixed_ip_unreserve(cls, cloud, fixed_ip):
        pass

    @classmethod
    def floating_ip_associate(cls, cloud, server, floating_ip):
        pass

    @classmethod
    def floating_ip_disassociate(cls, cloud, server, floating_ip):
        pass

    @classmethod
    def floating_ip_create(cls, cloud, floating_pool=None):
        pass

    @classmethod
    def floating_ip_delete(cls, cloud, floating_ip):
        pass

    @classmethod
    def list_floating_ip(cls, cloudname):
        try:
            cloud_provider = CloudProvider(cloudname).provider
            floating_ips = cloud_provider.list_floating_ips()

            # Cloudmesh database instance
            db = CloudmeshDatabase()

            for floating_ip in floating_ips.values():
                # Get instance_id associated with instance
                instance_id = floating_ip["instance_id"]

                if instance_id is not None:
                    try:
                        # Lookup instance details from db
                        instance_dict = db.find(kind="vm", cloud=cloudname, uuid=instance_id)
                        # Get instance_name for vm
                        instance_name = instance_dict.values()[0]["name"]
                        # Assign it to the dict
                        floating_ip["instance_name"] = instance_name
                    except Exception as ex:
                        Console.error(ex.message)
                        continue
                else:
                    # If no instance associated, keep None
                    floating_ip["instance_name"] = None

            (order, header) = CloudProvider(cloudname).get_attributes("floating_ip")

            return dict_printer(floating_ips,
                                order=order,
                                header=header)
        except Exception as ex:
            Console.error(ex.message, ex)

        return

    @classmethod
    def list_floating_ip_pool(cls, cloudname):
        try:
            cloud_provider = CloudProvider(cloudname).provider
            floating_ip_pools = cloud_provider.list_floating_ip_pools()

            (order, header) = CloudProvider(cloudname).get_attributes("floating_ip_pool")

            return dict_printer(floating_ip_pools,
                                order=order,
                                header=header)

        except Exception as ex:
            Console.error(ex.message, ex)
        pass
