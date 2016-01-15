from __future__ import print_function
from cloudmesh_client.common.ConfigDict import ConfigDict

from cloudmesh_client.common.todo import TODO
# add imports for other cloud providers in future
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.common.Printer import dict_printer, attribute_printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.Error import Error

from uuid import UUID


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

        except Exception, e:
            Error.traceback(e)

    @classmethod
    def isUuid(cls, name):
        try:
            UUID(name, version=4)
            return True
        except ValueError:
            return False

    @classmethod
    def boot(cls, **kwargs):

        key_name = kwargs["key_name"]
        cloud_name = kwargs["cloud"]

        conf = ConfigDict("cloudmesh.yaml")
        username = conf["cloudmesh"]["profile"]["username"]

        keycloudmap = cls.cm.get_key_cloud_mapping(username, key_name, cloud_name)

        if keycloudmap is None or len(keycloudmap) == 0:
            Console.error("No key cloud mapping found for user {:}, key name {:} and cloud {:} in database."
                          .format(username, key_name, cloud_name))
            return

        # print("Keycloudmap = {:}".format(keycloudmap))
        key_name_on_cloud = keycloudmap["key_name_on_cloud"]

        # print("Booting with key_name_on_cloud as " + key_name_on_cloud)

        cloud_provider = CloudProvider(cloud_name).provider

        if "nics" in kwargs:
           vm = cloud_provider.boot_vm(kwargs["name"],
                                           kwargs["image"],
                                           kwargs["flavor"],
                                           key=key_name_on_cloud,
                                           secgroup=kwargs["secgroup_list"],
                                           nics=nics)
        else:
            vm = cloud_provider.boot_vm(kwargs["name"],
                                           kwargs["image"],
                                           kwargs["flavor"],
                                           key=key_name_on_cloud,
                                           secgroup=kwargs["secgroup_list"],
                                           nics=None)

        print("Machine {:} is being booted on {:} Cloud...".format(kwargs["name"], cloud_provider.cloud))
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
            if "name_or_id" in kwargs and kwargs["name_or_id"] is not None:
                if cls.isUuid(kwargs["name_or_id"]):
                    elements = cls.cm.find("vm", cloud=kwargs["cloud"], uuid=kwargs["name_or_id"])
                else:
                    elements = cls.cm.find("vm", cloud=kwargs["cloud"], label=kwargs["name_or_id"])
            else:
                elements = cls.cm.find("vm", cloud=kwargs["cloud"])

            # print(elements)

            # order = ['id', 'uuid', 'name', 'cloud']
            (order, header) = CloudProvider(kwargs["cloud"]).get_attributes("vm")

            # order = None
            if "name_or_id" in kwargs and kwargs["name_or_id"] is not None:
                return attribute_printer(elements.values()[0],
                                         output=kwargs["output_format"])
            else:
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

    @classmethod
    def status_from_cloud(cls, **kwargs):
        cloud_provider = CloudProvider(kwargs["cloud"]).provider
        vm = cloud_provider.get_vm(name=kwargs["name_or_id"])
        return vm["status"]

    @classmethod
    def set_vm_login_user(cls, name_or_id, cloud, username):

        if cls.isUuid(name_or_id):
            uuid = name_or_id
        else:
            vm_data = cls.cm.find("vm", cloud=cloud, label=name_or_id)
            if vm_data is None or len(vm_data) == 0:
                raise RuntimeError("VM with label {} not found in database.".format(name_or_id))
            uuid = vm_data.values()[0]["uuid"]

        user_map_entry = cls.cm.find("VMUSERMAP", vm_uuid=uuid)

        if user_map_entry is None or len(user_map_entry) == 0:
            user_map_dict = cls.cm.db_obj_dict("VMUSERMAP", vm_uuid=uuid, username=username)
            cls.cm.add_obj(user_map_dict)
            cls.cm.save()
        else:
            cls.cm.update_vm_username(vm_uuid=uuid, username=username)

    @classmethod
    def get_vm_login_user(cls, name_or_id, cloud):

        if cls.isUuid(name_or_id):
            uuid = name_or_id
        else:
            vm_data = cls.cm.find("vm", cloud=cloud, label=name_or_id)
            if vm_data is None or len(vm_data) == 0:
                raise RuntimeError("VM with label {} not found in database.".format(name_or_id))
            uuid = vm_data.values()[0]["uuid"]

        # print(uuid)

        user_map_entry = cls.cm.find("VMUSERMAP", vm_uuid=uuid)

        # print(user_map_entry)

        if user_map_entry is None or len(user_map_entry) == 0:
            return None
        else:
            return user_map_entry.values()[0]["username"]
