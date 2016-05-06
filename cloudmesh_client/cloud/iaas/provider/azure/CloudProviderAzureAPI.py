from __future__ import print_function
from azure.servicemanagement import *
from pprint import pprint
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.cloud.iaas.provider.azure.AzureDict import AzureDict
from cloudmesh_client.shell.console import Console
from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase


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
        # pprint("In list_vm for Azure")
        result = self.provider.list_hosted_services()
        vm_dict_list = []
        for hosted_service in result:
            # print('----------Service name: ' + hosted_service.service_name)
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
        Console.TODO("not yet implemented")

    def delete_vm(self, name, group=None, force=None):
        Console.TODO("not yet implemented")

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
