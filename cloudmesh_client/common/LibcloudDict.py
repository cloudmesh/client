
from pprint import pprint

class LibcloudDict(object):

    @staticmethod
    def convert_libcloud_vm_to_dict(nodeObj):
        vm_dict = {}
        vm_dict['id'] = nodeObj.id
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
        if node_size_obj.id:
            vm_size_dict['id'] = node_size_obj.id
        if node_size_obj.name:
            vm_size_dict['name'] = node_size_obj.name
        if node_size_obj.ram:
            vm_size_dict['ram'] = node_size_obj.ram
        if node_size_obj.name:
            vm_size_dict['disk'] = node_size_obj.disk
        if node_size_obj.name:
            vm_size_dict['bandwidth'] = node_size_obj.bandwidth
        if node_size_obj.name:
            vm_size_dict['price'] = node_size_obj.price
        if node_size_obj.extra:
            pprint("Node Image size extra attrs")
            LibcloudDict.handle_vm_size_extra_args(node_size_obj.extra)
        return vm_size_dict

    @staticmethod
    def handle_vm_size_extra_args(node_size_extra_args):
        for key, val in node_size_extra_args.items():
            pprint(key+" : "+str(val))

    @staticmethod
    def handle_vm_image_details(node_image_obj):
        node_image_dict = {}
        if node_image_obj and node_image_obj.id:
            node_image_dict['id'] = node_image_obj.id
        else:
            node_image_dict['id'] = ""
        if node_image_obj and node_image_obj.name:
            node_image_dict["image_name"] = node_image_obj.name
        else:
            node_image_dict["image_name"] = ""
        if node_image_obj and node_image_obj.extra:
            vm_image_extra_args = LibcloudDict.handle_vm_image_extra_args(node_image_obj.extra)
            node_image_dict.update(vm_image_extra_args)
            pprint("NodeImage extras")
            pprint(node_image_obj.extra)
        else:
            pprint("NodeImage extras not found")
        ## Node Image Extra Args to be added here
        return node_image_dict

    @staticmethod
    def handle_vm_image_extra_args(extra_args):
        image_extra_args_dict = {}
        for key, value in extra_args.items():
            if key == "architecture":
                image_extra_args_dict[key] = value
            if key == "description":
                image_extra_args_dict[key] = value
            if key == "hypervisor":
                image_extra_args_dict[key] = value
            if key == "image_location":
                image_extra_args_dict[key] = value
            if key == "image_type":
                image_extra_args_dict[key] = value
            if key == "is_public":
                image_extra_args_dict[key] = value
            if key == "kernel_id":
                image_extra_args_dict[key] = value
            if key == "owner_alias":
                image_extra_args_dict[key] = value
            if key == "owner_id":
                image_extra_args_dict[key] = value
            if key == "platform":
                image_extra_args_dict[key] = value
            if key == "ramdisk_id":
                image_extra_args_dict[key] = value
            if key == "state":
                image_extra_args_dict[key] = value
            if key == "virtualization_type":
                image_extra_args_dict[key] = value
        return image_extra_args_dict
