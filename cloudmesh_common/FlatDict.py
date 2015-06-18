from __future__ import print_function
from pprint import pprint

# http://stackoverflow.com/questions/6027558/flatten-nested-python-dictionaries-compressing-keys

import collections


def flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def main():
    d = {
        'cm_cloud': 'india',
        'cm_update': '2015-06-18 22:11:48 UTC',
        'cm_user': 'gregor',
        'extra': {'created': '2015-05-21T20:37:10Z',
                  'metadata': {'base_image_ref': '398746398798372493287',
                               'description': None,
                               'image_location': 'snapshot',
                               'image_state': 'available',
                               'image_type': 'snapshot',
                               'instance_type_ephemeral_gb': '0',
                               'instance_type_flavorid': '3',
                               'instance_type_id': '1',
                               'instance_type_memory_mb': '4096',
                               'instance_type_name': 'm1.medium',
                               'instance_type_root_gb': '40',
                               'instance_type_rxtx_factor': '1.0',
                               'instance_type_swap': '0',
                               'instance_type_vcpus': '2',
                               'instance_uuid': '386473678463876387',
                               'kernel_id': None,
                               'network_allocated': 'True',
                               'owner_id': '36487264932876984723649',
                               'ramdisk_id': None,
                               'user_id': '762387463827463278649837'},
                  'minDisk': 40,
                  'minRam': 0,
                  'progress': 100,
                  'serverId': 'yiuksajhlkjahl',
                  'status': 'ACTIVE',
                  'updated': '2015-05-27T02:11:48Z'},
        'id': '39276498376478936247832687',
        'name': 'VM with Cloudmesh Configured Completely'
    }

    pprint(d)
    pprint(flatten(d))


if __name__ == "__main__":
    main()
