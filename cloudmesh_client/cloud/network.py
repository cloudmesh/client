from __future__ import print_function

import socket
from uuid import UUID
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
        """
        Method retrieves fixed ip info
        :param cloudname:
        :param fixed_ip_addr:
        :return: fixed_ip_info
        """
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
    def get_floating_ip(cls, cloudname, floating_ip_or_id):
        """
        Method to get floating ip info
        :param cloudname:
        :param floating_ip_or_id:
        :return: floating ip info
        """
        try:
            cloud_provider = CloudProvider(cloudname).provider
            result = None

            # check if argument is ip or uuid
            if cls.isIPAddr(ip_or_id=floating_ip_or_id):
                # get floating ip list
                floating_ips = cls.get_floating_ip_list(cloudname)
                for floating_ip in floating_ips.values():
                    ip_addr = floating_ip["ip"]

                    # if argument ip matches floating ip addr
                    if ip_addr == floating_ip_or_id:
                        result = floating_ip
                        break
            else:
                # find by floating ip uuid
                result = cloud_provider.get_floating_ip(floating_ip_id=floating_ip_or_id)

            # Could not find floating IP from given args
            if result is None:
                return None

            instance_id = result["instance_id"]
            # lookup instance_name from id
            instance_name = cls.find_instance_name(cloudname=cloudname,
                                                   instance_id=instance_id)

            # add instance_name to dict
            result["instance_name"] = instance_name

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
        """
        Method to list floating ips
        :param cloudname:
        :return: floating ip list
        """
        try:
            floating_ips = cls.get_floating_ip_list(cloudname)

            for floating_ip in floating_ips.values():
                # Get instance_id associated with instance
                instance_id = floating_ip["instance_id"]

                if instance_id is not None:
                    try:
                        instance_name = cls.find_instance_name(cloudname=cloudname,
                                                               instance_id=instance_id)
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
        """
        Method to list floating ip pool
        :param cloudname:
        :return:
        """
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

    @classmethod
    def isIPAddr(cls, ip_or_id):
        """
        Method to check if argument is IP address or notS
        :param ip_or_id:
        :return:
        """
        try:
            socket.inet_aton(ip_or_id)
            return True
        except:
            return False

    @classmethod
    def get_floating_ip_list(cls, cloudname):
        """
        Method to get the floating IP list
        :param cloudname:
        :return: floating_ips
        """
        try:
            cloud_provider = CloudProvider(cloudname).provider
            floating_ips = cloud_provider.list_floating_ips()
            return floating_ips
        except Exception as ex:
            Console.error(ex.message, ex)


    @classmethod
    def find_instance_name(cls, **kwargs):
        """
        Method to find instance name
        :param kwargs:
        :return: instance_name
        """
        cloudname = kwargs["cloudname"]
        instance_id = kwargs["instance_id"]

        # Cloudmesh database instance
        db = CloudmeshDatabase()

        # Lookup instance details from db
        instance_dict = db.find(kind="vm", cloud=cloudname, uuid=instance_id)
        # Get instance_name for vm
        instance_name = instance_dict.values()[0]["name"]

        return instance_name

    @classmethod
    def get_instance_dict(cls, **kwargs):
        """
        Method to get instance dict
        :param kwargs:
        :return: instance dict
        """
        cloudname = kwargs["cloudname"]
        instance_id = kwargs["instance_id"]

        # Cloudmesh database instance
        db = CloudmeshDatabase()

        # Lookup instance details from db
        if cls.isUuid(instance_id):
            instance_dict = db.find(kind="vm", cloud=cloudname, uuid=instance_id)
        else:
            instance_dict = db.find(kind="vm", cloud=cloudname, name=instance_id)

        # Instance not found in DB
        if cls.isDictEmpty(instance_dict):
            return None
        else:
            return instance_dict.values()[0]

    @classmethod
    def isUuid(cls, argument):
        """
        Method to check if arg is an UUID
        :param argument:
        :return:
        """
        try:
            UUID(argument, version=4)
            return True
        except ValueError:
            return False

    @classmethod
    def isDictEmpty(cls, dict):
        """
        Method to test empty Dict
        :param dict:
        :return:
        """
        if bool(dict):
            return False
        else:
            return True