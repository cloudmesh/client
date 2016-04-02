class Attributes(object):
    @classmethod
    def get(cls, kind):
        layout = {
            'flavor': {
                'order': [
                    'id',
                    'name',
                    'user',
                    'ram',
                    'os_flv_disabled',
                    'vcpus',
                    'swap',
                    'os_flavor_acces',
                    'rxtx_factor',
                    'os_flv_ext_data',
                    'disk',
                    'category',
                    'uuid',
                    'updated_at'
                ],
                'header': [
                    'Id',
                    'Name',
                    'User',
                    'RAM',
                    'Disabled',
                    'vCPUs',
                    'Swap',
                    'Access',
                    'rxtx_factor',
                    'os_flv_ext_data',
                    'Disk',
                    'Cloud',
                    'UUID',
                    'updated'
                ]
            },
            'image': {
                'order': [
                    'id',
                    'name',
                    'os_image_size',
                    'metadata__description',
                    'minDisk',
                    'minRam',
                    'progress',
                    'status',
                    'updated',
                    'uuid',
                    'category',
                    'updated_at'
                ],
                'header': [
                    'id',
                    'name',
                    'size',
                    'description',
                    'minDisk',
                    'minRam',
                    'progress',
                    'status',
                    'updated',
                    'uuid',
                    'cloud',
                    'updated_at'
                ]
            },
            'vm': {
                'order': [
                    'id',
                    'group',
                    'label',
                    'status',
                    'static_ip',
                    'floating_ip',
                    'key',
                    'project',
                    'user',
                    'category',
                    'updated_at'
                ],
                'header': [
                    'id',
                    'group',
                    'label',
                    'status',
                    'static_ip',
                    'floating_ip',
                    'key',
                    'project',
                    'user',
                    'cloud',
                    'updated_at'
                ]
            },
            'floating_ip': {
                'order': [
                    "instance_name",
                    "ip",
                    "pool",
                    "fixed_ip",
                    "id",
                    "instance_id",
                    'cloud'
                ],
                'header': [
                    "instance_name",
                    "floating_ip",
                    "floating_ip_pool",
                    "fixed_ip",
                    "floating_ip_id",
                    "instance_id",
                    'cloud'
                ],
            },
            'floating_ip_pool': {
                'order': [
                    "name"
                ],
                'header': [
                    "floating_ip_pool"
                ],
            },
            'clouds': {
                'order': [
                    "id",
                    "cloud",
                    "default",
                    "active",
                    "status",
                    "key"
                ],
                'header': [
                    "id",
                    "Cloud",
                    "Default",
                    "Active",
                    "Status",
                    "Key"
                ],
            },
            'limits': {
                'order': [
                    'Name',
                    'Value'
                ],
                'header': [
                    'Name',
                    'Value'
                ]
            },
            'quota': {
                'order': [
                    'Quota',
                    'Limit'
                ],
                'header': [
                    'Quota',
                    'Limit'
                ]
            },
            'secgroup': {
                'order': [
                    'id',
                    'name',
                    'category',
                    'user',
                    'project',
                    'uuid'
                ],
                'header': [
                    'id',
                    'secgroup_name',
                    'category',
                    'user',
                    'tenant_id',
                    'secgroup_uuid'
                ]
            },
            'default': {
                'order': [
                    'user',
                    'category',
                    'name',
                    'value',
                    'created_at',
                    'updated_at'
                ],
                'header': [
                    'user',
                    'category',
                    'name',
                    'value',
                    'created_at',
                    'updated_at'
                ],
            },
            'group': {
                'order': [
                    "name",
                    "member",
                    "user",
                    "category",
                    "type"],
                'header': [
                    "name",
                    "member",
                    "user",
                    "category",
                    "type"]

            },
            'key': {
                'order': [
                    'keypair__name',
                    "type",
                    "comment",
                    "keypair__fingerprint"
                ],
                'header': [
                    "Name",
                    "Type",
                    "Comment",
                    "Fingerprint"]
            }
        }

        if kind in layout:
            order = layout[kind]["order"]
            header = layout[kind]["header"]
        else:
            order = None
            header = None

        return order, header
