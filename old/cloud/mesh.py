import shutil

from cloudmesh_base.hostlist import Parameter
from cloudmesh_base.util import path_expand

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.default import Default


class Mesh(object):
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

    t_flavour = "flavour"
    t_image = "image"
    t_vm = "vm"

    def __init__(self):
        self.db = CloudmeshDatabase()

    @classmethod
    def clouds(self, format='json', order=None):
        filename = "cloudmesh.yaml"
        config = ConfigDict(filename)
        yaml_clouds = dict(config["cloudmesh"]["clouds"])
        return dict_printer(yaml_clouds, output=format, order=order)

    @classmethod
    def verify(self):
        print("verify")

    @classmethod
    def refresh(self):
        print ("refresh")

    @classmethod
    def register(self):
        print ("register")
        self.db.update(['vm', 'image', 'flavor'], ['india', 'aws', 'azure'])

    """
    @classmethod
    def key_add(self, *args):
        print ("key add")
        sshm = SSHKeyManager()
        sshdb = SSHKeyDBManager()
        print len(args)
        if len(args) == 1:
            if os.path.isdir(path_expand(args[0])):
                sshm.get_from_dir(args[0])
                print sshm
                for key in sshm.__keys__:
                    print key
                    print sshm.__keys__[key]['comment']
                    sshdb.add_from_sshkey(sshm.__keys__[key], key)
            else:  # args is the github username
                sshm.get_from_git(args[0])
                print args[0]
                for key in sshm.__keys__:
                    sshdb.add_from_sshkey(sshm.__keys__[key], key)
        elif len(args) == 2:
            keyname = args[0]
            path = path_expand(args[1])
            sshdb.add(path, keyname)


    def key_delete(self, keynames):
        sshdb = SSHKeyDBManager()
        names = keynames.split(',')
        for name in names:
            sshdb.delete(name)
    """

    @classmethod
    def clear(self):
        print ("clear")
        self.db.delete_all(["VM", "FLAVOR", "IMAGE", "DFAULT"])

    @classmethod
    def dump(self, filename):
        """

        :param filename: name of the db file that will receive the content of cloudmesh.db
        :return:
        """
        from_file = path_expand("~/.cloudmesh/cloudmesh.db")
        to_file = path_expand("~/.cloudmesh/{}".format(filename))
        shutil.copyfile(from_file, to_file)
        print ("dump")

    @classmethod
    def load(self, filename):
        """

        :param filename: name of the db file located on ./cloudmesh that will be copied do cloudmesh.db
        :return:
        """
        print ("load")
        from_file = path_expand("~/.cloudmesh/{}".format(filename))
        to_file = path_expand("~/.cloudmesh/cloudmesh.db")
        shutil.copyfile(from_file, to_file)

    @classmethod
    def vms(self, clouds):
        if isinstance(clouds, str):
            return self.vms(kind, [clouds], output)

        for cloud in clouds:
            print ("get vm ids from ", cloud)

    @classmethod
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
        if isinstance(clouds, str):
            return self.list(kind, [clouds], output)

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
    def boot(self, cloud=None, image=None, flavor=None, key=None,  arguments=None):
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
        if cloud is None:
            cloud =  Default.get("cloud", "general")
            print("get default cloud: " + str(cloud))
        if image is None:
            image =  Default.get("image", cloud)
            print("get default image ", str(image))
        if flavor is None:
            flavor =  Default.get("flavor", cloud)
            print("get default flavor ", str(flavor))
        if key is None:
            key =  Default.get("key", str(cloud))
            print("get default key ", str(key))

        # command_key

        print("boot an image", image, flavor, key, cloud, arguments)
        pass

    @classmethod
    def delete(self, ids):
        """
        delete the vms

        Example:

            delete("gregor-[001-010]")

        :param ids: host ids specified in hostlist format
        :return:
        """
        names = Parameter.expand(ids)
        for name in names:
            print ("delete", name)

    @classmethod
    def _generate_name(self, prefix, number, padding):
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
    def _parse_name(self, name):
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
    def next_name(self, name):
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
        prefix, n, padding = self._parse_name(name)
        n += 1
        return self._generate_name(prefix, n, padding)

    @classmethod
    def get_name(self):
        """gets the next name of a vm while increasing its index."""
        # the name format is written to the database based on a set_name
        # the database will contain an index that stores the current index.
        # if no name hase bee defined and this is accessed first the name
        # username-0001 will be used where username is your username
        return "notimplemented-0001"

    @classmethod
    def set_name(self, name):
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
        prefix, n, padding = self.parse_name(name)


def main():
    print(Mesh.next_name("Gregor-001"))

    Mesh.list("flavour", ["india", "hp"], output="table")
    Mesh.list("flavour", "india", output="table")

    Mesh.delete("gregor-001")

    Mesh.delete("gregor-[002-005]")

    print (Mesh.clouds(format='table', order=["cm_label", "cm_type"]))


    Mesh.boot()


    # mesh.dump('test.db')

    # mesh.clear()

    # Mesh.load('test.db')

    # Mesh.refresh()

    #Mesh.key_add('paulo-chagas')


if __name__ == "__main__":
    main()

    """

    # when using filenames embed them in path_expand from cloudmehs_base

    # prints dict of available clouds with information such as defined in yaml
    print(Mesh.clouds())

    # verifies the available clouds and puts some flag into the db that it works or not
    print(Mesh.verify())

    # refreshes the information in the mesh

    Mesh.refresh()
    Mesh.refresh("india")
    Mesh.refresh("india", "aws")
    Mesh.refresh(["india", "aws"])

    # register clouds from a yaml filr
    Mesh.register("cloudmesh.yaml")

    Mesh.key_add("name", "~/.ssh/idrsa.pub")
    Mesh.key_add("github")
    Mesh.key_add("~/.ssh")

    # clear the database
    Mesh.clear()

    # creates a copy of the database into the given file

    Mesh.dump("filename")

    # loads the database for the given file
    Mesh.load("filename")

    """
