
from pprint import pprint

class LibcloudDict(object):

    @staticmethod
    def convert_libcloud_vm_to_dict(nodeObj):
        vm_dict = {}
        vm_dict['name'] = nodeObj.name
        vm_dict['state'] = str(nodeObj.state)
        if len(nodeObj.public_ips) > 0:
            vm_dict['public_ips'] = nodeObj.public_ips[0]
        else:
            vm_dict['public_ips'] = ""
        if len(nodeObj.private_ips) > 0:
            vm_dict['private_ips'] = nodeObj.private_ips[0]
        else:
            vm_dict['private_ips'] = ""
        vm_image_dict = LibcloudDict.handle_vm_image_details(nodeObj.size)
        vm_dict.update(vm_image_dict)
        if nodeObj.extra:
            extra_args_dict = LibcloudDict.handle_vm_extra_args(nodeObj.extra)
            vm_dict.update(extra_args_dict)
            pprint("Node details dict")
            pprint(nodeObj.extra)
        pprint("IN convert_libcloud_vm_to_dict")
        pprint(vm_dict)
        return vm_dict

    @staticmethod
    def handle_vm_extra_args(extra_args):
        extra_vm_dict = {}
        for key, value in extra_args.items():
            if key == "availability":
                extra_vm_dict[key] = value
            if key == "instance_id":
                extra_vm_dict[key] = value
            if key == "instance_type":
                extra_vm_dict[key] = value
            if key == "key_name":
                extra_vm_dict[key] = value
            if key == "private_dns":
                extra_vm_dict[key] = value
            if key == "root_device_name":
                extra_vm_dict[key] = value
            if key == "root_device_type":
                extra_vm_dict[key] = value
            if key == "status":
                extra_vm_dict[key] = value
        return extra_vm_dict

    @staticmethod
    def handle_vm_size_details(node_size_obj):
        vm_size_dict = {}
        if node_size_obj.name:
            vm_size_dict['node_name'] = node_size_obj.name
        if node_size_obj.ram:
            vm_size_dict['ram'] = node_size_obj.ram
        if node_size_obj.name:
            vm_size_dict['disk'] = node_size_obj.disk
        if node_size_obj.name:
            vm_size_dict['bandwidth'] = node_size_obj.bandwidth
        if node_size_obj.name:
            vm_size_dict['price'] = node_size_obj.price
        return vm_size_dict

    @staticmethod
    def handle_vm_image_details(node_image_obj):
        node_image_dict = {}
        if node_image_obj and node_image_obj.id:
            node_image_dict["image_id"] = node_image_obj.id
        else:
            node_image_dict["image_id"] = ""
        if node_image_obj and node_image_obj.name:
            node_image_dict["image_name"] = node_image_obj.name
        else:
            node_image_dict["image_name"] = ""
        ## Node Image Extra Args to be added here
        return node_image_dict
