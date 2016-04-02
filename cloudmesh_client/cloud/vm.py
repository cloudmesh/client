from __future__ import print_function
from cloudmesh_client.common.ConfigDict import ConfigDict

from cloudmesh_client.common.todo import TODO
# add imports for other cloud providers in future
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.Error import Error
from uuid import UUID
from cloudmesh_client.common.dotdict import dotdict
from builtins import input
from pprint import pprint



# noinspection PyPep8Naming
class Vm(ListResource):

    cm = CloudmeshDatabase()
    
    @classmethod
    def construct_ip_dict(cls, ip_addr, name="kilo"):
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

        except Exception as e:
            Error.error("error in vm construct dict", traceback=True)

    @classmethod
    def isUuid(cls, name):
        try:
            UUID(name, version=4)
            return True
        except ValueError:
            return False

    @classmethod
    def boot(cls, **kwargs):

        data = dotdict(kwargs)
        pprint (data)

        for a in ["key", "name", "image", "flavor"]:
            if a not in kwargs:
                raise ValueError (a + " not in arguments to vm boot")

        conf = ConfigDict("cloudmesh.yaml")
        data.username = conf["cloudmesh"]["profile"]["username"]

        cloud_provider = CloudProvider(data.cloud).provider

        if "nics" in data:
            nics = data.nics
        else:
            nics = None

        vm = cloud_provider.boot_vm(data.name,
                                    data.image,
                                    data.flavor,
                                    key=data.key,
                                    secgroup=kwargs["secgroup_list"],
                                    nics=nics)


        print("Machine {name} is being booted on {cloud} Cloud...".format(**data))
        cls.refresh(cloud=data.cloud)

        cls.cm.update("vm", name=data.name)

        return vm

    @classmethod
    def start(cls, **kwargs):
        cloud_provider = CloudProvider(kwargs["cloud"]).provider
        for server in kwargs["servers"]:
            cloud_provider.start_vm(server)
            print("Machine {:} is being started on {:} Cloud...".format(server, cloud_provider.cloud))

        # Explicit refresh called after VM start, to update db.
        # cls.refresh(cloud=kwargs["cloud"])

    @classmethod
    def stop(cls, **kwargs):
        cloud_provider = CloudProvider(kwargs["cloud"]).provider
        for server in kwargs["servers"]:
            cloud_provider.stop_vm(server)
            print("Machine {:} is being stopped on {:} Cloud...".format(server, cloud_provider.cloud))

        # Explicit refresh called after VM stop, to update db.
        # cls.refresh(cloud=kwargs["cloud"])

    @classmethod
    def delete(cls, **kwargs):

        if "cloud" in kwargs:
            cloud_provider = CloudProvider(kwargs["cloud"]).provider
            for server in kwargs["servers"]:
                cloud_provider.delete_vm(server)
                print("VM {:} is being deleted on {:} cloud...".format(server, cloud_provider.cloud))

            cls.refresh(cloud=kwargs["cloud"])
        else:

            clouds = set()
            for server in kwargs["servers"]:
                try:
                    vm = cls.cm.find_by_name("VM", name=server)

                    cloud = vm["category"]
                    cloud_provider = CloudProvider(cloud).provider
                    clouds.add(cloud)
                    cloud_provider.delete_vm(server)
                    print("VM {:} is being deleted on {:} cloud...".format(server, cloud))
                except:
                    print("VM {:} can not be found.".format(server))

            for cloud in clouds:
                cls.refresh(cloud=cloud)


    @classmethod
    def get_vms_by_name(cls, name, cloud):
       
        vm_data = cls.cm.find("vm", name=name, category=cloud)
        if vm_data is None or len(vm_data) == 0:
            raise RuntimeError("VM data not found in database.")
        return vm_data

    @classmethod
    def rename(cls, **kwargs):

        dry_run = False

        if kwargs["is_dry_run"] is not None:
            dry_run = kwargs["is_dry_run"]

        if dry_run:
            print("Running in dryrun mode...")

        cloud_provider = CloudProvider(kwargs["cloud"]).provider
        new_name = kwargs["new_name"]
        for server in kwargs["servers"]:

            # Check for vms with duplicate names in DB.
            vms = cls.get_vms_by_name(name=server, cloud=kwargs["cloud"])

            if len(vms) > 1:
                users_choice = "y"

                if not kwargs["force"]:
                    print("More than 1 vms found with the same name as {}.".format(server))
                    users_choice = input("Would you like to auto-order the new names? (y/n): ")

                if users_choice.strip() == "y":
                    count = 1
                    for index in vms:
                        count_new_name = "{0}{1}".format(new_name, count)
                        # print(vms[index])

                        if not dry_run:
                            cloud_provider.rename_vm(vms[index]["uuid"], count_new_name)

                        print("Machine {0} with UUID {1} renamed to {2} on {3} cloud".format(vms[index]["name"],
                                                                                             vms[index]["uuid"],
                                                                                             count_new_name,
                                                                                             cloud_provider.cloud))
                        count += 1
                elif users_choice.strip() == "n":
                    if not dry_run:
                        cloud_provider.rename_vm(server, new_name)
                    print("Machine {0} renamed to {1} on {2} Cloud...".format(server, new_name, cloud_provider.cloud))
                else:
                    Console.error("Invalid Choice.")
                    return
            else:
                if not dry_run:
                    cloud_provider.rename_vm(server, new_name)
                print("Machine {0} renamed to {1} on {2} Cloud...".format(server, new_name, cloud_provider.cloud))

        if not dry_run:
            # Explicit refresh called after VM rename, to update db.
            cls.refresh(cloud=kwargs["cloud"])

    @classmethod
    def info(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def list(cls, **kwargs):
        """
        This method lists all VMs of the cloud
        """
        
        # prevent circular dependency
        def vm_groups(vm):
            """

            :param vm: name of the vm
            :return: a list of groups the vm is in
            """
            
            try:
                query = {
                    "type": "vm",
                    "member": vm
                }

                d = cls.cm.find("GROUP", **query)
                groups = set()
                for vm in d:
                    groups.add(d[vm]['name'])
                return list(groups)
            except Exception as ex:
                Console.error(ex.message, ex)

        try:
            if "name_or_id" in kwargs and kwargs["name_or_id"] is not None:
                if cls.isUuid(kwargs["name_or_id"]):
                    elements = cls.cm.find("vm",
                                           category=kwargs["cloud"],
                                           uuid=kwargs["name_or_id"])
                else:
                    elements = cls.cm.find("vm",
                                           category=kwargs["cloud"],
                                           label=kwargs["name_or_id"])
            else:
                elements = cls.cm.find("vm",
                                       category=kwargs["cloud"])



            for key in elements:
                element = elements[key]
                name = element["name"]
                groups = vm_groups(name)
                element["group"] = ','.join(groups)

            # print(elements)

            # order = ['id', 'uuid', 'name', 'cloud']
            (order, header) = CloudProvider(kwargs["cloud"]).get_attributes("vm")

            # order = None
            if "name_or_id" in kwargs and kwargs["name_or_id"] is not None:
                return Printer.attribute(list(elements.values())[0],
                                         output=kwargs["output_format"])
            else:
                return Printer.write(elements,
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

    @classmethod
    def status_from_cloud(cls, **kwargs):
        cloud_provider = CloudProvider(kwargs["cloud"]).provider
        vm = cloud_provider.get_vm(name=kwargs["name_or_id"])
        return vm["status"]

    @classmethod
    def set_vm_login_user(cls, name_or_id, cloud, username):
        print(name_or_id, username)
        ValueError("this method is wrong implemented")
       
        '''
        if cls.isUuid(name_or_id):
            uuid = name_or_id
        else:
            vm_data = cls.cm.find("vm", category=cloud, label=name_or_id)
            if vm_data is None or len(vm_data) == 0:
                raise RuntimeError("VM with label {} not found in database.".format(name_or_id))
            uuid = list(vm_data.values())[0]["uuid"]

        user_map_entry = cls.cm.find("VMUSERMAP", vm_uuid=uuid)

        if user_map_entry is None or len(user_map_entry) == 0:
            user_map_dict = cls.cm.db_obj_dict("VMUSERMAP", vm_uuid=uuid, username=username)
            cls.cm.add_obj(user_map_dict)
            cls.cm.save()
        else:
            cls.cm.update_vm_username(vm_uuid=uuid, username=username)
        '''

    @classmethod
    def get_vm_login_user(cls, name_or_id, cloud):
        print(name_or_id, cloud)

        ValueError("this method is wrong implemented")
       
        '''
        if cls.isUuid(name_or_id):
            uuid = name_or_id
        else:
            vm_data = cls.cm.find("vm", category=cloud, label=name_or_id)
            if vm_data is None or len(vm_data) == 0:
                raise RuntimeError("VM with label {} not found in database.".format(name_or_id))
            uuid = list(vm_data.values())[0]["uuid"]

        # print(uuid)

        user_map_entry = cls.cm.find("VMUSERMAP", vm_uuid=uuid)

        # print(user_map_entry)

        if user_map_entry is None or len(user_map_entry) == 0:
            return None
        else:
            return list(user_map_entry.values())[0]["username"]
        '''

    @classmethod
    def get_last_vm(cls, cloud):
       
        vm_data = cls.cm.find("vm", scope="first", category=cloud)
        if vm_data is None or len(vm_data) == 0:
            raise RuntimeError("VM data not found in database.")
        return vm_data

    @classmethod
    def get_vm_public_ip(cls, vm_name, cloud):
        """

        :param vm_name: Name of the VM instance whose Public IP has to be retrieved from the DB
        :param cloud: Libcloud supported Cloud provider name
        :return: Public IP as a list
        """
        public_ip_list = []
        vms = cls.get_vms_by_name(vm_name, cloud)
        keys = vms.keys()
        if keys is not None and len(keys) > 0:
            public_ip = vms[keys[0]]["public_ips"]
            if public_ip is not None and public_ip != "":
                public_ip_list.append(public_ip)
        return public_ip_list
