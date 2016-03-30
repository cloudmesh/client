from sqlalchemy import Column, String

from ..base.model import CloudmeshMixin

from ..CloudmeshDatabase import CloudmeshDatabase


class IMAGE_LIBCLOUD(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "image_libcloud"
    __category__ = "libcloud"
    __type__ = 'image'
    
    uuid = Column(String)
    status = Column(String)
    updated = Column(String)
    created = Column(String)
    architecture = Column(String)
    description = Column(String)
    hypervisor = Column(String)
    image_id = Column(String)
    image_location = Column(String)
    image_type = Column(String)
    is_public = Column(String)
    kernel_id = Column(String)
    owner_alias = Column(String)
    owner_id = Column(String)
    platform = Column(String)
    ramdisk_id = Column(String)
    state = Column(String)
    virtualization_type = Column(String)
    kind = 'image'

    def __init__(self,
                 **kwargs):

        self.provider = "libcloud"
        self.label = kwargs["image_name"]
        self.category = kwargs["category"] or "general"
        if kwargs['user'] is None:
            self.user = CloudmeshDatabase.user
        else:
            self.user = kwargs['user']
        self.uuid = kwargs["uuid"]
        if 'image_name' in kwargs:
            self.name = kwargs['image_name']
        if 'status' in kwargs:
            self.status = kwargs.get('status')
        if 'architecture' in kwargs:
            self.architecture = kwargs.get('architecture')
        if 'description' in kwargs:
            self.description = kwargs.get('description')
        if 'hypervisor' in kwargs:
            self.hypervisor = kwargs.get('hypervisor')
        if 'image_id' in kwargs:
            self.image_id = kwargs.get('image_id')
        if 'image_location' in kwargs:
            self.image_location = kwargs.get('image_location')
        if 'image_type' in kwargs:
            self.image_type = kwargs.get('image_type')
        if 'is_public' in kwargs:
            self.is_public = kwargs.get('is_public')
        if 'kernel_id' in kwargs:
            self.kernel_id = kwargs.get('kernel_id')
        if 'owner_alias' in kwargs:
            self.owner_alias = kwargs.get('owner_alias')
        if 'owner_id' in kwargs:
            self.owner_id = kwargs.get('owner_id')
        if 'platform' in kwargs:
            self.platform = kwargs.get('platform')
        if 'ramdisk_id' in kwargs:
            self.ramdisk_id = kwargs.get('ramdisk_id')
        if 'state' in kwargs:
            self.state = kwargs.get('state')
        self.type = self.__tablename__


class FLAVOR_LIBCLOUD(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "flavor_libcloud"
    __category__ = "general"
    __type__ = 'flavor'
    
    uuid = Column(String)
    flavor_id = Column(String)
    ram = Column(String)
    disk = Column(String)
    bandwidth = Column(String)
    price = Column(String)
    cpu = Column(String)
    kind = 'flavor'

    def __init__(self,
                 **kwargs):

        self.provider = "libcloud"
        self.label = kwargs["name"]
        self.category = kwargs["category"] or "general"
        self.name = kwargs["name"]
        if kwargs['user'] is None:
            self.user = CloudmeshDatabase.user
        else:
            self.user = kwargs['user']
        self.uuid = kwargs["uuid"]
        if "flavor_id" in kwargs:
            self.flavor_id = kwargs["flavor_id"]
        if "ram" in kwargs:
            self.ram = kwargs["ram"]
        if "disk" in kwargs:
            self.disk = kwargs["disk"]
        if "bandwidth" in kwargs:
            self.bandwidth = kwargs["bandwidth"]
        if "price" in kwargs:
            self.price = kwargs["price"]
        if "cpu" in kwargs:
            self.cpu = kwargs["cpu"]
        self.type = self.__tablename__


class VM_LIBCLOUD(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "vm_libcloud"
    __category__ = "general"
    __type__ = 'vm'
    
    uuid = Column(String)
    name = Column(String)
    state = Column(String)
    public_ips = Column(String)
    private_ips = Column(String)
    image_name = Column(String)
    availability = Column(String)
    image_id = Column(String)
    instance_id = Column(String)
    instance_type = Column(String)
    key = Column(String)
    private_dns = Column(String)
    root_device_name = Column(String)
    root_device_type = Column(String)
    status = Column(String)
    kind = 'vm'

    def __init__(self, **kwargs):

        self.provider = "libcloud"
        self.label = kwargs["name"]
        self.category = kwargs["category"] or "general"

        if kwargs['user'] is None:
            self.user = CloudmeshDatabase.user
        else:
            self.user = kwargs['user']
        if "node_id" in kwargs:
            self.uuid = kwargs["node_id"]
        if "name" in kwargs:
            self.name = kwargs["name"]
        if "state" in kwargs:
            self.state = kwargs["state"]
        if "public_ips" in kwargs:
            self.public_ips = kwargs["public_ips"]
        if "private_ips" in kwargs:
            self.private_ips = kwargs["private_ips"]
        if "image_name" in kwargs:
            self.image_name = kwargs["image_name"]
        if "availability" in kwargs:
            self.availability = kwargs["availability"]
        if "image_id" in kwargs:
            self.image_id = kwargs["image_id"]
        if "instance_id" in kwargs:
            self.instance_id = kwargs["instance_id"]
        if "instance_type" in kwargs:
            self.instance_type = kwargs["instance_type"]
        if "key" in kwargs:
            self.key = kwargs["key"]
        if "private_dns" in kwargs:
            self.private_dns = kwargs["private_dns"]
        if "root_device_name" in kwargs:
            self.root_device_name = kwargs["root_device_name"]
        if "root_device_type" in kwargs:
            self.root_device_type = kwargs["root_device_type"]
        if "status" in kwargs:
            self.status = kwargs["status"]
        self.type = self.__tablename__
