from __future__ import absolute_import

from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.vm import Vm

from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint

# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming
class Group(ListResource):
    cm = CloudmeshDatabase()  # Instance to communicate with the cloudmesh database

    order = ["name",
             "member",
             "user",
             "category",
             "type"]

    # TODO: implement and extend to user
    @classmethod
    def exists(cls, name, cloud):
        """
        checks if the group with the given name exists
        """
        raise ValueError("not implemented")

    # TODO: implement and extend to user
    @classmethod
    def check(cls, name, cloud):
        """
        checks if the group with the given name exists and raises exception
        """
        if not cls.exists(name, cloud):
            raise ValueError(
                "the default value {} in cloud {} does not exist".format(name,
                                                                         cloud))


    @classmethod
    def names(cls):
        try:
            query = {}

            d = cls.cm.find("GROUP", **query)
            names = set()
            for vm in d:
                names.add(d[vm]['name'])
            return list(names)
        except Exception as ex:
            Console.error(ex.message, ex)


    @classmethod
    def get_vms(cls, name):
        """
        returns a list of vms within this group
        :param name:
        :return:
        """
        try:
            query = {
                "type": "vm",
            }

            if name is not None:
                query["name"] = name

            d = cls.cm.find("GROUP", **query)
            names = set()
            for vm in d:
                names.add(d[vm]['member'])
            return list(names)
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def vm_groups(cls, vm):
        """

        :param vm: name of the vm
        :return: a list of groups the vm is in
        """

        try:
            query = {
                "type": "vm",
                "member": vm
            }

            d = cls.cm.find("GROUP", **query)
            groups = set()
            for vm in d:
                groups.add(d[vm]['name'])
            return list(groups)
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def list(cls, format="table", category="general"):
        """
        Method to get list of groups in
            the cloudmesh database
        :param format:
        :param cloud:
        :return:
        """
        try:
            args = {}
            d = cls.cm.find("GROUP", **args)
            # d = cls.cm.all(model.GROUP)

            return (dict_printer(d,
                                 order=cls.order,
                                 output=format))
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def get_info(cls, category="general", name=None, output="table"):
        """
        Method to get info about a group
        :param cloud:
        :param name:
        :param output:
        :return:
        """
        try:
            cloud = category or Default.get("cloud")

            args = {
                "category": category
            }

            if name is not None:
                args["name"] = name

            group = cls.cm.find("group", output="dict", **args)

            return dict_printer(group,
                                order=cls.order,
                                output=output)
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def add(cls, name=None, type="vm", member=None, category="general"):
        """
        Add an instance to a new group
            or add it to an existing one
        :param name:
        :param type:
        :param member:
        :param cloud:
        :return:
        """
        # user logged into cloudmesh
        user = ConfigDict.getUser(category) or cls.cm.user

        try:
            # See if group already exists. If yes, add id to the group
            data = dotdict({
                'category': category,
                'member': member,
                'type': type,
                'name': name
            })

            group = cls.cm.find("group", output="object",**data).first()

            if group is None:
                obj_d = cls.cm.db_obj_dict("group",
                                           name=name,
                                           member=member,
                                           type=type,
                                           category=category,
                                           user=user)
                cls.cm.add_obj(obj_d)
                cls.cm.save()
                Console.ok("Group: add {} to group {}".format(member, name))
            else:
                group.name = name
                group.member = member

                cls.cm.save()

                Console.ok("Group: move {} to group {}".format(member, name))

        except Exception as ex:
            Console.error(ex.message, ex)

        return

    @classmethod
    def get(cls, **kwargs):
        """
        This method queries the database to fetch group(s)
        with given name filtered by cloud.
        :param name:
        :param cloud:
        :return:
        """
        query = dict(kwargs)

        if 'output' in kwargs:
            for key, value in kwargs.items():
                if value is None:
                    query[key] = "None"
            del query['output']
        try:
            group = cls.cm.find("group", **query)
            if group is not None \
                    and "output" in kwargs:
                d = {"0": group}
                group = dict_printer(d)
            return group

        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def delete(cls, name=None, category="general"):
        """
        Method to delete a group from
            the cloudmesh database
        :param name:
        :param cloud:
        :return:
        """

        print ("DELETE")
        try:
            # group = cls.get(name=name, category=category)
            args = {}
            if name is not None:
                args["name"] = name
            if category is not None:
                args["category"] = category

            print ("AAA", args)

            group = cls.cm.find("group",  output="dict", **args)
            group_object = cls.cm.find("group", output="object", **args)


            print ("A", group, group_object)

            if group:
                # Delete VM from cloud before deleting group

                for vm in group:
                    server = group[vm]["member"]

                    groups = Group.vm_groups(server)

                    if len(groups) == 1:

                        try:
                            Vm.delete(cloud=category, servers=[server])
                        except Exception as e:
                            Console.error("Failed to delete VM {}, error: {}"
                                          .format(vm, e))
                            continue

                # Delete group record in local db

                print("G", group_object)
                for element in group_object:
                    cls.cm.delete(element)
                cls.cm.save()
                return "Delete. ok."
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def remove(cls, name, member, category):
        """
        Method to remove an ID from the group
        in the cloudmesh database
        :param name:
        :param id:
        :param category:
        :return:
        """
        print ("RRRRR")

        try:
            # group = cls.get(name=name, category=category)
            args = {
                "name": name,
                "category": category,
                "member": member,
            }

            # Find an existing group with name & category
            group = cls.cm.find("group", output="object", **args)
            d = cls.cm.find("group", output="dict", **args)

            pprint (args)
            pprint(d)
            print ("GGGGG", group)
            for g in group:
                if group is not None:
                    cls.cm.delete(g)
                else:
                    Console.msg("Group: could not find {name} {member}.".format(args))
            cls.cm.save()

            return "Removed {} from the group {}. ok.".format(member, name)


        except Exception as ex:
            Console.error(ex.message, ex)

        return

    @classmethod
    def copy(cls, _fromName, _toName):
        """
        Method to make copy of a group
        :param _fromName:
        :param _toName:
        :return:
        """
        try:
            from_args = {
                "name": _fromName
            }
            to_args = {
                "name": _toName
            }

            _fromGroup = cls.cm.find("group", output="dict", **from_args)
            _toGroup = cls.cm.find("group", output="dict", **to_args)

            pprint (_fromGroup)
            pprint(_toGroup)

            if _fromGroup is not None:

                for key in _fromGroup:
                    from_element=_fromGroup[key]
                    member = from_element["member"]
                    type = from_element["type"]
                    category = from_element["category"]
                    print ("TTT", _toName)
                    cls.add(name=_toName, type=type, member=member, category=category)
                cls.cm.save()
                Console.ok("Copy from group {} to group {}. ok."
                           .format(_fromName, _toName))

            else:
                Console.error(
                    "Group [{}] does not exist in the cloudmesh database!"
                    .format(_fromName))
                return None

        except Exception as ex:
            Console.error(ex.message, ex)


    @classmethod
    def merge(cls, group_a, group_b, merged_group):
        """
        Method to merge two groups into
            one group
        :param group_a:
        :param group_b:
        :param merged_group:
        :return:
        """
        cls.copy(group_a, merged_group)
        cls.copy(group_b, merged_group)


    # TODO: this is dependent on the provider This needs to be imported from the provider
    @classmethod
    def to_dict(cls, item):
        """
        Method to convert input to a dict
        :param item:
        :return:
        """
        d = {item.id: {}}
        for key in list(item.__dict__.keys()):
            if not key.startswith("_sa"):
                d[item.id][key] = str(item.__dict__[key])
        return d

