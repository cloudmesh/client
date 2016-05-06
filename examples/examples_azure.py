from __future__ import print_function
from azure import *
from azure.servicemanagement import *
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.FlatDict2 import FlatDict2
import base64
from pprint import pprint

confd = ConfigDict("cloudmesh.yaml")
cloudcred = confd['cloudmesh']['clouds']['azure']['credentials']
clouddefault = confd['cloudmesh']['clouds']['azure']['default']

subscription_id = cloudcred['subscriptionid']
certificate_path = cloudcred['managementcertfile']


## Need to check on how to automate the process of certificate creation
pprint("subscriptionid:"+subscription_id)
pprint("certificate_path:"+certificate_path)

sms = ServiceManagementService(subscription_id, certificate_path)
pprint("sms:")
pprint(sms)


result = sms.list_locations()
for location in result:
    print(location.name)

pprint("===========VM LIST============")

## http://azure-sdk-for-python.readthedocs.org/en/latest/_modules/azure/servicemanagement/models.html#HostedService
result = sms.list_hosted_services()

for hosted_service in result:
    print('----------Service name: ' + hosted_service.service_name)
    pprint("Detail of:" + hosted_service.service_name)
    hosted_service_detail = sms.get_hosted_service_properties(hosted_service.service_name, embed_detail=True)
    pprint("PRINITNG FLATDICT")
    flat_dict = FlatDict2.convert(hosted_service_detail, False)
    # pprint(flat_dict)
    pprint("=======ENd PRINITNG FLATDICT")

    # flat_dict = _to_dict(hosted_service_detail)

    for key, deployment in enumerate(hosted_service_detail.deployments):
        print("Dict of the VM Object", key)

        # dictAA = FlatDict2.convert(deployment)

        # dictAA = object_to_dict(deployment)
        # pprint(dictAA)
        # print("Flattened Dict of VM")
        # pprint(FlatDict(dictAA))


    # pprint(hosted_service_detail.deployments)
    # for deployment in hosted_service_detail.deployments:
    #     pprint("deployment_slot: "+deployment.deployment_slot)
    #     pprint("status: "+deployment.status)
    #     pprint("virtual_network_name: "+deployment.virtual_network_name)
    #     pprint("configuration: "+deployment.configuration)
    #     pprint("Extended:")
    #     pprint(deployment.extended_properties)
    #
    #     for role in deployment.role_list:
    #         pprint("Role name:"+role.role_name)
    #         pprint("Role role_type:"+role.role_type)
    #         pprint("Role os_version:"+role.os_version)
    #         pprint("Role role_size:"+role.role_size)
    #         pprint("Role image name:"+role.os_virtual_hard_disk.source_image_name)
    #         pprint("Role image media_link:"+role.os_virtual_hard_disk.media_link)
    #         pprint("Role image host_caching:"+role.os_virtual_hard_disk.host_caching)
    #         if role.os_virtual_hard_disk.disk_label:
    #             pprint("Role image disk_label:"+role.os_virtual_hard_disk.disk_label)
    #         if role.os_virtual_hard_disk.os:
    #             pprint("Role image os:"+role.os_virtual_hard_disk.os)
    #         if role.os_virtual_hard_disk.remote_source_image_link:
    #             pprint("Role image remote_source_image_link:"+role.os_virtual_hard_disk.remote_source_image_link)
    #     for role_instance in deployment.role_instance_list:
    #         pprint("Instance Name:"+role_instance.instance_name)
    #         pprint("Instance Size:"+role_instance.instance_size)
    #         pprint("Instance state details:"+role_instance.instance_state_details)
    #         # pprint("Instance upgarde  details:"+role_instance.instance_upgrade_domain)
    #     for virtual_ip in deployment.virtual_ips:
    #         pprint("virtual IP: "+virtual_ip.address)
    #
    # print('Management URL: ' + hosted_service.url)
    # print('Location: ' + hosted_service.hosted_service_properties.location)
    # print('')

pprint("=======IMAGES=======")

### IMAGES
# result = sms.list_operating_systems()


result = sms.list_os_images()

for index, image in enumerate(result):
    print("IMAGE ", index)
    # print(FlatDict2.convert(image), False)
# ## class OSImage
#
# result = sms.list_os_images()
#
# for image in result:
#     print('-------Name: ' + image.name)
#     print('Label: ' + image.label)
#     print('OS: ' + image.os)
#     print('OS Image family: ' + image.image_family)
#     print('Category: ' + image.category)
#     print('Description: ' + image.description)
#     print('Location: ' + image.location)
#     print('Media link: ' + image.media_link)
#
#     print('publisher_name: ' + image.publisher_name)
#     print('os_state:'+image.os_state)
#     print('eula:'+image.eula)
#     print('')


### SIZES

##### class RoleSize
pprint("============SIZES===========")
result = sms.list_role_sizes()

for index, role_size in enumerate(result):
    print("SIZE ", index)
    print(FlatDict2.convert(role_size), False)
    # print(object_to_dict(role_size))

# for role_size in result:
#     print('------Name: ' + role_size.name)
#     print('Label: ' + role_size.label)
#     print('Cores:', role_size.cores)
#     print('Memory: ', role_size.memory_in_mb)
#     print('supported_by_virtual_machines: ', role_size.supported_by_virtual_machines)
#     print('max_data_disk_count: ', role_size.max_data_disk_count)


#### STORAGE
pprint("============STORAGE===========")
result = sms.list_storage_accounts()

storage_service_name = ""
for storage_service in result:

    print("STORAGE ", index)
    storage_dict = FlatDict2.convert(storage_service)
    print(storage_dict, False)
    storage_service_name = storage_dict['service_name']
    # print(object_to_dict(storage_service))

    # print('------service_name: ' + storage_service.service_name)
    # storage_service_name = storage_service.service_name
    # print('URL: ' + storage_service.url)
    # print('Storage Service Location:', storage_service.storage_service_properties.location)

###### Create VM

def create_vm(sms, storage_name  = "default_storage", os_disk_name = "test-disk-name"):


    name = 'sup-vm-ssh-3'
    location = 'Central US'
    sms.create_hosted_service(service_name=name,
                                label=name,
                                location=location)

    # Add the certificate to the hosted service
    cert_data_path = "/Users/supreeth/.ssh/azure/mycer.pfx"
    with open(cert_data_path, "rb") as bfile:
        print("Adding the certificate")
        cert_data = base64.b64encode(bfile.read())
        cert_format = 'pfx'
        cert_password = ''
        cert_res = sms.add_service_certificate(service_name=name,
                            data=cert_data,
                            certificate_format=cert_format,
                            password=cert_password)
        print(cert_res)
        sms.wait_for_operation_status(cert_res.request_id, timeout=30)



    pprint("---------CREATING A NEW VM-------")
    #Set the location


    # Name of an os image as returned by list_os_images
   # image_name = 'OpenLogic__OpenLogic-CentOS-62-20120531-en-us-30GB.vhd'

    image_name = 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-12_04_5-LTS-amd64-server-20160315-en-us-30GB'
    # Destination storage account container/blob where the VM disk
    # will be created
    media_link='https://{0}.blob.core.windows.net/vhds/{1}.vhd'.format(
                        storage_name,
                        os_disk_name,
                    )
    print("Hosting on media link", media_link)
    # Linux VM configuration, you can use WindowsConfigurationSet
    # for a Windows VM instead

    SERVICE_CERT_THUMBPRINT = '97A9EAB9903EBDD0775B3D3BD1780271988B4224'
    linux_config = LinuxConfigurationSet('sup-vm-ssh-2', 'azureuser', 'password', True)
    linux_config.ssh = SSH()
    public_key = PublicKey(SERVICE_CERT_THUMBPRINT, '/Users/supreeth/.ssh/azure/mycer.pub')
    linux_config.ssh.public_keys.public_keys.append(public_key)
    pair = KeyPair(SERVICE_CERT_THUMBPRINT, '/Users/supreeth/.ssh/azure/mycer.pem')
    linux_config.ssh.key_pairs.key_pairs.append(pair)


    os_hd = OSVirtualHardDisk(image_name, media_link)


    # Endpint configuration
    network = ConfigurationSet()
    network.configuration_set_type = 'NetworkConfiguration'
    network.input_endpoints.input_endpoints.append(
        ConfigurationSetInputEndpoint('SSH', 'tcp', '22', '22'))



    sms.create_virtual_machine_deployment(service_name=name,
    deployment_name=name,
    deployment_slot='production',
    label=name,
    role_name=name,
    system_config=linux_config,
    os_virtual_hard_disk=os_hd,
    network_config=network,
    role_size='Basic_A1')






create_vm(sms, storage_service_name, 'test-disk-2')