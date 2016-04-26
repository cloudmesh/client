import os
from pprint import pprint
from uuid import UUID
from azure.servicemanagement import *
from cloudmesh_client.common.ConfigDict import Config, ConfigDict
from cloudmesh_client.common.AzureDict import AzureDict
from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase


class CloudProviderAzure(CloudProviderBase):

    def __init__(self, cloud_name, cloud_details, user=None, flat=True):
        super(CloudProviderAzure, self).__init__(cloud_name, user=user)
        pprint("AZURE PROVIDER YAYYYY")
        self.cloud_type = "azure"
        self.kind = ["vm"]
        self.dbobject = ["azure_vm"]
        self.provider = self.initialize()

    def initialize(self):
        confd = ConfigDict("cloudmesh.yaml")
        cloudcred = confd['cloudmesh']['clouds']['azure']['credentials']
        subscription_id = cloudcred['subscriptionid']
        certificate_path = cloudcred['managementcertfile']

        pprint("subscriptionid:"+subscription_id)
        pprint("certificate_path:"+certificate_path)
        sms = ServiceManagementService(subscription_id, certificate_path)
        return sms

    def list_vm(self, cloudname, **kwargs):
        # return self.list(self.provider.list_nodes, cloudnames, kwargs)
        pprint("In list_vm for Azure")
        result = self.provider.list_hosted_services()
        vm_dict_list = []
        for hosted_service in result:
            print('----------Service name: ' + hosted_service.service_name)
            pprint("Detail of:" + hosted_service.service_name)
            hosted_service_detail = self.provider.get_hosted_service_properties(hosted_service.service_name, embed_detail=True)
            for key, deployment in enumerate(hosted_service_detail.deployments):
                print("Dict of the VM Object", key)
                vm_dict = AzureDict.convert_to_vm_dict(hosted_service, deployment)
                vm_dict_list.append(vm_dict)
        return self._to_dict(vm_dict_list)

    def _to_dict(self, dict_list):
        final_dict = dict()
        for index, result_dict in enumerate(dict_list):
            pprint("index"+str(index))
            final_dict[index] = result_dict
        return final_dict


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
            }
        }

        if kind in layout:
            order = layout[kind]['order']
            header = layout[kind]['header']
        else:
            order = None
            header = None

        return order, header