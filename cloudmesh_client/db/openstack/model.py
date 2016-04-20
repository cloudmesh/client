from ..CloudmeshDatabase import CloudmeshDatabase, CloudmeshMixin
from sqlalchemy import Column, Date, Integer, String


# noinspection PyPep8Naming
class IMAGE_OPENSTACK(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "image_openstack"
    __kind__ = 'image'
    __provider__ = "openstack"
    __mergefields__ = ["username"]

    uuid = Column(String)
    status = Column(String)
    updated = Column(String)
    created = Column(String)
    minDisk = Column(String)
    progress = Column(String)
    minRam = Column(String)
    username = Column(String)
    os_image_size = Column(String)  # This is OS-EXT-IMG-SIZE:size
    # metadata info..
    metadata__base_image_ref = Column(String)
    metadata__description = Column(String)
    metadata__image_location = Column(String)
    metadata__image_state = Column(String)
    metadata__image_type = Column(String)
    metadata__instance_type_ephemeral_gb = Column(String)
    metadata__instance_type_flavorid = Column(String)
    metadata__instance_type_id = Column(String)
    metadata__instance_type_memory_mb = Column(String)
    metadata__instance_type_name = Column(String)
    metadata__instance_type_root_gb = Column(String)
    metadata__instance_type_rxtx_factor = Column(String)
    metadata__instance_type_swap = Column(String)
    metadata__instance_type_vcpus = Column(String)
    metadata__instance_uuid = Column(String)
    metadata__kernel_id = Column(String)
    metadata__network_allocated = Column(String)
    metadata__owner_id = Column(String)
    metadata__ramdisk_id = Column(String)
    metadata__user_id = Column(String)

    def __init__(self, **kwargs):
        super(IMAGE_OPENSTACK, self).set_defaults(**kwargs)

        self.username = kwargs.get("username", None)
        self.uuid = kwargs.get('uuid')
        self.status = kwargs.get('status')
        self.updated = kwargs.get('updated')
        self.created = kwargs.get('created')
        self.minDisk = kwargs.get('minDisk')
        self.progress = kwargs.get('progress')
        self.minRam = kwargs.get('minRam')
        self.os_image_size = kwargs.get('OS-EXT-IMG-SIZE:size')
        self.metadata__base_image_ref = kwargs.get('metadata__base_image_ref')
        self.metadata__description = kwargs.get('metadata__description')
        self.metadata__image_location = kwargs.get('metadata__image_location')
        self.metadata__image_state = kwargs.get('metadata__image_state')
        self.metadata__image_type = kwargs.get('metadata__image_type')
        self.metadata__instance_type_ephemeral_gb = kwargs.get(
            'metadata__instance_type_ephemeral_gb')
        self.metadata__instance_type_flavorid = kwargs.get(
            'metadata__instance_type_flavorid')
        self.metadata__instance_type_id = kwargs.get(
            'metadata__instance_type_id')
        self.metadata__instance_type_memory_mb = kwargs.get(
            'metadata__instance_type_memory_mb')
        self.metadata__instance_type_name = kwargs.get(
            'metadata__instance_type_name')
        self.metadata__instance_type_root_gb = kwargs.get(
            'metadata__instance_type_root_gb')
        self.metadata__instance_type_rxtx_factor = kwargs.get(
            'metadata__instance_type_rxtx_factor')
        self.metadata__instance_type_swap = kwargs.get(
            'metadata__instance_type_swap')
        self.metadata__instance_type_vcpus = kwargs.get(
            'metadata__instance_type_vcpus')
        self.metadata__instance_uuid = kwargs.get('metadata__instance_uuid')
        self.metadata__kernel_id = kwargs.get('metadata__kernel_id')
        self.metadata__network_allocated = kwargs.get(
            'metadata__network_allocated')
        self.metadata__owner_id = kwargs.get('metadata__owner_id')
        self.metadata__ramdisk_id = kwargs.get('metadata__ramdisk_id')
        self.metadata__user_id = kwargs.get('metadata__user_id')

        """if kwargs is not None:
            for key, value in kwargs.iteritems():
                print ("{} = {}".format(key, value))
                self[key] = value"""


# noinspection PyPep8Naming
class FLAVOR_OPENSTACK(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "flavor_openstack"
    __kind__ = 'flavor'
    __provider__ = "openstack"

    uuid = Column(String)
    ram = Column(String)
    os_flv_disabled = Column(String)
    vcpus = Column(String)
    swap = Column(String)
    os_flavor_acces = Column(String)
    rxtx_factor = Column(String)
    os_flv_ext_data = Column(String)
    disk = Column(String)

    def __init__(self, **kwargs):
        super(FLAVOR_OPENSTACK, self).set_defaults(**kwargs)

        self.uuid = kwargs.get('uuid')
        self.ram = kwargs.get('ram')
        self.os_flv_disabled = kwargs.get('OS-FLV-DISABLED:disabled')
        self.vcpus = kwargs.get('vcpus')
        self.swap = kwargs.get('swap')
        self.os_flavor_acces = kwargs.get('os-flavor-access:is_public')
        self.rxtx_factor = kwargs.get('rxtx_factor')
        self.os_flv_ext_data = kwargs.get('OS-FLV-EXT-DATA:ephemeral')
        self.disk = kwargs.get('disk')

        """if kwargs is not None:
            for key, value in kwargs.iteritems():
                print ("{} = {}".format(key, value))
                self[key] = value"""


# noinspection PyPep8Naming
class VM_OPENSTACK(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "vm_openstack"
    __kind__ = 'vm'
    __provider__ = "openstack"
    __mergefields__ = ["username"]

    username = Column(String)
    uuid = Column(String)
    diskConfig = Column(String)
    availability_zone = Column(String)
    power_state = Column(String)
    task_state = Column(String)
    vm_state = Column(String)
    launched_at = Column(String)
    terminated_at = Column(String)
    accessIPv4 = Column(String)
    accessIPv6 = Column(String)
    static_ip = Column(String)
    floating_ip = Column(String)
    config_drive = Column(String)
    created = Column(String)
    flavor__id = Column(String)
    flavor = Column(String)
    hostId = Column(String)
    image__id = Column(String)
    image = Column(String)
    group = Column(String)
    key = Column(String)
    volumes_attached = Column(String)
    progress = Column(String)
    security_groups = Column(String)
    status = Column(String)
    tenant_id = Column(String)
    updated = Column(String)
    user_id = Column(String)  # what is this used for?

    def __init__(self, **kwargs):
        super(VM_OPENSTACK, self).set_defaults(**kwargs)

        self.uuid = kwargs.get("uuid", None)
        self.username = kwargs.get("username", None)
        self.diskConfig = kwargs.get("OS-DCF:diskConfig", None)
        self.availability_zone = kwargs.get("OS-EXT-AZ:availability_zone", None)
        self.power_state = kwargs.get("OS-EXT-STS:power_state", None)
        self.task_state = kwargs.get("OS-EXT-STS:task_state", None)
        self.vm_state = kwargs.get("OS-EXT-STS:vm_state", None)
        self.launched_at = kwargs.get("OS-SRV-USG:launched_at", None)
        self.terminated_at = kwargs.get("OS-SRV-USG:terminated_at", None)
        self.accessIPv4 = kwargs.get("accessIPv4", None)
        self.accessIPv6 = kwargs.get("accessIPv6", None)
        self.static_ip = kwargs.get("static_ip", None)
        self.floating_ip = kwargs.get("floating_ip", None)
        self.config_drive = kwargs.get("config_drive", None)
        self.created = kwargs.get("created", None)
        self.flavor__id = kwargs.get("flavor__id", None)
        self.hostId = kwargs.get("hostId", None)
        self.image__id = kwargs.get("image__id", None)
        self.key = kwargs.get("key", None)
        self.group = kwargs.get("group", None)

        # self.volumes_attached = kwargs.get("volumes_attached", None) or None
        # self.progress = kwargs.get("progress", None)

        # Expects a comma separated string list of security groups.

        self.security_groups = kwargs.get("security_ groups", None)
        self.status = kwargs.get("status", None)
        self.tenant_id = kwargs.get("tenant_id", None)
        self.updated = kwargs.get("updated", None)
        self.user_id = kwargs.get("user_id", None)
        self.status = kwargs.get("status", "defined")
        # self.set_user()