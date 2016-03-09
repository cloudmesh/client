from __future__ import print_function

# here comes the data model for the libcloud abstractions

'''

LIBCLOUD IMAGE DICT ELEMENT

{'_uuid': None,
 'driver': <libcloud.compute.drivers.ec2.EC2NodeDriver object at 0x104a99240>,
 'extra': {'architecture': '',
           'block_device_mapping': [],
           'description': '',
           'hypervisor': None,
           'image_location': 'None (Ubuntu-Server-14.04-LTS)',
           'image_type': 'machine',
           'is_public': 'true',
           'kernel_id': None,
           'owner_alias': None,
           'owner_id': 'admin',
           'platform': None,
           'ramdisk_id': None,
           'root_device_type': 'instance-store',
           'state': 'available',
           'tags': {},
           'virtualization_type': None},
 'id': 'ami-00000005',
 'name': 'Ubuntu-Server-14.04-LTS'}

'''


'''

LIBCLOUD VM DICT

{'_uuid': 'c7f3475df0720fa9aeac012689aa989ee15e46b7',
 'driver': <libcloud.compute.drivers.ec2.EC2NodeDriver object at 0x104a99240>,
 'extra': {'architecture': None,
           'availability': 'nova',
           'block_device_mapping': [],
           'client_token': None,
           'dns_name': '129.114.111.53',
           'ebs_optimized': None,
           'groups': [],
           'hypervisor': None,
           'iam_profile': None,
           'image_id': 'ami-00000005',
           'instance_id': 'i-000035f1',
           'instance_lifecycle': None,
           'instance_tenancy': None,
           'instance_type': 'm1.small',
           'kernel_id': None,
           'key_name': 'y',
           'launch_index': 0,
           'launch_time': '2016-03-06T22:24:40.000Z',
           'monitoring': None,
           'network_interfaces': [],
           'platform': None,
           'private_dns': 'ansible-1',
           'product_codes': [],
           'ramdisk_id': None,
           'reason': None,
           'root_device_name': '/dev/vda',
           'root_device_type': 'instance-store',
           'source_dest_check': None,
           'status': 'running',
           'subnet_id': None,
           'tags': {},
           'virtualization_type': None,
           'vpc_id': None},

'''

'''

LIBCLOUD FLAVOR DICT

{'_uuid': None,
 'bandwidth': None,
 'disk': 0,
 'driver': <libcloud.compute.drivers.ec2.EC2NodeDriver object at 0x1053982e8>,
 'extra': {'cpu': 2},
 'id': 't2.large',
 'name': 'Burstable Performance Medium Instance',
 'price': 0.104,
 'ram': 8192}

 '''