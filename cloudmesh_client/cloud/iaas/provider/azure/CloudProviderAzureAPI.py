from __future__ import print_function
from azure.servicemanagement import *
from pprint import pprint
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.cloud.iaas.provider.azure.AzureDict import AzureDict
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase
import base64
import sys
import traceback

class CloudProviderAzureAPI(CloudProviderBase):

    def __init__(self, cloud_name, cloud_details, user=None):
        super(CloudProviderAzureAPI, self).__init__(cloud_name, user=user)
        self.cloud_type = "azure"
        self.kind = ["image", "flavor", "vm"]
        self.provider = None
        self.default_image = None
        self.default_flavor = None
        self.cloud = None
        self.cloud_details = None
        self.initialize(cloud_name, cloud_details)

    def initialize(self, cloudname, user=None):
        """
        reads the details for the initialization from the cloudname defined in the yaml file
        Azure cloud requires subscription_id and service management certificate to initialize the provider
        :param cloudname:
        :param user:
        :return:
        """
        confd = ConfigDict("cloudmesh.yaml")
        cloudcred = confd['cloudmesh']['clouds']['azure']['credentials']
        subscription_id = cloudcred['subscriptionid']
        certificate_path = cloudcred['managementcertfile']
        pprint("subscriptionid:"+subscription_id)
        pprint("certificate_path:"+certificate_path)
        self.provider = ServiceManagementService(subscription_id, certificate_path)
        self.default_image = confd['cloudmesh']['clouds']['azure']['default']['image']
        self.default_flavor = confd['cloudmesh']['clouds']['azure']['default']['flavor']
        self.cloud = "azure"
        self.cloud_details = confd['cloudmesh']['clouds']['azure']

    def _to_dict(self, dict_list):
        final_dict = dict()
        for index, result_dict in enumerate(dict_list):
            # pprint("index"+str(index))
            final_dict[index] = result_dict
        return final_dict

    def list_flavor(self, cloudname, **kwargs):
        result = self.provider.list_role_sizes()
        flavor_dict_list = []
        for index, role_size in enumerate(result):
            # print("SIZE ", index)
            flavor_dict = AzureDict.convert_to_flavor_dict(role_size)
            flavor_dict_list.append(flavor_dict)
        return self._to_dict(flavor_dict_list)

    def list_image(self, cloudname, **kwargs):
        result = self.provider.list_os_images()
        image_dict_list = []
        for index, image in enumerate(result):
            # print("IMAGE ", index)
            image_dict = AzureDict.convert_to_image_dict(image)
            image_dict_list.append(image_dict)
        return self._to_dict(image_dict_list)

    def list_vm(self, cloudname, **kwargs):
        """
            List the VMs or Deployments in Azure Cloud
        :param cloudname:
        :param kwargs:
        :return:
        """
        # pprint("In list_vm for Azure")
        result = self.provider.list_hosted_services()
        vm_dict_list = []
        for hosted_service in result:
            pprint("Detail of:" + hosted_service.service_name)
            hosted_service_detail = self.provider.get_hosted_service_properties(hosted_service.service_name, embed_detail=True)
            for key, deployment in enumerate(hosted_service_detail.deployments):
                # print("Dict of the VM Object", key)
                vm_dict = AzureDict.convert_to_vm_dict(hosted_service, deployment)
                vm_dict_list.append(vm_dict)
        return self._to_dict(vm_dict_list)

    def list_secgroup_rules(self, cloudname):
        Console.TODO("not yet implemented")

    def list_secgroup(self, cloudname):
        Console.TODO("not yet implemented")

    def add_certificate(self, service_name, certificate_path):
        """

        :param service_name: Hosted service name in Azure cloud to which the certificate needs to be added
        :param certificate_path: PFX(PKCS encoded) certificate Path
        :return:
        """
        with open(certificate_path, "rb") as bfile:
            print("Adding the PFX certificate")
            cert_data = base64.b64encode(bfile.read())
            cert_format = 'pfx'
            cert_password = ''
            cert_res = self.provider.add_service_certificate(service_name=service_name,
                                data=cert_data,
                                certificate_format=cert_format,
                                password=cert_password)
            print(cert_res)
            self.provider.wait_for_operation_status(cert_res.request_id, timeout=30)

    def _get_storage_name(self):
        """
            Fetches the default storage service name from the Azure cloud
        :return:
        """
        result = self.provider.list_storage_accounts()
        if len(result) > 0:
            print("storage_service_name found ", result[0].service_name)
            return result[0].service_name
        Console.error("No Storage Accounts found")
        return None

    def boot_vm(self,
                name,
                group=None,
                image=None,
                flavor=None,
                cloud=None,
                cert_thumbprint=None,
                pub_key_path=None,
                cert_path=None,
                pfx_path=None,
                secgroup=None,
                meta=None,
                nics=None,
                **kwargs):
        """
            Boots up a new VM Instance.
            Steps involved: creating a hosted(Cloud) Service, adding the PFX certificate file,
            get default storage name, creating a configuration set, adding an endpoint(SSH by default),
            and finally creating a VM deployment

        :param name: Hosted Service Name and VM instance name
        :param group:
        :param image:
        :param flavor:
        :param cloud:
        :param cert_thumbprint:
        :param pub_key_path:
        :param cert_path:
        :param pfx_path:
        :param secgroup:
        :param meta:
        :param nics:
        :param kwargs:
        :return:
        """
        location = ConfigDict(filename="cloudmesh.yaml")["cloudmesh"]["clouds"]["azure"]["default"]["location"] or 'Central US'
        try:
            self.provider.create_hosted_service(service_name=name,
                                    label=name,
                                    location=location)
        except:
            traceback.print_exc()
            pprint("Error creating hosted service")
        pprint("service name"+name)
        pprint("location name"+location)
        pprint("cert_thumbprint"+cert_thumbprint)
        pprint("pub_key_path"+pub_key_path)
        pprint("cert_path"+cert_path)
        pprint("pfx_path"+pfx_path)
        pprint("Image"+image)
        pprint("Flavor"+flavor)
        pprint("Certificate adding")
        self.add_certificate(name, pfx_path)
        pprint("Certificate added")
        storage_name = self._get_storage_name()
        media_link = 'https://{0}.blob.core.windows.net/vhds/{1}.vhd'.format(
                        storage_name,
                        name)
        os_hd = OSVirtualHardDisk(image, media_link)

        username = ConfigDict(filename="cloudmesh.yaml")["cloudmesh"]["clouds"]["azure"]["default"]["username"]
        password = ConfigDict(filename="cloudmesh.yaml")["cloudmesh"]["clouds"]["azure"]["default"]["password"]
        pprint("Username:"+username)
        pprint("password:"+password)

        # TODO: current case handles only for linux guest VMs, implementation needed for Windows VMs
        linux_config = LinuxConfigurationSet(name, username, password, False)
        linux_config.ssh = SSH()
        public_key = PublicKey(cert_thumbprint, pub_key_path)
        linux_config.ssh.public_keys.public_keys.append(public_key)
        pair = KeyPair(cert_thumbprint, cert_path)
        linux_config.ssh.key_pairs.key_pairs.append(pair)

        # Endpoint configuration
        network = ConfigurationSet()
        network.configuration_set_type = 'NetworkConfiguration'
        network.input_endpoints.input_endpoints.append(
            ConfigurationSetInputEndpoint('SSH', 'tcp', '22', '22'))

        print("Starting the VM on ", media_link)
        try:
            vm_create_result = self.provider.create_virtual_machine_deployment(service_name=name,
            deployment_name=name,
            deployment_slot='production',
            label=name,
            role_name=name,
            system_config=linux_config,
            os_virtual_hard_disk=os_hd,
            network_config=network,
            role_size=flavor)
            # pprint(vm_create_result)
            self.provider.wait_for_operation_status(vm_create_result.request_id, timeout=30)
            Console.info("VM boot up successful.ok.")
        except:
            traceback.print_exc()
            pprint("Exception in starting the VM")
        return name

    def get_ips(self, name, group=None, force=None):
        """
        Returns the ip of the instance indicated by name
        :param name:
        :param group:
        :param force:
        :return: IP address of the instance
        """
        pprint("In get_ips::")
        result = self.provider.list_hosted_services()
        for hosted_service in result:
            # pprint("Detail of:" + hosted_service.service_name)
            hosted_service_detail = self.provider.get_hosted_service_properties(hosted_service.service_name, embed_detail=True)
            for key, deployment in enumerate(hosted_service_detail.deployments):
                vm_dict = AzureDict.convert_to_vm_dict(hosted_service, deployment)
                instance_name = vm_dict['instance_name']
                if instance_name == name:
                    vip_list = []
                    vip_list.append(vm_dict['public_ips'])
                    return vip_list
        return None

    def delete_vm(self, name, group=None, force=None):
        """
            Delete a VM instance whose hosted service name and instance name is given by name
        :param name:
        :param group:
        :param force:
        :return:
        """
        self.provider.delete_deployment(service_name=name,
                                        deployment_name=name)
        self.provider.delete_hosted_service(service_name=name)
        Console.info("Delete Success.ok.")

    def assign_ip(self, name):
        Console.TODO("not yet implemented")

    def attributes(self, kind):
        layout = {
            'vm': {
                'order': [
                    'id',
                    'uuid',
                    'label',
                    'status',
                    'public_ips',
                    'private_ips',
                    'image_name',
                    'key',
                    'availability',
                    'instance_type',
                    'user',
                    'category',
                    'updated_at'
                ],
                'header': [
                    'id',
                    'uuid',
                    'label',
                    'status',
                    'public_ips',
                    'private_ips',
                    'image_name',
                    'key',
                    'availability',
                    'instance_type',
                    'user',
                    'cloud',
                    'updated'
                ]
            },
            'image': {
                'order': [
                    'uuid',
                    'affinity_group',
                    'category',
                    'label',
                    'media_link',
                    'os',
                    'vm_image',
                    'image_family'
                ],
                'header': [
                    'uuid',
                    'affinity_group',
                    'category',
                    'label',
                    'media_link',
                    'os',
                    'vm_image',
                    'image_family'
                ]
            },
            'flavor': {
                'order': [
                    'uuid',
                    'label',
                    'web_worker_resource_disk_size',
                    'virtual_machine_resource_disk_size',
                    'ram',
                    'cores',
                    'max_data_disks'
                ],
                'header': [
                    'uuid',
                    'label',
                    'web_worker_resource_disk_size',
                    'virtual_machine_resource_disk_size',
                    'ram',
                    'cores',
                    'max_data_disks'
                ]
            }
        }

        if kind in layout:
            order = layout[kind]['order']
            header = layout[kind]['header']
        else:
            order = None
            header = None

        return order, header
    #
    # All other must methods defined bellow so we can discuss
    #
