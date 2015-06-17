class Cloud(object):

    """
    Design decision. Bellow we like to implement actually a type detection that based on
    one specifying a single string or a list does the right things
    I am not yet sure how to reflect this in the :type: but we can probably sat
    str or list of str

    example:

    delete("myvm1")
    delete("myvm2")
    delete("myvm1", "myvm2")
    delete(["myvm1", "myvm2"])

    are doing all the same thing

    the way we do this is we implement for lists and than mak the other call
    recursively to a list

    We start simply with a print msg

    """
    def list(self, kind, clouds, output="table"):
        """
        Lists the IaaS objects such as flavors, images, vms in the specified output format.

        :param kind: flavor, image, vm
        :type kind: str
        :param clouds: list of clouds we list
        :type clouds: list of str
        :param output: json, yaml, table
        :type output: str
        :return:
        """
        print("list some important objects from a cloud")
        pass

    def boot(self, image, flavor, key, cloud, arguments):
        """
        Boots the image on a specified cloud

        :param image: The name of the image
        :type image: str
        :param flavor: The name of the flavor
        :type flavor: str
        :param key: The name of the key
        :type key: str
        :param cloud: The name of the cloud
        :type cloud: str
        :param arguments: An array of arguments
        :type arguments: list of str
        :return: the id of the vm
        :rtype: str
        """
        print("bot an image")
        pass

    def delete(self, ids):
        """
        delete the vms

        :param id:
        :return:
        """