
from pprint import pprint

class LibcloudDict(object):

    @staticmethod
    def convert_libcloud_vm_to_dict(nodeObj):
        vm_dict = {}
        vm_dict['name']=nodeObj.name
        vm_dict['state']=nodeObj.name
        vm_dict['private_ips']=nodeObj.name
        pprint("IN convert_libcloud_vm_to_dict")
        pprint(vm_dict)
        return vm_dict

