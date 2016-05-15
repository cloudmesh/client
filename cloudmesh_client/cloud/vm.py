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
from cloudmesh_client.cloud.network import Network
from cloudmesh_client.default import Default
import traceback

# noinspection PyPep8Naming
class Vm(ListResource):
    cm = CloudmeshDatabase()


    @classmethod
    def uuid(cls, name, category=None):
        vm = cls.get(name, category=category)
        if vm is None:
            return None

        return vm.uuid

    @classmethod
    def get(cls, key, category=None):
        """
        returns the value of the first objects matching the key
        with the given category.

        :param key: The dictionary key
        :param category: The category
        :return:
        """

        if category is None:
            o = cls.cm.find(kind='vm',
                            output='dict',
                            scope='first',
                            name=key)

        else:
            o = cls.cm.find(category=category,
                            kind='vm',
                            output='dict',
                            scope='first',
                            name=key)
        return o

    @classmethod
    def construct_ip_dict(cls, ip_addr, name=None):
        # TODO kilo cloud as defualt should be avoided
        if name is None:
            Console.error("cloud name not set")
            return None
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
                Console.TODO("ec2 ip dict yet to be implemented")
                TODO.implement()

            # Handle Azure Specific Output
            if cloud_details["cm_type"] == "azure":
                index = 0
                ipaddr = {}
                for ip in ip_addr:
                    ipaddr[index] = {}
                    ipaddr[index]["network"] = ip
                    ipaddr[index]["version"] = 'ipv4'
                    ipaddr[index]["addr"] = ip
                    index += 1
                return ipaddr

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

        arg = dotdict(kwargs)

        for a in ["key", "name", "image", "flavor"]:
            if a not in kwargs:
                raise ValueError(a + " not in arguments to vm boot")

        conf = ConfigDict("cloudmesh.yaml")
        arg.username = conf["cloudmesh"]["profile"]["user"]
        arg.group = arg.group or Default.group
        cloud_provider = CloudProvider(arg.cloud).provider

        if "nics" in arg:
            nics = arg.nics
        else:
            nics = None

        basic_dict = {
            "cloud": arg.cloud,
            "name": arg.name,
            "image": arg.image,
            "flavor": arg.flavor,
            "key": arg.key,
            "secgroup": [arg.secgroup],
            "nics": nics,
            "meta": {'kind': 'cloudmesh',
                     'group': arg.group,
                     'image': arg.image,
                     'flavor': arg.flavor,
                     'key': arg.key,
                     'category': arg.cloud
                    }
        }

        # Special case for Azure where certificate details needs to be added
        if arg.cloud == "azure":
            kwargs = dict()
            kwargs['kind'] = "key_azure"
            db_result = cls.cm.find(**kwargs)
            # pprint("Key DB results")
            key_result = None
            try:
                for key in db_result:
                    if key['name'] == arg.key:
                        pprint("Found the key")
                        key_result = key
                        break
                if key_result is not None:
                    new_dict_items = dict()
                    new_dict_items['cert_thumbprint'] = key_result['fingerprint']
                    new_dict_items['pub_key_path'] = key_result['key_path']
                    new_dict_items['cert_path'] = key_result['certificate']
                    new_dict_items['pfx_path'] = key_result['pfx_path']
                    basic_dict.update(new_dict_items)
                else:
                    pprint("None found in DB")
            except:
                traceback.print_exc()
                pprint("Exception while processing azure boot arguments")
        d = dotdict(basic_dict)

        Console.ok("Machine {name} is being booted on cloud {cloud} ...".format(**arg))

        print(Printer.attribute(d))

        vm = cloud_provider.boot_vm(**d)
        if vm is not None:
            cls.refresh(cloud=arg.cloud)

            cls.cm.set(d.name, "key", d.key, scope="first", kind="vm")
            cls.cm.set(d.name, "image", d.image, scope="first", kind="vm")
            cls.cm.set(d.name, "flavor", d.flavor, scope="first", kind="vm")
            cls.cm.set(d.name, "group", arg.group, scope="first", kind="vm")
            cls.cm.set(d.name, "user", arg.user, scope="first", kind="vm")

        # update group and key
        #
        # cls.cm.update("vm", name=data.name)

        return vm

    @classmethod
    def start(cls, **kwargs):
        arg = dotdict(kwargs)
        cloud_provider = CloudProvider(arg.cloud).provider
        for server in kwargs["servers"]:
            cloud_provider.start_vm(server)
            Console.ok("Machine {:} is being started on {:} Cloud...".format(server, cloud_provider.cloud))

            # Explicit refresh called after VM start, to update db.
            # cls.refresh(cloud=kwargs["cloud"])

    @classmethod
    def stop(cls, **kwargs):
        arg = dotdict(kwargs)
        cloud_provider = CloudProvider(arg.cloud).provider
        for server in kwargs["servers"]:
            cloud_provider.stop_vm(server)
            Console.ok("Machine {:} is being stopped on {:} Cloud...".format(server, cloud_provider.cloud))

            # Explicit refresh called after VM stop, to update db.
            # cls.refresh(cloud=kwargs["cloud"])

    @classmethod
    def delete(cls, **kwargs):
        arg = dotdict(kwargs)

        force = kwargs.get("force", Default.purge)


        if "cloud" in arg:
            cloud_provider = CloudProvider(arg.cloud).provider
            for server in kwargs["servers"]:
                vm = cls.cm.find(name=server, kind="vm", cloud=arg.cloud, scope="first")
                if vm:
                    provider = vm["provider"]
                    cloud = vm["category"]

                    # If server has a floating ip associated, release it
                    server_dict = Network.get_instance_dict(cloudname=arg.cloud,
                                                            instance_id=server)
                    floating_ip = server_dict["floating_ip"]
                    if floating_ip is not None:
                        Network.disassociate_floating_ip(cloudname=arg.cloud,
                                                         instance_name=server,
                                                         floating_ip=floating_ip)
                    cloud_provider.delete_vm(server)
                    if force:
                        cls.cm.delete(kind="vm",
                                      provider=provider,
                                      category=cloud,
                                      name=server)  # delete the record from db
                        Console.ok("VM record {:} is being deleted from the local database..." \
                                   .format(server))

                    else:
                        cls.cm.set(server, "status", "deleted", kind="vm", scope="first")

                    # Console.ok("VM {:} is being deleted on {:} cloud...".format(server, cloud_provider.cloud))
                else:
                    Console.error("VM {:} can not be found.".format(server), traceflag=False)
        else:

            clouds = set()
            for server in arg.servers:

                vm = cls.cm.find(kind="vm", name=server, scope="first")
                if vm:
                    cloud = vm["category"]
                    provider = vm["provider"]
                    cloud_provider = CloudProvider(cloud).provider
                    clouds.add(cloud)
                    cloud_provider.delete_vm(server)
                    if force:
                        cls.cm.delete(kind="vm",
                                      provider=provider,
                                      category=cloud,
                                      name=server)
                        Console.ok("VM record {:} is being deleted from the local database..." \
                                   .format(server))

                    else:
                        cls.cm.set(server, "status", "deleted", kind="vm", scope="first")

                    # Console.ok("VM {:} is being deleted on {:} cloud...".format(server, cloud))
                else:
                    Console.error("VM {:} can not be found.".format(server), traceflag=False)


    @classmethod
    def get_vms_by_name(cls, name, cloud):

        vm_data = cls.cm.find(kind="vm", name=name, category=cloud)
        if vm_data is None or len(vm_data) == 0:
            raise RuntimeError("VM data not found in database.")
        return vm_data

    @classmethod
    def rename(cls, **kwargs):

        arg = dotdict(kwargs)

        cloud_provider = CloudProvider(kwargs["cloud"]).provider

        # Check for vms with duplicate names in DB.
        vms = cls.get_vms_by_name(name=arg.oldname, cloud=arg.cloud)

        if len(vms) > 1:
            users_choice = "y"

            if not arg.force:
                print("More than 1 vms found with the same name as {}.".format(server))
                users_choice = input("Would you like to auto-order the new names? (y/n): ")

            if users_choice.strip() == "y":
                count = 1
                for index in vms:
                    count_new_name = "{0}{1}".format(arg.newname, count)
                    # print(vms[index])

                    cloud_provider.rename_vm(vms[index]["uuid"], count_new_name)

                    print("Machine {0} with UUID {1} renamed to {2} on {3} cloud".format(vms[index]["name"],
                                                                                         vms[index]["uuid"],
                                                                                         count_new_name,
                                                                                         cloud_provider.cloud))
                    count += 1
            elif users_choice.strip() == "n":
                cloud_provider.rename_vm(arg.oldname, arg.newname)
                print(
                    "Machine {0} renamed to {1} on {2} Cloud...".format(arg.oldname, arg.newname, cloud_provider.cloud))
            else:
                Console.error("Invalid Choice.")
                return
        else:
            cloud_provider.rename_vm(arg.oldname, arg.newname)
            print("Machine {0} renamed to {1} on {2} Cloud...".format(arg.oldname, arg.newname, cloud_provider.cloud))

        # Explicit refresh called after VM rename, to update db.
        cls.refresh(cloud=arg.cloud)

    @classmethod
    def info(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    def list(cls, **kwargs):
        """
        This method lists all VMs of the cloud
        """

        arg = dotdict(kwargs)
        if "name" in arg:
            arg.name = arg.name

        arg.output = arg.output or 'table'

        # pprint (kwargs)
        # prevent circular dependency
        def vm_groups(vm):
            """

            :param vm: name of the vm
            :return: a list of groups the vm is in
            """

            try:
                query = {
                    'kind': "group",
                    'provider': 'general',
                    "species": "vm",
                    "member": vm,
                    "scope": 'all',
                    "output": 'dict'
                }

                d = cls.cm.find(**query)
                groups_vm = set()
                if d is not None and len(d) > 0:
                    for vm in d:
                        groups_vm.add(vm['name'])
                return list(groups_vm)
            except Exception as ex:
                Console.error(ex.message)
            return []

        try:
            if "name" in arg and arg.name is not None:
                if cls.isUuid(arg.name):
                    elements = cls.cm.find(kind="vm",
                                           category=arg.category,
                                           uuid=arg.name)
                else:
                    elements = cls.cm.find(kind="vm",
                                           category=arg.category,
                                           label=arg.name)
            else:
                elements = cls.cm.find(kind="vm",
                                       category=arg.category)

            if elements is None or len(elements) == 0:
                return None

            for elem in elements:
                element = elem
                name = element["name"]
                groups = vm_groups(name)
                element["group"] = ','.join(groups)

            # print(elements)

            # order = ['id', 'uuid', 'name', 'cloud']
            (order, header) = CloudProvider(arg.category).get_attributes("vm")

            # order = None
            if "name" in arg and arg.name is not None:
                return Printer.attribute(elements[0],
                                         output=arg.output)
            else:
                return Printer.write(elements,
                                     order=order,
                                     output=arg.output)
        except Exception as ex:
            Console.error(ex.message)

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
        vm = cloud_provider.get_vm(name=kwargs["name"])
        return vm["status"]

    @classmethod
    def set_login_user(cls, name=None, cloud=None, username=None):

        # cls.cm.set(name, "username", username, kind="vm", scope="first")

        vm = Vm.get(name, category=cloud)

        if vm is None:
            Console.error("VM could not be found", traceflag=False)
            return
        else:
            cls.cm.update(kind="vm",
                          provider=vm["provider"],
                          filter={'name': name},
                          update={"username": username}
                          )

    @classmethod
    def get_login_user(cls, name, cloud):
        print(name, cloud)

        Console.error("this method is wrong implemented")

        '''
        if cls.isUuid(name):
            uuid = name
        else:
            vm_data = cls.cm.find(kind="vm", category=cloud, label=name)
            if vm_data is None or len(vm_data) == 0:
                raise RuntimeError("VM with label {} not found in database.".format(name))
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
