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

    uuid = Column(String)
    affinity_group = Column(String)
    category = Column(String)
    description = Column(String)
    location = Column(String)
    media_link = Column(String)
    os = Column(String)
    vm_image = Column(String)
    id = Column(String)

    def __init__(self,
                 **kwargs):
        super(IMAGE_LIBCLOUD, self).set_defaults(**kwargs)

        self.uuid = kwargs.get('uuid')
        self.affinity_group = kwargs.get('affinity_group')
        self.category = kwargs.get('category')
        self.description = kwargs.get('description')
        self.location = kwargs.get('location')
        self.media_link = kwargs.get('media_link')
        self.os = kwargs.get('os')
        self.vm_image = kwargs.get('vm_image')
        self.id = kwargs.get('id')

# noinspection PyPep8Naming
class FLAVOR_AZURE(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "flavor_azure"

    __kind__ = 'flavor'
    __provider__ = "azure"

    uuid = Column(String)
    bandwidth = Column(String)
    disk = Column(String)
    driver = Column(String)
    extra = Column(String)
    cores = Column(String)
    max_data_disks = Column(String)
    id = Column(String)
    name = Column(String)
    price = Column(String)
    ram = Column(String)

    def __init__(self,
                 **kwargs):
        super(FLAVOR_LIBCLOUD, self).set_defaults(**kwargs)

        self.uuid = kwargs.get('uuid')
        self.bandwidth = kwargs.get('bandwidth')
        self.disk = kwargs.get('disk')
        self.driver = kwargs.get('driver')
        self.extra = kwargs.get('extra')
        self.cores = kwargs.get('cores')
        self.max_data_disks = kwargs.get('max_data_disks')
        self.id = kwargs.get('id')
        self.price = kwargs.get('price')
        self.ram = kwargs.get('ram')




