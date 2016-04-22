from __future__ import print_function

import socket
from uuid import UUID

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase

from pprint import pprint
from builtins import input


# noinspection PyBroadException,PyPep8Naming
class Network(ListResource):
    cm = CloudmeshDatabase()

    @classmethod
    def get_fixed_ip(cls, cloudname, fixed_ip_addr, output='table'):
        """
        Method retrieves fixed ip info
        :param cloudname:
        :param fixed_ip_addr:
        :return: fixed_ip_info
        """
        try:
            cloud_provider = CloudProvider(cloudname).provider
            result = cloud_provider.get_fixed_ip(fixed_ip_addr=fixed_ip_addr)

            return Printer.attribute(result,
                                     header=[
                                         "name",
                                         "value"
                                     ],
                                     output=output)
        except Exception as ex:
            Console.error(ex.message)

        return

    @classmethod
    def get_floating_ip(cls, cloudname, floating_ip_or_id, output='table'):
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
                for floating_ip in list(floating_ips):
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
            instance_name = None

            if instance_id is not None:
                # lookup instance_name from id
                instance_name = cls.find_instance_name(cloudname=cloudname,
                                                       instance_id=instance_id)

            # add instance_name to dict
            result["instance_name"] = instance_name

            # add misc details to response
            result["cloud"] = cloudname
            result["user"] = cloud_provider.cloud_details["credentials"]["OS_USERNAME"]
            result["project"] = cloud_provider.cloud_details["credentials"]["OS_TENANT_NAME"]

            return Printer.attribute(result,
                                     header=[
                                         "name",
                                         "value"
                                     ],
                                     output=output)
        except Exception:
            # auto detect floating-ip-id
            floating_ips = cls.get_floating_ip_list(cloudname)
            # for each floating-ip from list
            for floating_ip in list(floating_ips):
                if floating_ip["id"].startswith(floating_ip_or_id) or \
                        floating_ip["ip"].startswith(floating_ip_or_id):
                    # confirm choice with user
                    print("Did you mean floating-ip [{}] ? (y/n)".format(floating_ip["ip"]))
                    choice = input().lower()
                    # if yes, return dict
                    if choice == 'y':
                        return Printer.attribute(floating_ip,
                                                 header=[
                                                     "name",
                                                     "value"
                                                 ],
                                                 output=output)
                        # Console.error(ex.message)
        return

    @classmethod
    def reserve_fixed_ip(cls, cloudname, fixed_ip_addr):
        """
        Reserve a fixed ip address
        :param cloudname:
        :param fixed_ip_addr:
        :return:
        """
        try:
            cloud_provider = CloudProvider(cloudname).provider
            cloud_provider.reserve_fixed_ip(fixed_ip_addr=fixed_ip_addr)
            return "Success."
        except Exception as ex:
            Console.error(ex.message)


        return

    @classmethod
    def unreserve_fixed_ip(cls, cloudname, fixed_ip_addr):
        """
        Unreserve a fixed ip address
        :param cloudname:
        :param fixed_ip_addr:
        :return:
        """
        try:
            cloud_provider = CloudProvider(cloudname).provider
            cloud_provider.unreserve_fixed_ip(fixed_ip_addr=fixed_ip_addr)
            return "Success."
        except Exception as ex:
            Console.error(ex.message)
            return ex

    @classmethod
    def associate_floating_ip(cls, cloudname, instance_name, floating_ip):
        """
        Method to associate floating ip to an instance
        :param cloudname:
        :param instance_name:
        :param floating_ip:
        :return:
        """
        try:
            cloud_provider = CloudProvider(cloudname).provider
            # Find the server instance
            server = cloud_provider.provider.servers.find(name=instance_name)
            # Add the floating ip to the instance
            server.add_floating_ip(floating_ip)
            return "Success."
        except Exception as ex:
            if "already has a floating" in ex.message:
                Console.error("VM has already floating ip", traceflag=False)
            else:
                Console.error(ex.message)
                return ex
        pass

    @classmethod
    def disassociate_floating_ip(cls, cloudname, instance_name, floating_ip):
        """
        Disassociates a floating ip from an instance
        :param cloudname:
        :param instance_name:
        :param floating_ip:
        :return:
        """
        try:
            cloud_provider = CloudProvider(cloudname).provider
            # Find the server instance
            server = cloud_provider.provider.servers.find(name=instance_name)
            # Remove the floating ip from the instance
            server.remove_floating_ip(floating_ip)
            # Release the floating ip to the pool
            cls.delete_floating_ip(cloudname=cloudname,
                                   floating_ip_or_id=floating_ip)
            return "Success."
        except Exception as ex:
            Console.error(ex.message)
            return ex
        pass

    @classmethod
    def create_assign_floating_ip(cls, cloudname, instance_name):
        """
        Method to create a new floating-ip
        and associate it with the instance
        :param cloudname: cloud
        :param instance_name: name of instance
        :return: floating_ip
        """
        try:
            cloud_provider = CloudProvider(cloudname).provider
            floating_ip = cloud_provider.create_assign_floating_ip(instance_name)
            return floating_ip
        except Exception as ex:
            Console.error(ex.message)
            return

    @classmethod
    def create_floating_ip(cls, cloudname, floating_pool=None):
        """
        Method to create a floating ip address under a pool
        :param cloudname:
        :param floating_pool:
        :return: floating ip addr
        """
        try:
            cloud_provider = CloudProvider(cloudname).provider
            # If floating pool is not given,
            # get first from list
            if floating_pool is None:
                floating_pool = cloud_provider.provider.floating_ip_pools.list()[0].name
                Console.ok("Floating pool not provided, selected [{}] as the pool."
                           .format(floating_pool))

            floating_ip = cloud_provider.create_floating_ip(float_pool=floating_pool)
            return floating_ip
        except Exception as ex:
            Console.error(ex.message)
            return

    @classmethod
    def delete_floating_ip(cls, cloudname, floating_ip_or_id):
        """
        Method to delete a floating ip address
        :param cloudname:
        :param floating_ip_or_id:
        :return:
        """
        try:
            cloud_provider = CloudProvider(cloudname).provider
            floating_ip_dict = None

            # check if argument is ip or uuid
            if cls.isIPAddr(ip_or_id=floating_ip_or_id):
                # get floating ip list
                floating_ips = cls.get_floating_ip_list(cloudname)
                for floating_ip in list(floating_ips):
                    ip_addr = floating_ip["ip"]

                    # if argument ip matches floating ip addr
                    if ip_addr == floating_ip_or_id:
                        floating_ip_dict = floating_ip
                        break
            else:
                # find by floating ip uuid
                floating_ip_dict = cloud_provider.get_floating_ip(floating_ip_id=floating_ip_or_id)

            # Could not find floating IP from given args
            if floating_ip_dict is None:
                return None

            # Delete the floating ip; returns None if success
            result = cloud_provider.delete_floating_ip(floating_ip_dict["id"])

            if not result:
                return "Floating IP [{}] deleted successfully!" \
                    .format(floating_ip_dict["ip"])

        except Exception as ex:
            Console.error(ex.message)
            return

    @classmethod
    def list_floating_ip(cls, cloudname, output='table'):
        """
        Method to list floating ips
        :param cloudname:
        :return: floating ip list
        """
        try:
            floating_ips = cls.get_floating_ip_list(cloudname)

            for floating_ip in list(floating_ips.values()):
                # Get instance_id associated with instance
                instance_id = floating_ip["instance_id"]

                if instance_id is not None:
                    try:
                        instance_name = cls.find_instance_name(cloudname=cloudname,
                                                               instance_id=instance_id)
                        # Assign it to the dict
                        floating_ip["instance_name"] = instance_name
                        floating_ip["cloud"] = cloudname
                    except Exception as ex:
                        Console.error(ex.message)
                        continue
                else:
                    # If no instance associated, keep None
                    floating_ip["instance_name"] = None

            (order, header) = CloudProvider(cloudname).get_attributes("floating_ip")

            return Printer.write(floating_ips,
                                 order=order,
                                 header=header,
                                 output=output)
        except Exception as ex:
            Console.error(ex.message)

        return

    @classmethod
    def list_unused_floating_ip(cls, cloudname, output='table'):
        """
        Method to list unused floating ips
        These floating ips are not associated with any instance
        :param cloudname:
        :return: floating ip list
        """
        try:
            # fetch unused floating ips
            floating_ips = cls.get_unused_floating_ip_list(cloudname)

            # print the output
            return Printer.write(floating_ips,
                                 order=[
                                     "ip",
                                     "pool",
                                     "id",
                                     "cloud"
                                 ],
                                 header=[
                                     "floating_ip",
                                     "floating_ip_pool",
                                     "floating_ip_id",
                                     "cloud"
                                 ],
                                 output=output)
        except Exception as ex:
            Console.error(ex.message)

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

            return Printer.write(floating_ip_pools,
                                 order=order,
                                 header=header)

        except Exception as ex:
            Console.error(ex.message)
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
    def get_unused_floating_ip_list(cls, cloudname):
        """
        Method to get the unused floating IP list
        :param cloudname:
        :return: floating_ips
        """
        try:
            cloud_provider = CloudProvider(cloudname).provider
            floating_ips = cloud_provider.list_floating_ips()
            unused_floating_ips = list()

            for floating_ip in list(floating_ips.values()):
                if floating_ip["fixed_ip"] is None and \
                                floating_ip["instance_id"] is None:
                    # add to unused list
                    floating_ip["cloud"] = cloudname
                    unused_floating_ips.append(floating_ip)

            return unused_floating_ips
        except Exception as ex:
            Console.error(ex.message)

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
            Console.error(ex.message)

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

        # Lookup instance details from db
        instance_dict = cls.cm.find(kind="vm", category=cloudname,
                                    uuid=instance_id)

        # Get instance_name for vm
        if len(instance_dict) > 0:
            instance_name = list(instance_dict)[0]["name"]
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

        # Lookup instance details from db
        if cls.isUuid(instance_id):
            instance_dict = cls.cm.find(kind="vm", category=cloudname,
                                        uuid=instance_id)
        else:
            instance_dict = cls.cm.find(kind="vm", category=cloudname,
                                        name=instance_id)

        # Instance not found in DB
        if cls.isDictEmpty(instance_dict):
            # auto detect instance_id feature
            vms = cls.cm.find(kind="vm", category=cloudname)
            # check for each instance in db
            for vm in list(vms):
                # if match found in either name/id
                if vm["uuid"].startswith(instance_id) or \
                        vm["name"].startswith(instance_id):
                    # confirm choice with user
                    print("Did you mean instance [{}] ? (y/n)".format(vm["name"]))
                    choice = input().lower()
                    # if yes, return dict
                    if choice == 'y':
                        return vm
            return None
        else:
            return list(instance_dict)[0]

    @classmethod
    def find_assign_floating_ip(cls, cloudname, instance_id):
        instance_dict = cls.get_instance_dict(cloudname=cloudname,
                                              instance_id=instance_id)
        # Instance not found
        if instance_dict is None:
            Console.error("Instance [{}] not found in the cloudmesh database!"
                          .format(instance_id))
            return None

        instance_name = instance_dict["name"]

        # Get an unused ip from pool if exist and associate
        unused_floating_ips = cls.get_unused_floating_ip_list(cloudname=cloudname)

        if unused_floating_ips:
            floating_ip = unused_floating_ips[0]["ip"]
            result = cls.assign_floating_ip(cloudname=cloudname,
                                            instance_id=instance_id,
                                            floating_ip=floating_ip)
            if result is None:
                Console.error("IP {} could not be assigned to VM {} "
                          .format( floating_ip, instance_name))
                return None
        else:
            # create a new ip and associate
            floating_ip = cls.create_assign_floating_ip(cloudname=cloudname,
                                                            instance_name=instance_name)

        return floating_ip

    @classmethod
    def assign_floating_ip(cls, cloudname, instance_id, floating_ip):
        # find instance in db
        instance_dict = cls.get_instance_dict(cloudname=cloudname,
                                              instance_id=instance_id)
        # Instance not found
        if instance_dict is None:
            Console.error("Instance [{}] not found in the cloudmesh database!"
                          .format(instance_id))
            return None

        instance_name = instance_dict["name"]
        result = cls.associate_floating_ip(cloudname=cloudname,
                                           instance_name=instance_name,
                                           floating_ip=floating_ip)
        return result

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
    def isDictEmpty(cls, dictionary):
        """
        Method to test empty Dict
        :param dictionary:
        :return:
        """
        if bool(dictionary):
            return False
        else:
            return True
