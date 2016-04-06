class Attributes(object):
    @classmethod
    def get(cls, kind):
        layout = {
            'flavor': {
                'order': [
                    'id',
                    'name',
                    'user',
                    'cpu',
                    'ram',
                    'bandwidth',
                    'price',
                    'category',
                    'uuid',
                    'updated_at'
                ],
                'header': [
                    'Id',
                    'Name',
                    'User',
                    'cpu',
                    'RAM',
                    'bandwidth',
                    'price',
                    'Cloud',
                    'UUID',
                    'Updated'
                ]
            },
            'image': {
                'order': [
                    'id',
                    'name',
                    'category',
                    'image_type',
                    'state',
                    'uuid',
                    'updated_at',
                    'owner_id'
                ],
                'header': [
                    'id',
                    'name',
                    'cloud',
                    'image_type',
                    'state',
                    'uuid',
                    'updated_at',
                    'owner_id'
                ]
            },
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
            },
            'floating_ip': {
                'order': [
                    "instance_name",
                    "ip",
                    "pool",
                    "fixed_ip",
                    "id",
                    "instance_id",
                    'cloud',
                    'updated'
                ],
                'header': [
                    "instance_name",
                    "floating_ip",
                    "floating_ip_pool",
                    "fixed_ip",
                    "floating_ip_id",
                    "instance_id",
                    'cloud',
                    'updated'
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
                    "cloud",
                    "status"
                ],
                'header': [
                    "cloud",
                    "status"
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
                    'cloud',
                    'name',
                    'value',
                    'created_at',
                    'updated_at'
                ],
                'header': [
                    'user',
                    'cloud',
                    'name',
                    'value',
                    'created',
                    'updated'
                ],
            }
        }
        if kind in layout:
            order = layout[kind]['order']
            header = layout[kind]['header']
        else:
            order = None
            header = None

        return order, header
