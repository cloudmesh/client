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
        pass

    @classmethod
    def _generate_name(cls, prefix, number, padding):
        """method to create a vm name from a prefix, with given padding of 0"""
        format_string = prefix + "-{0:0" + str(padding) + "}"
        return format_string.format(number)

    @classmethod
    def _parse_name(cls, name):
        prefix, number = name.rsplit('-', 1)
        n = int(number)
        padding = len(number)
        return prefix, n, padding

    @classmethod
    def next_name(cls, name):
        prefix, n, padding = cls.parse_name(name)
        n = n + 1
        return cls._generate_name(prefix, n, padding)

    @classmethod
    def get_name(cls):
        """gets the next name of a vm while increasing its index."""
        # the name format is written to the database based on a set_name
        # the database will contain an index that stores the current index.
        # if no name hase bee defined and this is accessed first the name
        # username-0001 will be used where username is your username
        return "notimplemented-0001"

    @classmethod
    def set_name(cls, name):
        """sets the name of a vm.
        The name is ended by a simple number. The number of 0 in it wil be used for padding.

        set_name("gregor-001")
        This information will be used when getting the next index. If the next index exceeds the padding
        we simply just increase the number.

        """
        prefix, n, padding = cls.parse_name(name)



def main():
    c = Cloud()
    print(Cloud.next_name("Gregor-001"))

if __name__ == "__main__":
    main()
