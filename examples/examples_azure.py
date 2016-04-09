from __future__ import print_function
from azure import *
from azure.servicemanagement import *
from cloudmesh_client.common.ConfigDict import ConfigDict

from pprint import pprint

confd = ConfigDict("cloudmesh.yaml")
cloudcred = confd['cloudmesh']['clouds']['azure']['credentials']
clouddefault = confd['cloudmesh']['clouds']['azure']['default']

subscription_id = cloudcred['subscriptionid']
certificate_path = cloudcred['managementcertfile']


## Need to check on how to automate the process of certificate creation
pprint("subscriptionid:"+subscription_id)
pprint("certificate_path:"+certificate_path)

sms = ServiceManagementService(subscription_id, certificate_path)
pprint("sms:")
pprint(sms)


result = sms.list_locations()
for location in result:
    print(location.name)


result = sms.list_hosted_services()

for hosted_service in result:
    print('Service name: ' + hosted_service.service_name)
    print('Management URL: ' + hosted_service.url)
    print('Location: ' + hosted_service.hosted_service_properties.location)
    print('')


### NODES
result = sms.list_hosted_services()

for hosted_service in result:
    print('Service name: ' + hosted_service.service_name)
    print('Management URL: ' + hosted_service.url)
    print('Location: ' + hosted_service.hosted_service_properties.location)
    print('')


### IMAGES
result = sms.list_operating_systems()

for os in result:
    print('OS: ' + os.label)
    print('Family: ' + os.family_label)
    print('Active: ' + str(os.is_active))