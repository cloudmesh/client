from cloudmesh_base.hostlist import Parameter

class CloudmeshProviderBase(object):

    @classmethod
    def initialize(cls, cloudname, user=None):
        cls.kind = ["image","flavor","vm", "quota", "limits", "usage"]
        cls.nodes = None
        cls.flavors = None
        cls.data = None
        cls.images = None
        cls.cloudname = cloudname
        cls.keys = None
        cls.user = user
        cls.secgroup = None
        cls.credential = None
        cls.driver = None

    @classmethod
    def mode(cls, source):
        """
        Sets the source for the information to be returned. "db" and "cloud"
        :param source: the database can be queried in mode "db",
        the database can be bypassed in mode "cloud"
        """
        raise NotImplemented("Not implemented yet.")
        return None

    # #########################
    # KIND MANAGEMENT
    # #########################
    @classmethod
    def kinds(cls):
        """
        returns a list of supported list and detail kinds
        :return: list of kinds supported
        :rtype: list
        """
        return cls.kind

    @classmethod
    def is_kind(cls, name):
        """
        returns tru if the kind given by name exists
        :param name:
        :return:
        """
        return name in cls.kind

    @classmethod
    def add_kind(cls, name):
        cls.kind.append(name)

    @classmethod
    def del_kind(cls, name):
        cls.kind.del(name)

    @classmethod
    def check_kind(cls, name):
        """
        returns tru if the kind given by name exists
        :param name:
        :return:
        """
        if not cls.is_kind(name):
            raise ValueError("Kind " + name + "not supported")

    # #########################
    # RESOURCE
    # #########################

    @classmethod
    def list(cls, kind, cloudname, *kwargs):
        """
        returns the objects in json format
        :param kind: the kind of list: vm, image, flavor, ...
        :param cloudname:
        :return:
        """
        """
        Listing of vm instances
        :return:
        """
        cls.check_kind(kind)
        raise NotImplemented("Not implemented yet.")
        return None

    @classmethod
    def get(cls, kind, cloudname, identifier, *kwargs):
        """
        Listing of vm instances
        :return:
        """
        cls.check_kind(kind)
        raise NotImplemented("Not implemented yet.")
        return None


   # #########################
    # VMS
    # #########################

    @classmethod
    def boot_vm(cls, cloud, user, name, image, flavor, key, secgroup, meta, *kwargs):
        """
        Boots a new vm instance on the target cloud.
        :param cloud:
        :param user:
        :param name:
        :param image:
        :param flavor:
        :param key:
        :param secgroup:
        :param meta:
        :return:
        """
        raise NotImplemented("Not implemented yet.")
        return None

    @classmethod
    def list_vm(cls, cloudname, *kwargs):
        """
        returns the objects in json format
        :param cloudname:
        :return:
        """
        """
        Listing of vm instances
        :return:
        """
        raise NotImplemented("Not implemented yet.")
        return None


    @classmethod
    def get_vm(cls, cloudname, identifier, **kwargs):
        """
        returns the objects in json format
        :param cloudname:
        :return:
        """
        """
        get vm instance
        :return:
        """
        raise NotImplemented("Not implemented yet.")
        return None

    @classmethod
    def delete(cls, name, group=None, force=None):
        """
        Deletes the vm indicated by name_or_id on target cloud.
        :param name_or_id:
        :param group:
        :param force:
        :return:
        """
        raise NotImplemented("Not implemented yet.")
        return

    @classmethod
    def get_ips(cls, name, group=None, force=None):
        """
        Returns the ip addresses of the instance indicated by name_or_id
        :param name_or_id:
        :param group:
        :param force:
        :return:
        """
        raise NotImplemented("Not implemented yet.")
        return


    # #########################
    # IMAGE
    # #########################

    @classmethod
    def get_image(cls, **kwargs):
        """
        finds the image based on a query
        TODO: details TBD
        """
        return None

    # #########################
    # FLAVOR
    # #########################

    @classmethod
    def get_flavor(cls, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        raise NotImplemented("Not implemented yet.")
        return


    # #########################
    # REFRESH
    # #########################
    
    @classmethod
    def refresh(cls, cloud, kind, **kwargs):
        """
        refreshes the information from the cloud into the db

        refresh ("india,aws", "vm,images")

        uses parametrized arguments defined by Parameter in cloudmesh.base

        TODO: details TBD
        """
        raise NotImplemented("Not implemented yet.")
        return





