from __future__ import print_function
from ..CloudmeshDatabase import CloudmeshDatabase, CloudmeshMixin
from sqlalchemy import Column, Date, Integer, String

'''
Azure via libcloud
=====

Azure Image
-----------

    {'_uuid': None,
     'driver': <libcloud.compute.drivers.azure.AzureNodeDriver object at 0x7f4b69e32cd0>,
     'extra': {'affinity_group': '',
               'category': u'Public',
               'description': u"Linux VM image with coreclr-x64-beta5-11624 installed to /opt/dnx. This image is based on Ubuntu 14.04 LTS, with prerequisites of CoreCLR installed. It also contains PartsUnlimited demo app which runs on the installed coreclr. The demo app is installed to /opt/demo. To run the demo, please type the command '/opt/demo/Kestrel' in a terminal window. The website is listening on port 5004. Please enable or map a endpoint of HTTP port 5004 for your azure VM.",
               'location': u'East Asia;Southeast Asia;Australia East;Australia Southeast;Brazil South;North Europe;West Europe;Japan East;Japan West;Central US;East US;East US 2;North Central US;South Central US;West US',
               'media_link': '',
               'os': u'Linux',
               'vm_image': False},
     'id': '03f55de797f546a1b29d1b8d66be687a__CoreCLR-x64-Beta5-Linux-PartsUnlimited-Demo-App-201504.29',
     'name': u'CoreCLR x64 Beta5 (11624) with PartsUnlimited Demo App on Ubuntu Server 14.04 LTS'}

Azure Size
----------

    {'_uuid': None,
     'bandwidth': None,
     'disk': 127,
     'driver': <libcloud.compute.drivers.azure.AzureNodeDriver object at 0x7f4b69e32cd0>,
     'extra': {
        'cores': 16,
        'max_data_disks': 32},
     'id': 'Standard_D14',
     'name': 'D14 Faster Compute Instance',
     'price': '1.6261',
     'ram': 114688}


'''


# noinspection PyPep8Naming
class IMAGE_AZURE(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "image_azure"

    __kind__ = 'image'
    __provider__ = "azure"

    uuid = Column(String)               # name
    affinity_group = Column(String)     # affinity_group
    category = Column(String)           # category
    label = Column(String)              # label
    description = Column(String)        # description
    location = Column(String)           # location
    media_link = Column(String)         # media_link
    os = Column(String)                 # os
    vm_image = Column(String)           # name
    image_family = Column(String)       # image_family

    def __init__(self,
                 **kwargs):
        super(IMAGE_AZURE, self).set_defaults(**kwargs)

        self.uuid = kwargs.get('name')
        self.affinity_group = kwargs.get('affinity_group')
        self.category = kwargs.get('category')
        self.label = kwargs.get('label')
        self.description = kwargs.get('description')
        self.location = kwargs.get('location')
        self.media_link = kwargs.get('media_link')
        self.os = kwargs.get('os')
        self.vm_image = kwargs.get('name')
        self.image_family = kwargs.get('image_family')


# noinspection PyPep8Naming
class FLAVOR_AZURE(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "flavor_azure"

    __kind__ = 'flavor'
    __provider__ = "azure"

    uuid = Column(String)                                       # name
    label = Column(String)                                      # label
    web_worker_resource_disk_size = Column(String)             # web_worker_resource_disk_size_in_mb
    virtual_machine_resource_disk_size = Column(String)         # virtual_machine_resource_disk_size_in_mb
    ram = Column(String)                                     # memory_in_mb
    cores = Column(String)                                      # cores
    max_data_disks = Column(String)                             # max_data_disk_count
    name = Column(String)                                       # name

    def __init__(self,
                 **kwargs):
        super(FLAVOR_AZURE, self).set_defaults(**kwargs)

        self.uuid = kwargs.get('name')
        self.label = kwargs.get("label", None)
        self.web_worker_resource_disk_size = kwargs.get("web_worker_resource_disk_size_in_mb", None)
        self.virtual_machine_resource_disk_size = kwargs.get("virtual_machine_resource_disk_size_in_mb", None)
        self.ram = kwargs.get("memory_in_mb", None)
        self.cores = kwargs.get("cores", None)
        self.max_data_disks = kwargs.get("max_data_disk_count", None)
        self.name = kwargs.get("name", None)


class VM_AZURE(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "vm_azure"

    __kind__ = 'vm'
    __provider__ = "azure"
    __mergefields__ = ["username"]

    username = Column(String)
    uuid = Column(String)                   # deployments, deployments [ private_id ]
    instance_name = Column(String)          # deployments, deployments [ name ]
    cloud_service = Column(String)          # service_name
    status = Column(String)                 # deployments, deployments [ status ]
    public_ips = Column(String)             # deployments, deployments [ virtual_ips__virtual_ips, address]
    floating_ip = Column(String)
    private_ips = Column(String)            # deployments, deployments [ role_instance_list__role_instances, ip_address]
    image_name = Column(String)             # deployments, deployments [role_list__roles[ os_virtual_hard_disk,source_image_name]]
    resource_location = Column(String)      # hosted_service_properties,hosted_service_properties,ResourceLocation
    deployment_slot = Column(String)        # deployments, deployments [ deployment_slot ]
    dns_name = Column(String)               # deployments, deployments [ url ]
    instance_size = Column(String)          # deployments, deployments [ role_instance_list__role_instances [ instance_size]]
    media_link = Column(String)             # deployments, deployments [ role_list__roles[ os_virtual_hard_disk, media_link ]]
    disk_name = Column(String)              # deployments, deployments [role_list__roles[ os_virtual_hard_disk,disk_name]]

    def __init__(self, **kwargs):
        super(VM_AZURE, self).set_defaults(**kwargs)

        self.uuid = kwargs.get("id")
        self.username = kwargs.get("username", None)
        self.instance_name = kwargs.get("instance_name", None)
        self.cloud_service = kwargs.get("cloud_service", None)
        self.status = kwargs.get("status", None)
        self.public_ips = kwargs.get("public_ips", None)
        self.floating_ip = kwargs.get("floating_ip", None)
        self.private_ips = kwargs.get("private_ips", None)
        self.image_name = kwargs.get("image_name", None)
        self.resource_location = kwargs.get("resource_location", None)
        self.deployment_slot = kwargs.get("deployment_slot", None)
        self.dns_name = kwargs.get("dns_name", None)
        self.instance_size = kwargs.get("instance_size", None)
        self.media_link = kwargs.get("media_link", None)
        self.disk_name = kwargs.get("disk_name", None)

class KEY_AZURE(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "key_azure"

    __kind__ = 'key_azure'
    __provider__ = 'azure'

    name = Column(String)
    certificate = Column(String)
    fingerprint = Column(String, unique=True)
    key_path = Column(String)
    pfx_path = Column(String)

    def __init__(self, **kwargs):
        super(KEY_AZURE, self).set_defaults(**kwargs)

        self.name = kwargs.get("name")
        self.certificate = kwargs.get("certificate")
        self.fingerprint = kwargs.get("fingerprint")
        self.key_path = kwargs.get("key_path")
        self.pfx_path = kwargs.get("pfx_path")

