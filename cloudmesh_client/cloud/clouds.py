import cloudmesh_base.hostlist


class Cloud(object):
    t_flavour = "flavour"
    t_image = "image"
    t_vm = "vm"

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

    @classmethod
    def vms(cls, clouds):
        if isinstance(clouds, str):
            return cls.vms(kind, [clouds], output)

        for cloud in clouds:
            print ("get vm ids from ", cloud)

    @classmethod
    def list(cls, kind, clouds, output="table"):
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
        if isinstance(clouds, str):
            return cls.list(kind, [clouds], output)

        for cloud in clouds:
            if kind in ["f", "flavour"]:
                print ("flavor", cloud)
            elif kind in ["v", "vm"]:
                print ("vm", cloud)
            elif kind in ["i", "image"]:
                print ("image", cloud)
            else:
                print ("kind", kind, "not supported")
        return "done"

    @classmethod
    def boot(cls, image, flavor, key, cloud, arguments):
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
        print("bot an image", image, flavor, key, cloud, arguments)
        pass

    @classmethod
    def delete(cls, ids):
        """
        delete the vms

        Example:

            delete("gregor-[001-010]")

        :param ids: host ids specified in hostlist format
        :return:
        """
        names = hostlist.expand_hostlist(ids)
        for name in names:
            print ("delete", name)

    @classmethod
    def _generate_name(cls, prefix, number, padding):
        """
        method to create a vm name from a prefix, with given padding of 0

        :param prefix: the prefix of the name
        :type prefix: str
        :param number: the number
        :type number: str or int
        :param padding: the number of 0 that are used for padding
        :type padding: str or int
        :return:
        """
        format_string = prefix + "-{0:0" + str(padding) + "}"
        return format_string.format(number)

    @classmethod
    def _parse_name(cls, name):
        """
        returns the prefix, the number and the padding length

        :param name: the name to parse
        :type name: str
        :return: prefix, number, padding length
        :rtype: str, int, int
        """
        prefix, number = name.rsplit('-', 1)
        n = int(number)
        padding = len(number)
        return prefix, n, padding

    @classmethod
    def next_name(cls, name):
        """
        generates the next name.

        Example:

            next_name("gregor-0001")

            gregor-0002

        :param name: the name
        :type name: str
        :return: the new name
        :rtype: str
        """
        prefix, n, padding = cls._parse_name(name)
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
        """

        :param name:
        :return:
        """
        """sets the name of a vm.
        The name is ended by a simple number. The number of 0 in it wil be used for padding.

        set_name("gregor-001")
        This information will be used when getting the next index. If the next index exceeds the padding
        we simply just increase the number.

        """
        prefix, n, padding = cls.parse_name(name)


def main():
    print(Cloud.next_name("Gregor-001"))

    Cloud.list("flavour", ["india", "hp"], output="table")
    Cloud.list("flavour", "india", output="table")

    Cloud.delete("gregor-001")

    Cloud.delete("gregor-[002-005]")


if __name__ == "__main__":
    main()
