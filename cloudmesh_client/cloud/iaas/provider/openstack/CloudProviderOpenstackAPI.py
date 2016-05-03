import os
from pprint import pprint
from uuid import UUID

from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.common.ConfigDict import Config, ConfigDict
from cloudmesh_client.common.FlatDict import FlatDict
from keystoneclient.auth.identity import v3
from keystoneclient import session
from novaclient import client
import requests
import getpass
from cloudmesh_client.shell.console import Console

requests.packages.urllib3.disable_warnings()


# TODO: unset as not allowing to smoothly switch
def set_os_environ(cloudname):
    """Set os environment variables on a given cloudname"""
    # TODO: this has a severe bug as it is not unsetting variables
    # Also this coded duplicates in part from register
    try:
        d = ConfigDict("cloudmesh.yaml")
        credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]
        for key, value in list(credentials.items()):
            if key == "OS_CACERT":
                os.environ[key] = Config.path_expand(value)
            else:
                os.environ[key] = value
    except Exception as e:
        Console.error("problem setting env")


#
# we already have a much better convert to dict function
#


# noinspection PyPep8Naming,PyUnusedLocal,PyUnusedLocal
class CloudProviderOpenstackAPI(CloudProviderBase):
    cloud_type = "openstack"
    cloud_pwd = {}

    def __init__(self, cloud_name, cloud_details, user=None, flat=True):
        super(CloudProviderOpenstackAPI, self).__init__(cloud_name, user=user)
        self.flat = flat
        self.cloud_type = "openstack"
        self.kind = ["image", "flavor", "vm", "quota", "limits", "usage", "key", "group"]
        self.dbobject = ["image", "flavor", "vm", "quota", "limits", "usage", "key", "group"]

        self.provider = None
        self.default_image = None
        self.default_flavor = None
        self.cloud = None
        self.cloud_details = None

        self.initialize(cloud_name, cloud_details)

    def _to_dict(self, openstack_result):
        d = {}
        for index, value in enumerate(openstack_result):
            # print "---"
            d[index] = dict(value.__dict__["_info"])
            if 'links' in d[index]:
                del d[index]['links']
            if 'server__links' in d[index]:
                del d[index]['server__links']
            if 'image__links' in d[index]:
                del d[index]['image__links']
            if 'flavor__links' in d[index]:
                del d[index]['flavor__links']

            # If flat dict flag set, convert to flatdict
            if self.flat is True:
                d[index] = dict(FlatDict(d[index]).dict)
            else:
                ValueError("TODO: we only support flat for now")
        return d

    def _ksv3_auth(self, credentials):
        # auth to identity v3

        # ref: http://docs.openstack.org/developer/python-keystoneclient/api/keystoneclient.auth.identity.v3.html#keystoneclient.auth.identity.v3.Password
        allowed_params = ["auth_url",
                          "password",
                          "username",
                          "user_id",
                          "user_domain_id",
                          "user_domain_name",
                          "trust_id",
                          "domain_id",
                          "domain_name",
                          "project_id",
                          "project_name",
                          "project_domain_id",
                          "project_domain_name"]
        authdict = {}
        # always required
        authdict["auth_url"] = credentials["OS_AUTH_URL"]
        authdict["password"] = credentials["OS_PASSWORD"]

        # setting automatically all available ones
        # CAUTION: MAY be causing conflict/error.
        # e.g., for jetstream, the OS_USER_DOMAIN_ID=tacc
        # was causing error (domain not found)
        for key in credentials:
            if key.startswith("OS_"):
                newkey = key[3:].lower()
                if newkey in allowed_params:
                    authdict[newkey] = credentials[key]

        '''
        # different cloud provider may be using different set of other info
        # e.g. id or name for project, domain, etc.
        if "OS_USERNAME" in credentials:
            authdict["username"] = credentials["OS_USERNAME"]
        if "OS_USER_ID" in credentials:
            authdict["user_id"] = credentials["OS_USER_ID"]
        if "OS_PROJECT_NAME" in credentials:
            authdict["project_name"] = credentials["OS_PROJECT_NAME"]
        if "OS_PROJECT_ID" in credentials:
            authdict["project_id"] = credentials["OS_PROJECT_ID"]
        if "OS_USER_DOMAIN_NAME" in credentials:
            authdict["user_domain_name"] = credentials["OS_USER_DOMAIN_NAME"]
        elif "OS_USER_DOMAIN_ID" in credentials:
            authdict["user_domain_name"] = credentials["OS_USER_DOMAIN_ID"]
        if "OS_PROJECT_DOMAIN_NAME" in credentials:
            authdict["project_domain_name"] = credentials["OS_PROJECT_DOMAIN_NAME"]
        elif "OS_PROJECT_DOMAIN_ID" in credentials:
            authdict["project_domain_name"] = credentials["OS_PROJECT_DOMAIN_ID"]
        '''
        # pprint(authdict)

        ksauth = v3.Password(**authdict)

        return ksauth

    def logon(self, cloudname):
        """
        Logs onto a cloud
        :param cloudname:
        :return:
        """
        CloudProviderOpenstackAPI.cloud_pwd[cloudname] = {}
        d = ConfigDict("cloudmesh.yaml")
        credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]

        os_password = credentials["OS_PASSWORD"]
        if os_password.lower() == "readline":
            os_password = getpass.getpass()
        elif os_password.lower() == "env":
            os_password = os.environ.get("OS_PASSWORD", getpass.getpass())

        #
        # TODO: pwd is not standing for passwd
        #
        CloudProviderOpenstackAPI.cloud_pwd[cloudname]["pwd"] = os_password
        CloudProviderOpenstackAPI.cloud_pwd[cloudname]["status"] = "Active"

        return

    def activate(self, cloudname):
        """
        Activates a cloud
        :param cloudname:
        :return:
        """
        CloudProviderOpenstackAPI.cloud_pwd[cloudname]["status"] = "Active"
        return

    def deactivate(self, cloudname):
        """
        Deactivates a cloud
        :param cloudname:
        :return:
        """
        CloudProviderOpenstackAPI.cloud_pwd[cloudname]["status"] = "Inactive"
        return

    def logout(self, cloudname):
        """
        Logs out from a cloud
        :param cloudname:
        :return:
        """
        CloudProviderOpenstackAPI.cloud_pwd.pop(cloudname)
        return

    def list_clouds(self):
        """
        Lists clouds
        :return:
        """
        cloud_dict = {}
        d = ConfigDict("cloudmesh.yaml")
        clouds = list(d["cloudmesh"]["clouds"].keys())
        for i, cloud in enumerate(clouds):
            if cloud in CloudProviderOpenstackAPI.cloud_pwd:
                cloud_dict[i] = {
                    "cloud": cloud,
                    "status": CloudProviderOpenstackAPI.cloud_pwd[cloud]["status"]
                }
            else:
                cloud_dict[i] = {
                    "cloud": cloud,
                    "status": "Logged Out"
                }

        return cloud_dict

    def initialize(self, cloudname, user=None):

        d = ConfigDict("cloudmesh.yaml")
        self.cloud_details = d["cloudmesh"]["clouds"][cloudname]

        # pprint(self.cloud_details)

        self.cloud = cloudname
        self.default_flavor = self.cloud_details["default"]["flavor"]
        self.default_image = self.cloud_details["default"]["image"]
        self.tenant = self.cloud_details['credentials']['OS_TENANT_NAME']
        version = 2
        credentials = self.cloud_details["credentials"]
        cert = False
        if "OS_CACERT" in credentials:
            if credentials["OS_CACERT"] is not False:
                cert = Config.path_expand(credentials["OS_CACERT"])
        auth_url = credentials["OS_AUTH_URL"]
        ksversion = auth_url.split("/")[-1]

        """
        # GitHub issue 101
        # mechanism to interactively ask for password
        # when OS_PASSWORD set as "readline",
        # or read os.environ if set as "env".
        """
        os_password = credentials["OS_PASSWORD"]
        if os_password.lower() in ["readline", "read", "tbd"]:
            os_password = getpass.getpass()
        elif os_password.lower() == "env":
            os_password = os.environ.get("OS_PASSWORD", getpass.getpass())

        if "v2.0" == ksversion:
            self.provider = client.Client(
                version,
                credentials["OS_USERNAME"],
                os_password,
                credentials["OS_TENANT_NAME"],
                credentials["OS_AUTH_URL"],
                cert)
        elif "v3" == ksversion:
            sess = session.Session(auth=self._ksv3_auth(credentials),
                                   verify=cert)
            self.provider = client.Client(2, session=sess)

    def mode(self, source):
        """
        Sets the source for the information to be returned. "db" and "cloud"
        :param source: the database can be queried in mode "db",
        the database can be bypassed in mode "cloud"
        """
        TODO.implement()

    def list_key(self, cloudname, **kwargs):

        # TODO: this needs to be move to the provider
        _keys = self._to_dict(self.provider.keypairs.list())

        for id in _keys:
            key = _keys[id]

            # key["type"], key["string"], key["comment"] = (key["keypair__public_key"] + " ").split(" ", 3)
            # key["comment"] = key["comment"].strip()
            key_segments = key["keypair__public_key"].split(" ")
            key["type"] = key_segments[0]
            key["string"] = key_segments[1]
            key["comment"] = ''
            if len(key_segments) == 3:
                key["comment"] = key_segments[2]
            elif len(key_segments) > 3:
                key["comment"] = " ".join(key_segments[2:])

        return _keys
        # return self._to_dict(self.provider.keypairs.list())

    def list_flavor(self, cloudname, **kwargs):
        d = self._to_dict(self.provider.flavors.list())
        return d

    def list_image(self, cloudname, **kwargs):
        d = self._to_dict(self.provider.images.list())
        for e in d:
            o = d[e]
            if 'server__links' in o:
                del o['server__links']
        return d

    def list_secgroup(self, cloudname, **kwargs):
        return self._to_dict(self.provider.security_groups.list())

    def list_secgroup_rules(self, cloudname):

        groups = self.list_secgroup(cloudname)

        rules = []

        for id in groups:
            group = groups[id]
            for rule in group["rules"]:

                if rule['ip_protocol'] is not None:

                    element = {
                        'fromPort': rule["from_port"],
                        'toPort': rule["to_port"],
                        'group': group["name"],
                        'protocol': rule['ip_protocol'],
                        'ruleid': rule['id'],
                        'groupid': rule['parent_group_id']
                    }

                    if 'cidr' in rule['ip_range']:
                        element['ipRange'] = rule['ip_range']['cidr']
                    else:
                        element['ip_range'] = None
                    rules.append(element)
        return rules

    def create_secgroup(self, secgroup_name):
        secgroup = self.provider.security_groups \
            .create(name=secgroup_name,
                    description="Security group {}".format(secgroup_name))

        return secgroup

    def add_secgroup_rule(self, **kwargs):
        rule_id = self.provider.security_group_rules.create(kwargs["uuid"],
                                                            ip_protocol=kwargs["protocol"],
                                                            from_port=kwargs["from_port"],
                                                            to_port=kwargs["to_port"],
                                                            cidr=kwargs["cidr"])
        return rule_id

    def delete_secgroup(self, name):
        ret = None
        groups = self.provider.security_groups.list()

        if groups is not None:
            for sec_group in groups:

                # delete the secgroup in the cloud
                if sec_group.name == name:
                    try:
                        ret = self.provider.security_groups.delete(sec_group)
                        Console.msg("Secgroup delete: {} {}".format(sec_group.name, sec_group.__dict__["id"]))
                    except Exception as e:
                        Console.error(e.message, traceflag=False)
                        Console.error("Secgroup delete: {}".format(sec_group.name), traceflag=False)

        else:
            print("Could not find security group [{}] in cloud [{}]"
                  .format(name, self.cloud))
        return ret

    def delete_secgroup_rule(self, rule_id):
        return self.provider.security_group_rules.delete(rule_id)
        #return

    def list_vm(self, cloudname, **kwargs):
        vm_dict = self._to_dict(self.provider.servers.list())

        # Extracting and modifying dict with IP details as per the model requirement.
        ip_detail_dict = dict()
        secgroup_list_dict = dict()
        for index in vm_dict:
            ip_detail_dict[index] = dict()
            ip_detail_dict[index][u"floating_ip"] = None
            ip_detail_dict[index][u"static_ip"] = None
            for key in vm_dict[index]:
                if key.startswith("addresses"):
                    for ip_detail in vm_dict[index][key]:
                        if ip_detail["OS-EXT-IPS:type"] is not None:
                            if ip_detail["OS-EXT-IPS:type"] == "fixed":
                                ip_detail_dict[index][u"static_ip"] = ip_detail["addr"]
                            elif ip_detail["OS-EXT-IPS:type"] == "floating":
                                ip_detail_dict[index][u"floating_ip"] = ip_detail["addr"]

            secgroup_list_dict[index] = ""

            sec_index = 0
            if "security_groups" in vm_dict[index]:
                for secgroup in vm_dict[index][u"security_groups"]:
                    secgroup_list_dict[index] += secgroup["name"]
                    sec_index += 1
                    # Append comma if not the last element
                    if sec_index < len(vm_dict[index]["security_groups"]):
                        secgroup_list_dict[index] += ","

        for index in vm_dict:
            vm_dict[index][u"floating_ip"] = ip_detail_dict[index]["floating_ip"]
            vm_dict[index][u"static_ip"] = ip_detail_dict[index]["static_ip"]
            vm_dict[index][u"security_ groups"] = secgroup_list_dict[index]

        for e in vm_dict:
            o = vm_dict[e]
            for link in ['server_links', 'flavor__links', 'image__links']:
                if link in o:
                    del o[link]

        return vm_dict

    def rename_vm(self, current_name, new_name):
        """
        Renames a vm.
        :param current_name:
        :param new_name:
        :return:
        """
        if self.isUuid(current_name):
            server = self.provider.servers.get(current_name)
            print("Renaming VM ({})".format(current_name))
            server.update(name=new_name)
        else:
            # server = self.provider.servers.find(name=name)
            search_opts = {
                'name': current_name,
            }
            vms = self.provider.servers.list(search_opts=search_opts)
            for vm in vms:
                print("Renaming VM ({}) : {}".format(vm.name, vm.id))
                vm.update(name=new_name)

    def list_limits(self, tenant, **kwargs):
        return self.provider.limits.get(tenant_id=tenant).__dict__["_info"]

    def list_floating_ips(self, **kwargs):
        return self._to_dict(self.provider.floating_ips.list())

    def list_floating_ip_pools(self, **kwargs):
        return self._to_dict(self.provider.floating_ip_pools.list())

    def list_quota(self, cloudname, **kwargs):
        # pprint(self.provider.__dict__)
        # pprint(dir(self.provider.quotas))
        tenant = self.cloud_details["credentials"]["OS_TENANT_NAME"]
        # print (tenant)
        # pprint(self.provider.quotas.defaults(tenant))
        result = self.provider.quotas.defaults(tenant).__dict__["_info"]
        del result['id']
        return result

    def list_usage(self, cloudname, **kwargs):
        raise ValueError("list usage is not supported")

    def list_console(self, name, length=None):
        server = self.provider.servers.get(name)
        log = server.get_console_output(length=None)
        return log

    def boot_vm(self,
                name,
                group=None,
                image=None,
                flavor=None,
                cloud=None,
                key=None,
                secgroup=None,
                meta=None,
                nics=None,
                **kwargs):
        """
        Spawns a VM instance on the cloud.
        If image and flavor passed as none, it would consider the defaults specified in cloudmesh.yaml.

        :param name: Name of the instance to be started
        :param image: Image id to be used for the instance
        :param flavor: Flavor to be used for the instance
        :param cloud: Cloud on which to spawn the machine. Defaults to 'India'.
        :param key: Key to be used for the instance
        :param secgroup: Security group for the instance
        :param meta: A dict of arbitrary key/value metadata to store for this server
        """

        if cloud is None:
            Console.error("Cloud is not specified")
            return None

        image = image or self.default_image
        flavor = flavor or self.default_flavor

        image_id = self.get_image_id(image)
        flavor_id = self.get_flavor_id(flavor)

        # if no nics specified, try to find one in case it's needed
        if nics is None or len(nics) == 0 or (len(nics) == 1 and nics[0]['net-id'] is None):
            # get net-id based on tenant network name, and other possible
            # default network names
            netnames = ["{0}-net".format(self.tenant), "int-net"]
            nicsmy = self.provider.networks.list()
            for netname in netnames:
                nic = [x for x in nicsmy if x.label == netname]
                if len(nic) > 0:
                    # found and break out of loop
                    # use the value found here
                    nic = nic[0]
                    nics = [{"net-id": nic.id}]
                    break

        """
        create(name, image, flavor, meta=None, files=None, reservation_id=None, min_count=None, max_count=None,
          security_groups=None, userdata=None, key_name=None, availability_zone=None, block_device_mapping=None,
          block_device_mapping_v2=None, nics=None, scheduler_hints=None, config_drive=None, disk_config=None,
          admin_pass=None, access_ip_v4=None, access_ip_v6=None, **kwargs)
        """
        d = {
            "name": name,
            "image_id": image_id,
            "flavor_id": flavor_id,
            "meta": meta,
            "key_name": key,
            "security_groups": secgroup,
            "nics": nics}
        id = None
        try:
            server = self.provider.servers.create(name,
                                                  image_id,
                                                  flavor_id,
                                                  meta=meta,
                                                  key_name=key,
                                                  security_groups=secgroup,
                                                  nics=nics)
            # return the server id
            id = server.__dict__["id"]
            return id
        except Exception as e:
            if "Invalid key_name provided." in str(e):
                Console.error("Invalid key provided. "
                              "Is the key loaded, the default key set properly and uploaded to the cloud?",
                              traceflag=False)
            else:
                Console.error("Problem starting vm", traceflag=False)
                Console.error(e.message)

        return id

    def delete_vm(self, name, group=None, force=None):
        """
        Deletes a machine on the target cloud indicated by the id or name
        :param name: Name or ID of the instance to be deleted
        :param group: Security group of the instance to be deleted
        :param force: Force delete option
        :return:
        """

        if self.isUuid(name):
            server = self.provider.servers.get(name)
        else:
            # server = self.provider.servers.find(name=name)
            search_opts = {
                'name': name,
            }
            vms = self.provider.servers.list(search_opts=search_opts)
            for vm in vms:
                print("Deleting VM ({}) : {}".format(vm.name, vm.id))
                vm.delete()

    def delete_floating_ip(self, floating_ip):
        """
        Method deletes a floating IP address
        :param floating_ip:
        :return: None
        """
        return self.provider.floating_ips.delete(floating_ip)

    def start_vm(self, name, group=None, force=None):
        """
        Starts a suspended machine on the target cloud indicated by the id or name
        :param name: Name or ID of the instance to be deleted
        :param group: Security group of the instance to be deleted
        :param force: Force delete option
        :return:
        """

        if self.isUuid(name):
            server = self.provider.servers.get(name)
        else:
            server = self.provider.servers.find(name=name)

        server.start()

    def stop_vm(self, name, group=None, force=None):
        """
        Stops a machine on the target cloud indicated by the id or name
        :param name: Name or ID of the instance to be deleted
        :param group: Security group of the instance to be deleted
        :param force: Force delete option
        :return:
        """

        if self.isUuid(name):
            server = self.provider.servers.get(name)
        else:
            server = self.provider.servers.find(name=name)

        server.stop()

    def get_ips(self, name, group=None, force=None):
        """
        Returns the ip of the instance indicated by name
        :param name:
        :param group:
        :param force:
        :return: IP address of the instance
        """
        if self.isUuid(name):
            server = self.provider.servers.get(name)
        else:
            server = self.provider.servers.find(name=name)

        return self.provider.servers.ips(server)

    def get_floating_ip(self, floating_ip_id):
        """
        Returns the floating ip info associated with floating_ip_id
        :param floating_ip_id:
        :return: floating ip info
        """
        float_ip = self.provider.floating_ips.get(floating_ip_id)
        return float_ip.__dict__["_info"]

    def get_fixed_ip(self, fixed_ip_addr):
        """
        Returns the fixed ip info associated with fixed ip addr
        :param fixed_ip_addr:
        :return: fixed ip info
        """
        fixed_ip = self.provider.fixed_ips.get(fixed_ip_addr)
        return fixed_ip.__dict__["_info"]

    def reserve_fixed_ip(self, fixed_ip_addr):
        """
        Reserves a fixed ip address
        :param fixed_ip_addr:
        :return:
        """
        self.provider.fixed_ips.reserve(fixed_ip_addr)

    def unreserve_fixed_ip(self, fixed_ip_addr):
        """
        Unreserves a fixed ip address
        :param fixed_ip_addr:
        :return:
        """
        self.provider.fixed_ips.unreserve(fixed_ip_addr)

    def create_assign_floating_ip(self, server_name):
        """
        Function creates a new floating ip and associates it with the machine specified.
        :param server_name: Name of the machine to which the floating ip needs to be assigned.
        :return: Floating IP | None if floating ip already assigned.
        """
        ret = None
        allocated_ips = self.list_floating_ips()
        fip = None
        for idx, ipobj in list(allocated_ips.items()):
            if ipobj['instance_id'] is None:
                fip = ipobj['ip']
                break
        if not fip:
            float_pool = self.provider.floating_ip_pools.list()[0].name
            try:
                floating_ip = self.provider.floating_ips.create(pool=float_pool)
                fip = floating_ip.ip
            except:
                ret = "Error: No more floating ips available"
        if fip:
            server = self.provider.servers.find(name=server_name)
            try:
                server.add_floating_ip(fip)
            except Exception as e:
                print(e)
                self.provider.floating_ips.delete(floating_ip)

            ret = fip
        else:
            ret = "Error: failed to create floatingip"
        return ret

    def add_key_to_cloud(self, name, public_key):
        """
        Method to add key to cloud, typically a keypair for openstack.
        :param name: Name of the keypair.
        :param public_key: public key string.
        :return:
        """

        # print("Name=" + name)
        # print("public_key=" + public_key)

        keypair = self.provider.keypairs.create(name, public_key=public_key)
        return keypair

    def delete_key_from_cloud(self, name):
        """
        Method to delete key from cloud, typically a keypair for openstack.
        :param name: Name of the keypair.
        :return:
        """

        # print("Name=" + name)
        # print("public_key=" + public_key)

        keypair = self.provider.keypairs.delete(name)
        return keypair

    def create_floating_ip(self, float_pool):
        """
        Method creates a new floating ip under the specified pool
        :param float_pool:
        :return: Floating IP
        """
        floating_ip = self.provider.floating_ips.create(pool=float_pool)
        return floating_ip.ip

    # TODO: define this
    # noinspection PyProtectedMember,PyProtectedMember
    def get_image(self, **kwargs):

        """
        finds the image based on a query
        TODO: details TBD
        """
        name = kwargs['name']
        if self.isUuid(name):
            return self.provider.images.get(name)._info
        else:
            return self.provider.images.find(name=name)._info

    # TODO: define this
    # noinspection PyProtectedMember,PyProtectedMember
    def get_image_id(self, name):

        """
        finds the image based on a query
        TODO: details TBD
        """
        return self.get_image(name=name)["id"]

    def get_flavor_id(self, name):

        """
        finds the image based on a query
        TODO: details TBD
        """
        return self.get_flavor(id=name)["id"]

    def isUuid(self, name):
        try:
            UUID(name, version=4)
            return True
        except ValueError:
            return False

    # noinspection PyProtectedMember
    def get_flavor(self, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        if kwargs['id'].isdigit():
            pass
        else:
            kwargs['name'] = kwargs['id']
            del kwargs['id']
        return self.provider.flavors.find(**kwargs)._info

    # noinspection PyProtectedMember,PyProtectedMember
    def get_vm(self, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        vm_name = kwargs['name']
        if self.isUuid(vm_name):
            return self.provider.servers.get(vm_name)._info
        else:
            return self.provider.servers.find(name=vm_name,
                                              scope="first")._info

    def attributes(self, kind):

        layout = {
            'flavor': {
                'order': [
                    'cm_id',
                    'name',
                    #'user',
                    'ram',
                    'os_flv_disabled',
                    'vcpus',
                    'swap',
                    'os_flavor_acces',
                    'rxtx_factor',
                    'os_flv_ext_data',
                    'disk',
                    'category',
                    'updated_at'
                ],
                'header': [
                    'Id',
                    'Name',
                    #'User',
                    'RAM',
                    'Disabled',
                    'vCPUs',
                    'Swap',
                    'Access',
                    'rxtx_factor',
                    'os_flv_ext_data',
                    'Disk',
                    'Cloud',
                    'updated'
                ]
            },
            'image': {
                'order': [
                    'cm_id',
                    'name',
                    'os_image_size',
                    'metadata__description',
                    'minDisk',
                    'minRam',
                    'status',
                    'category',
                ],
                'header': [
                    'id',
                    'name',
                    'size',
                    'description',
                    'minDisk',
                    'minRam',
                    'status',
                    'cloud',
                ]
            },
            'vm': {
                'order': [
                    'cm_id',
                    'group',
                    'name',
                    'status',
                    'static_ip',
                    'floating_ip',
                    'image',
                    'flavor',
                    'username',
                    'key',
                    'project',
                    'category',
                    'updated_at',
                    'user'
                ],
                'header': [
                    'id',
                    'group',
                    'name',
                    'status',
                    'static_ip',
                    'floating_ip',
                    'username',
                    'image',
                    'flavor',
                    'key',
                    'project',
                    'cloud',
                    'updated_at',
                    'user'
                ]
            },
            'ip': {
                'order': [
                    'name',
                    'static_ip',
                    'floating_ip',
                ],
                'header': [
                    'name',
                    'static_ip',
                    'floating_ip',
                ]
            },
            'floating_ip': {
                'order': [
                    "instance_name",
                    "ip",
                    "pool",
                    "fixed_ip",
                    # "id",
                    # "instance_id",
                    'cloud'
                ],
                'header': [
                    "instance_name",
                    "floating_ip",
                    "floating_ip_pool",
                    "fixed_ip",
                    # "floating_ip_id",
                    # "instance_id",
                    'cloud'
                ],
            },
            'floating_ip_pool': {
                'order': [
                    "name"
                ],
                'header': [
                    "floating_ip_pool"
                ],
            },
            'clouds': {
                'order': [
                    "id",
                    "cloud",
                    "default",
                    "active",
                    "status",
                    "key"
                ],
                'header': [
                    "id",
                    "Cloud",
                    "Default",
                    "Active",
                    "Status",
                    "Key"
                ],
            },
            'limits': {
                'order': [
                    'Name',
                    'Value'
                ],
                'header': [
                    'Name',
                    'Value'
                ]
            },
            'quota': {
                'order': [
                    'Quota',
                    'Limit'
                ],
                'header': [
                    'Quota',
                    'Limit'
                ]
            },
            'secgroup': {
                'order': [
                    'cm_id',
                    'group',
                    'name',
                    'category',
                    'user',
                    'project',
                    'uuid'
                ],
                'header': [
                    'Id',
                    'Group'
                    'Name',
                    'Category',
                    'User',
                    'Tenant',
                    'Uuid'
                ]
            },
            'default': {
                'order': [
                    'user',
                    'category',
                    'name',
                    'value',
                    'created_at',
                    'updated_at'
                ],
                'header': [
                    'user',
                    'category',
                    'name',
                    'value',
                    'created_at',
                    'updated_at'
                ],
            },
            'group': {
                'order': [
                    "name",
                    "member",
                    "user",
                    "category",
                    "type"],
                'header': [
                    "name",
                    "member",
                    "user",
                    "category",
                    "type"]

            },
            'key': {
                'order': [
                    'category',
                    'keypair__name',
                    "type",
                    "comment",
                    "keypair__fingerprint"
                ],
                'header': [
                    "Category",
                    "Name",
                    "Type",
                    "Comment",
                    "Fingerprint"]
            }
        }

        if kind in layout:
            order = layout[kind]["order"]
            header = layout[kind]["header"]
        else:
            order = None
            header = None

        return order, header


# CloudProviderBase.register(CloudProviderOpenstackAPI)

if __name__ == "__main__":
    cloudname = 'kilo'
    d = ConfigDict("cloudmesh.yaml")
    cloud_details = d["cloudmesh"]["clouds"][cloudname]

    cp = CloudProviderOpenstackAPI(cloudname, cloud_details)

    d = {'name': '390792c3-66a0-4c83-a0d7-c81e1c787710'}
    pprint(cp.list_quota(cloudname))

    pprint(cp.list_key(cloudname))
