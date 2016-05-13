from pprint import pprint
from cloudmesh_client.common.FlatDict2 import FlatDict2


class AzureDict(object):

    @classmethod
    def convert_to_vm_dict(cls, hosted_service_obj, deployment_obj):
        # pprint("In convert_to_vm_dict")
        vm_dict = dict()

        # option1: fetching from the objects directly
        vm_dict['id'] = deployment_obj.private_id
        vm_dict['name'] = deployment_obj.name
        vm_dict['instance_name'] = deployment_obj.name
        vm_dict['cloud_service'] = hosted_service_obj.service_name
        vm_dict['status'] = deployment_obj.status
        vm_dict['dns_name'] = deployment_obj.url
        if deployment_obj.virtual_ips is not None and len(deployment_obj.virtual_ips.virtual_ips) > 0:
            vm_dict['public_ips'] = deployment_obj.virtual_ips.virtual_ips[0].address
            # pprint((deployment_obj.virtual_ips.virtual_ips)[0].address)

        # option2: Using dict to fetch
        hosted_service_dict = FlatDict2.convert(hosted_service_obj)
        deployment_dict = FlatDict2.convert(deployment_obj)
        # pprint(deployment_dict)

        # vm_dict['id'] = deployment_dict['private_id']
        # vm_dict['name'] = deployment_dict['name']
        # vm_dict['instance_name'] = deployment_dict['name']
        # vm_dict['cloud_service'] = hosted_service_dict['service_name']
        # vm_dict['status'] = deployment_dict['status']
        # vm_dict['dns_name'] = deployment_dict['url']
        # if 'virtual_ips__virtual_ips' in deployment_dict and len(deployment_dict['virtual_ips__virtual_ips']) > 0:
        #     vm_dict['public_ips'] = deployment_dict['virtual_ips__virtual_ips'][0]['address']
        # if 'role_instance_list__role_instances' in deployment_dict and len(deployment_dict['role_instance_list__role_instances']) > 0:
        #     vm_dict['private_ips'] = deployment_dict['role_instance_list__role_instances'][0]['ip_address']
        # if 'role_list__roles' in deployment_dict and len(deployment_dict['role_list__roles']) > 0:
        #     if 'os_virtual_hard_disk' in deployment_dict['role_list__roles'][0]:
        #         vm_dict['image_name'] = deployment_dict['role_list__roles'][0]['os_virtual_hard_disk']['source_image_name']

        # vm_dict['resource_location'] = hosted_service_dict['hosted_service_properties']['hosted_service_properties']['ResourceLocation']
        return vm_dict


    @classmethod
    def convert_to_image_dict(cls, image_obj):
        image_dict = dict()
        image_dict['id'] = image_obj.name
        image_dict_values = FlatDict2.convert(image_obj)
        for key in image_dict_values:
            image_dict[key] = image_dict_values[key]
        return image_dict


    @classmethod
    def convert_to_flavor_dict(cls, flavor_obj):
        flavor_dict = dict()
        flavor_dict['id'] = flavor_obj.name
        flavor_dict_values = FlatDict2.convert(flavor_obj)
        for key in flavor_dict_values:
            flavor_dict[key] = flavor_dict_values[key]
        return flavor_dict

