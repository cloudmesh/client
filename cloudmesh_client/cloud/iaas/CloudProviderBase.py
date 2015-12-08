# from cloudmesh_base.hostlist import Parameter
import inspect
# from abc import ABCMeta

from cloudmesh_client.common.Printer import dict_printer, attribute_printer
from cloudmesh_client.shell.console import Console


# noinspection PyBroadException
class CloudProviderBase(object):
    #    __metaclass__ = ABCMeta

    def __init__(self, cloudname, user=None, flat=False, source="db"):
        self.kind = ["image", "flavor", "vm", "quota", "limits", "usage"]
        self.nodes = None
        self.flavors = None
        self.data = None
        self.images = None
        self.quota = None
        self.limits = None
        self.usage = None
        self.cloudname = cloudname
        self.keys = None
        self.user = user
        self.secgroup = None
        self.credential = None
        self.driver = None
        self.flag = flat
        self.source = source

    def attributes(self, kind):
        """

        :param kind:
        :return: order and headers of the useful data
        """
        if kind in self.kind:
            header = None
            order = None
        else:
            raise ValueError("Kind " + kind + " not supported")

    def set_source(self, source):
        """
        Sets the source for the information to be returned. "db" and
        "cloud", "memory"
        :param source: the database can be queried in mode "db",
        the database can be bypassed in mode "cloud"
        """
        self.source = source
        if self.source in ["memory"]:
            raise ValueError("Memory source ot implemented yet.")
        return None

    # #########################
    # KIND MANAGEMENT
    # #########################

    def kinds(self, ):
        """
        returns a list of supported list and detail kinds
        :return: list of kinds supported
        :rtype: list
        """
        return self.kind

    def is_kind(self, name):
        """
        returns tru if the kind given by name exists
        :param name:
        :return:
        """
        return name in self.kind

    def add_kind(self, name):
        self.kind.append(name)

    def del_kind(self, name):
        self.kind.remove(name)

    def check_kind(self, name):
        """
        returns tru if the kind given by name exists
        :param name:
        :return:
        """
        if not self.is_kind(name):
            raise ValueError("Kind " + name + "not supported")

    # #########################
    # RESOURCE
    # #########################

    def resource(self, function, kind, cloudname, **kwargs):
        """
        returns the objects in json format
        :param kind: the kind of list: vm, image, flavor, ...
        :param cloudname: if cloudname = none all cloudes, or cloudname = "all"
        :return:
        """
        """
        Listing of vm instances
        :return:
        """
        self.check_kind(kind)
        what = getattr(self, function + "_" + kind)
        return what(cloudname, **kwargs)

    def list(self, kind, cloudname, **kwargs):
        """
        returns the objects in json format
        :param kind: the kind of list: vm, image, flavor, ...
        :param cloudname: if cloudname = none all cloudes, or cloudname = "all"
        :return:
        """
        """
        Listing of vm instances
        :return:
        """
        # print (kwargs)
        return self.resource("list", kind, cloudname, **kwargs)

    def get(self, kind, cloudname, identifier, **kwargs):
        """
        Listing of vm instances
        :return:
        """
        return self.resource("get", kind, cloudname, **kwargs)

    def refresh(self, kind, cloudname, identifier, **kwargs):
        """
        Listing of vm instances
        :return:
        """
        return self.resource("refresh", kind, cloudname, **kwargs)

    # #########################
    # VMS
    # #########################

    def boot_vm(self, cloud, user, name, image, flavor, key, secgroup, meta,
                *kwargs):
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
        raise ValueError(inspect.stack()[0][3] + ": Not implemented yet.")
        return None

    def list_vm(self, cloudname, **kwargs):
        """
        returns the objects in json format
        :param cloudname:
        :return:
        """
        """
        Listing of vm instances
        :return:
        """
        raise ValueError(
            "{}: Not implemented yet.".format(inspect.stack()[0][3]))
        return None

    def get_vm(self, cloudname, identifier, **kwargs):
        """
        returns the objects in json format
        :param cloudname:
        :return:
        """
        """
        get vm instance
        :return:
        """
        raise ValueError(
            "{}: Not implemented yet.".format(inspect.stack()[0][3]))
        return None

    def refresh_vm(self, cloudname, identifier, **kwargs):
        """
        Listing of vm instances
        :return:
        """
        raise ValueError(
            "{}: Not implemented yet.".format(inspect.stack()[0][3]))
        return

    def delete(self, name, group=None, force=None):
        """
        Deletes the vm indicated by name_or_id on target cloud.
        :param name_or_id:
        :param group:
        :param force:
        :return:
        """
        raise ValueError(
            "{}: Not implemented yet.".format(inspect.stack()[0][3]))
        return

    def get_ips(self, name, group=None, force=None):
        """
        Returns the ip addresses of the instance indicated by name_or_id
        :param name_or_id:
        :param group:
        :param force:
        :return:
        """
        raise ValueError(
            "{}: Not implemented yet.".format(inspect.stack()[0][3]))
        return

    # #########################
    # IMAGE
    # #########################

    def list_image(self, cloudname, **kwargs):
        """
        returns the objects in json format
        :param cloudname:
        :return:
        """
        """
        Listing of iamge
        :return:
        """
        raise ValueError(
            "{}: Not implemented yet.".format(inspect.stack()[0][3]))
        return None

    def get_image(self, **kwargs):
        """
        finds the image based on a query
        TODO: details TBD
        """
        raise ValueError(
            "{}: Not implemented yet.".format(inspect.stack()[0][3]))
        return None

    def refresh_image(self, cloudname, identifier, **kwargs):
        """
        Listing of vm instances
        :return:
        """
        raise ValueError(
            "{}: Not implemented yet.".format(inspect.stack()[0][3]))
        return

    # #########################
    # FLAVOR
    # #########################

    def list_flavor(self, cloudname, **kwargs):
        """
        returns the objects in json format
        :param cloudname:
        :return:
        """
        """
        Listing of iamge
        :return:
        """
        raise ValueError(
            "{}: Not implemented yet.".format(inspect.stack()[0][3]))
        return None

    def get_flavor(self, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        raise ValueError(
            "{}: Not implemented yet.".format(inspect.stack()[0][3]))
        return

    # noinspection PyUnusedLocal
    def refresh_flavor(self, cloudname, identifier, **kwargs):
        """
        Listing of vm instances
        :return:
        """
        raise ValueError(
            "{}: Not implemented yet.".format(inspect.stack()[0][3]))
        return

    def details(self, kind, cloud, id, format="table"):
        from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
        try:
            cm = CloudmeshDatabase()

            if kind not in self.kind:
                raise ValueError('{} not defined'.format(kind))

            elements = None
            for idkey in ["name", "uuid", "id"]:
                s = {idkey: id}
                try:
                    elements = cm.find(kind, cloud=cloud, **s)
                except:
                    pass
                if len(elements) > 0:
                    break

            if len(elements) == 0:
                return None

            if format == "table":
                element = elements.values()[0]
                return attribute_printer(element)
            else:
                return dict_printer(elements,
                                    output=format)
        except Exception as ex:
            Console.error(ex.message, ex)
