from __future__ import absolute_import

from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.default import Default
from cloudmesh_client.cloud.vm import Vm

from cloudmesh_client.common.dotdict import dotdict

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
    def list(cls, format="table", category="kilo"):
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
    def get_info(cls, category="kilo", name=None, output="table"):
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
                "name": name,
                "category": category
            }

            # group = cls.get(name=name, category=cloud)
            group = cls.cm.find("group", output="object", **args).first()

            if group is not None:
                d = cls.to_dict(group)
            else:
                return None

            return dict_printer(d,
                                order=cls.order,
                                output=output)
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def add(cls, name=None, type="vm", member=None, category="kilo"):
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
                'type': type
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
            group = cls.cm.find_by_name("group", **query)
            if group is not None \
                    and "output" in kwargs:
                d = {"0": group}
                group = dict_printer(d)
            return group

        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def delete(cls, name=None, category="kilo"):
        """
        Method to delete a group from
            the cloudmesh database
        :param name:
        :param cloud:
        :return:
        """
        try:
            # group = cls.get(name=name, category=category)
            args = {}
            if name is not None:
                args["name"] = name
            if category is not None:
                args["category"] = category

            group = cls.cm.find("group", type="vm", output="object", **args)

            if group:
                # Delete VM from cloud before deleting group

                for vm in group:
                    server = group[vm]["member"]
                    try:
                        Vm.delete(cloud=category, servers=[server])
                    except Exception as e:
                        Console.error("Failed to delete VM {}, error: {}"
                                      .format(vm, e))
                        continue

                # Delete group record in local db
                cls.cm.delete(group)
                cls.cm.save()
                return "Delete Success"
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def remove(cls, name, id, category):
        """
        Method to remove an ID from the group
        in the cloudmesh database
        :param name:
        :param id:
        :param category:
        :return:
        """
        try:
            # group = cls.get(name=name, category=category)
            args = {
                "name": name,
                "category": category,
                "member": id
            }

            # Find an existing group with name & category
            group = cls.cm.find("group", output="object", **args)

            if group is not None:
                cls.delete(group)
                cls.cm.save()

                return "Successfully removed {} from the group {}".format(id, name)
            else:
                return "Group: could not find {name} {member}.".format(args)

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

            # _fromGroup = cls.cm.find_by_name(model.GROUP, _fromName)
            # _toGroup = cls.cm.find_by_name(model.GROUP, _toName)
            _fromGroup = cls.cm.find("group", output="object", **from_args)
            _toGroup = cls.cm.find("group", output="object", **to_args)


            if _fromGroup is not None:

                for from_element in _fromGroup:
                    member = from_element["member"]
                    type = from_element["type"]
                    category = from_element["category"]
                    cls.add(cls, name=_toName, type=type, member=member, category=category)
                cls.cm.save()
                Console.ok("Copy from Group [{}] to Group [{}] ok."
                           .format(_fromName, _toName))

            else:
                Console.error(
                    "Group [{}] does not exist in the cloudmesh database!"
                    .format(_fromName))
                return None

        except Exception as ex:
            Console.error(ex.message, ex)


    @classmethod
    def merge(cls, _nameA, _nameB, mergeName):
        """
        Method to merge two groups into
            one group
        :param _nameA:
        :param _nameB:
        :param mergeName:
        :return:
        """

        ValueError("group merge not yet implemented")
        '''
        try:
            args_a = {
                "name": _nameA
            }
            args_b = {
                "name": _nameB
            }

            # groupA = cls.cm.find_by_name(model.GROUP, _nameA)
            # groupB = cls.cm.find_by_name(model.GROUP, _nameB)

            groupA = cls.cm.find("group", output="object", **args_a)
            groupB = cls.cm.find("group", output="object", **args_b)

            if groupA is not None and groupB is not None:

                # Copy default parameters
                user = groupA.user
                category = groupA.category

                """
                mergeGroup = model.GROUP(
                    mergeName,
                    merge_str,
                    user=user,
                    category=category
                )
                cls.cm.add(mergeGroup)
                """

                mergeGroup = cls.cm.db_obj_dict("group",
                                                name=mergeName,
                                                value=merge_str,
                                                user=user,
                                                category=category)
                cls.cm.add_obj(mergeGroup)
                cls.cm.save()

                Console.ok(
                    "Merge of group [{}] & [{}] to group [{}] ok."
                    .format(_nameA, _nameB, mergeName))
            else:
                Console.error("Your groups [{}] and/or [{}] do not exist!"
                              .format(_nameA, _nameB))
        except Exception as ex:
            Console.error(ex.message, ex)
        '''


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

