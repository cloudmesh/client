from ..CloudmeshDatabase import CloudmeshDatabase, CloudmeshMixin
from sqlalchemy import Column, Date, Integer, String


# noinspection PyPep8Naming
class IMAGE_LIBCLOUD(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "image_libcloud"

    __kind__ = 'image'
    __provider__ = "libcloud"
    __mergefields__ = ["username"]

    username = Column(String)
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

    def __init__(self,
                 **kwargs):
        super(IMAGE_LIBCLOUD, self).set_defaults(**kwargs)

        self.status = kwargs.get('status')
        self.architecture = kwargs.get('architecture')
        self.description = kwargs.get('description')
        self.hypervisor = kwargs.get('hypervisor')
        self.image_id = kwargs.get('image_id')
        self.image_location = kwargs.get('image_location')
        self.image_type = kwargs.get('image_type')
        self.is_public = kwargs.get('is_public')
        self.kernel_id = kwargs.get('kernel_id')
        self.owner_alias = kwargs.get('owner_alias')
        self.owner_id = kwargs.get('owner_id')
        self.platform = kwargs.get('platform')
        self.ramdisk_id = kwargs.get('ramdisk_id')
        self.state = kwargs.get('state')


# noinspection PyPep8Naming
class FLAVOR_LIBCLOUD(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "flavor_libcloud"

    __kind__ = 'flavor'
    __provider__ = "libcloud"

    uuid = Column(String)
    flavor_id = Column(String)
    ram = Column(String)
    disk = Column(String)
    bandwidth = Column(String)
    price = Column(String)
    cpu = Column(String)

    def __init__(self,
                 **kwargs):
        super(FLAVOR_LIBCLOUD, self).set_defaults(**kwargs)

        self.uuid = kwargs.get("uuid")
        self.flavor_id = kwargs.get("flavor_id")
        self.ram = kwargs.get("ram")
        self.disk = kwargs.get("disk")
        self.bandwidth = kwargs.get("bandwidth")
        self.price = kwargs.get("price")
        self.cpu = kwargs.get("cpu")


# noinspection PyPep8Naming
class VM_LIBCLOUD(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "vm_libcloud"

    __kind__ = 'vm'
    __provider__ = "libcloud"
    __mergefields__ = ["username"]

    username = Column(String)
    uuid = Column(String)
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

    def __init__(self, **kwargs):
        super(VM_LIBCLOUD, self).set_defaults(**kwargs)

        self.uuid = kwargs.get("node_id")
        self.state = kwargs.get("state")
        self.public_ips = kwargs.get("public_ips")
        self.private_ips = kwargs.get("private_ips")
        self.image_name = kwargs.get("image_name")
        self.availability = kwargs.get("availability")
        self.image_id = kwargs.get("image_id")
        self.instance_id = kwargs.get("instance_id")
        self.instance_type = kwargs.get("instance_type")
        self.key = kwargs.get("key")
        self.private_dns = kwargs.get("private_dns")
        self.root_device_name = kwargs.get("root_device_name")
        self.root_device_type = kwargs.get("root_device_type")
        self.status = kwargs.get("status", "defined")
