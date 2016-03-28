from sqlalchemy import Column, Integer, String, MetaData, \
    create_engine, ForeignKey


from ..base.model import CloudmeshMixin

from ..db import database
db = database()

#
# OPENSTACK
#

class IMAGE_OPENSTACK(CloudmeshMixin, db.Base):
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
    kind = 'image'

    def __init__(self,
                 name,
                 uuid,
                 category=None,
                 user=None,
                 **kwargs):

        self.provider = "openstack"
        self.label = name
        self.category = category or "general"
        self.name = name
        if user is None:
            self.user = db.user
        else:
            self.user = user

        self.username = kwargs.get("username", 'undefined')
        self.uuid = uuid
        self.type = self.__tablename__
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


class FLAVOR_OPENSTACK(CloudmeshMixin, db.Base):
    uuid = Column(String)
    ram = Column(String)
    os_flv_disabled = Column(String)
    vcpus = Column(String)
    swap = Column(String)
    os_flavor_acces = Column(String)
    rxtx_factor = Column(String)
    os_flv_ext_data = Column(String)
    disk = Column(String)
    kind = 'image'

    def __init__(self,
                 name,
                 uuid,
                 category=None,
                 user=None,
                 **kwargs):

        self.provider = "openstack"
        self.label = name
        self.category = category or "general"

        self.name = name
        if user is None:
            self.user = db.user
        else:
            self.user = user
        self.uuid = uuid
        self.ram = kwargs.get('ram')
        self.os_flv_disabled = kwargs.get('OS-FLV-DISABLED:disabled')
        self.vcpus = kwargs.get('vcpus')
        self.swap = kwargs.get('swap')
        self.os_flavor_acces = kwargs.get('os-flavor-access:is_public')
        self.rxtx_factor = kwargs.get('rxtx_factor')
        self.os_flv_ext_data = kwargs.get('OS-FLV-EXT-DATA:ephemeral')
        self.disk = kwargs.get('disk')
        self.type = self.__tablename__

        """if kwargs is not None:
            for key, value in kwargs.iteritems():
                print ("{} = {}".format(key, value))
                self[key] = value"""


class VM_OPENSTACK(CloudmeshMixin, db.Base):
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
    hostId = Column(String)
    image__id = Column(String)
    key = Column(String)
    name = Column(String)
    volumes_attached = Column(String)
    progress = Column(String)
    security_groups = Column(String)
    status = Column(String)
    tenant_id = Column(String)
    updated = Column(String)
    user_id = Column(String) # what is this used for?
    username = Column(String)
    kind = 'vm'

    def __init__(self, **kwargs):

        self.provider = "openstack"
        self.label = kwargs["name"]
        self.category = kwargs["category"] or "general"

        self.name = kwargs["name"]
        if kwargs['user'] is None:
            self.user = db.user
        else:
            self.user = kwargs['user']
        self.uuid = kwargs["uuid"]
        self.username = kwargs.get("username", 'undefined')
        if "OS-DCF:diskConfig" in kwargs:
            self.diskConfig = kwargs["OS-DCF:diskConfig"]
        if "OS-EXT-AZ:availability_zone" in kwargs:
            self.availability_zone = kwargs["OS-EXT-AZ:availability_zone"]
        if "OS-EXT-STS:power_state" in kwargs:
            self.power_state = kwargs["OS-EXT-STS:power_state"]

        if "OS-EXT-STS:task_state" in kwargs:
            self.task_state = kwargs["OS-EXT-STS:task_state"]

        if "OS-EXT-STS:vm_state" in kwargs:
            self.vm_state = kwargs["OS-EXT-STS:vm_state"]

        if "OS-SRV-USG:launched_at" in kwargs:
            self.launched_at = kwargs["OS-SRV-USG:launched_at"]

        if "OS-SRV-USG:terminated_at" in kwargs:
            self.terminated_at = kwargs["OS-SRV-USG:terminated_at"]

        if "accessIPv4" in kwargs:
            self.accessIPv4 = kwargs["accessIPv4"]

        if "accessIPv6" in kwargs:
            self.accessIPv6 = kwargs["accessIPv6"]

        if "static_ip" in kwargs:
            self.static_ip = kwargs["static_ip"]

        if "floating_ip" in kwargs:
            self.floating_ip = kwargs["floating_ip"]

        if "config_drive" in kwargs:
            self.config_drive = kwargs["config_drive"]

        if "created" in kwargs:
            self.created = kwargs["created"]

        if "flavor__id" in kwargs:
            self.flavor__id = kwargs["flavor__id"]

        if "hostId" in kwargs:
            self.hostId = kwargs["hostId"]

        if "image__id" in kwargs:
            self.image__id = kwargs["image__id"]

        if "key" in kwargs:
            self.key = kwargs["key"]

        if "name" in kwargs:
            self.name = kwargs["name"]
        # self.volumes_attached = kwargs["volumes_attached"] or None
        # self.progress = kwargs["progress"]

        # Expects a comma separated string list of security groups.

        if "security_ groups" in kwargs:
            self.security_groups = kwargs["security_ groups"]

        if "status" in kwargs:
            self.status = kwargs["status"]

        if "tenant_id" in kwargs:
            self.tenant_id = kwargs["tenant_id"]

        if "updated" in kwargs:
            self.updated = kwargs["updated"]

        if "user_id" in kwargs:
            self.user_id = kwargs["user_id"]

        self.type = self.__tablename__

        """
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                print ("{} = {}".format(key, value))
                self[key] = value
        """
