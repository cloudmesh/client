from __future__ import absolute_import

from cloudmesh_base.Shell import Shell
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.cloud.nova import Nova
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.ListResource import ListResource
from cloudmesh_client.cloud.default import Default
from cloudmesh_client.cloud.vm import Vm


# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming
class Group(ListResource):
    cm = CloudmeshDatabase()  # Instance to communicate with the cloudmesh database

    order = ["name",
             "value",
             "user",
             "cloud",
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
    def list(cls, format="table", cloud="kilo"):
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
            # Transform the dict to show multiple rows per vm
            newdict = Group.transform_dict(d)
            return (dict_printer(newdict,
                                 order=cls.order,
                                 output=format))
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def get_info(cls, cloud="kilo", name=None, output="table"):
        """
        Method to get info about a group
        :param cloud:
        :param name:
        :param output:
        :return:
        """
        try:
            cloud = cloud or Default.get("cloud")
            args = {
                "name": name,
                "cloud": cloud
            }

            # group = cls.get(name=name, cloud=cloud)
            group = cls.cm.find("group", output="object", **args).first()

            if group is not None:
                d = cls.to_dict(group)
                # Transform the dict to show multiple rows per vm
                newdict = Group.transform_dict(d)
            else:
                return None

            return dict_printer(newdict,
                                order=cls.order,
                                output=output)
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def add(cls, name=None, type="vm", id=None, cloud="kilo"):
        """
        Add an instance to a new group
            or add it to an existing one
        :param name:
        :param type:
        :param id:
        :param cloud:
        :return:
        """
        # user logged into cloudmesh
        user = cls.getUser(cloud) or cls.cm.user

        try:
            # See if group already exists. If yes, add id to the group
            query = {
                'name': name,
                'cloud': cloud
            }

            # Find an existing group with name
            existing_group = cls.cm.find("group", output="object",
                                         **query).first()

            # Existing group
            if existing_group is not None:
                id_str = str(existing_group.value)
                ids = id_str.split(',')

                # check if id is already in group
                if id in ids:
                    Console.error("ID [{}] is already part of Group [{}]"
                                  .format(id, name))
                else:
                    id_str += ',' + id  # add the id to the group
                    existing_group.value = id_str
                    cls.cm.save()
                    Console.ok("Added ID [{}] to Group [{}]"
                               .format(id, name))

            # Create a new group
            else:
                obj_d = cls.cm.db_obj_dict("group",
                                           name=name,
                                           value=id,
                                           type=type,
                                           cloud=cloud,
                                           user=user)
                cls.cm.add_obj(obj_d)
                cls.cm.save()

                """
                group_obj = model.GROUP(
                    name,
                    id,
                    type,
                    cloud=cloud,
                    user=user
                )
                cls.cm.add(group_obj)
                cls.cm.save()
                """
                Console.ok("Created a new group [{}] and added ID [{}] to it"
                           .format(name, id))

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
            for key, value in kwargs.iteritems():
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
    def delete(cls, name=None, cloud="kilo"):
        """
        Method to delete a group from
            the cloudmesh database
        :param name:
        :param cloud:
        :return:
        """
        try:
            # group = cls.get(name=name, cloud=cloud)
            args = {}
            if name is not None:
                args["name"] = name
            if cloud is not None:
                args["cloud"] = cloud

            group = cls.cm.find("group", output="object", **args).first()

            if group:
                # Delete VM from cloud before deleting group
                vm_ids = group.value.split(",")
                for vm_id in vm_ids:
                    try:
                        # Submit request to delete VM
                        # args = ["delete", vm_id]
                        # result = Shell.execute("nova", args)

                        # FIX: Using vm.delete instead of nova
                        Vm.delete(cloud=cloud, servers=[vm_id])
                    except Exception as e:
                        Console.error("Failed to delete VM {}, error: {}"
                                      .format(vm_id, e))
                        continue

                # Delete group record in local db
                cls.cm.delete(group)
                return "Delete Success"
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def remove(cls, name, id, cloud):
        """
        Method to remove an ID from the group
        in the cloudmesh database
        :param name:
        :param id:
        :param cloud:
        :return:
        """
        try:
            # group = cls.get(name=name, cloud=cloud)
            args = {
                "name": name,
                "cloud": cloud
            }

            # Find an existing group with name & cloud
            group = cls.cm.find("group", output="object", **args).first()

            if group is not None:
                vm_ids = group.value.split(",")
                new_id_str = ","
                del_group = False

                # If group has single ID, then set delete flag
                if len(vm_ids) == 1:
                    del_group = True

                if id in vm_ids:
                    for vm_id in vm_ids:
                        if id == vm_id:
                            vm_ids.remove(vm_id)

                    # Update the list of IDs for group
                    new_id_str = new_id_str.join(vm_ids)
                    group.value = new_id_str

                    # Save the db record
                    cls.cm.save()

                    # If delete flag set, then delete group
                    if del_group is not None:
                        Group.delete(name, cloud)

                    return "Successfully removed ID [{}] from the group [{}]" \
                        .format(id, name)
                else:
                    Console.error(
                        "The ID [{}] supplied does not belong to group [{}]"
                        .format(id, name))
                    return None
            else:
                return None

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
            _fromGroup = cls.cm.find("group", output="object",
                                     **from_args).first()
            _toGroup = cls.cm.find("group", output="object", **to_args).first()

            # Get IDs from _fromName group
            from_id_str = str(_fromGroup.value)
            from_ids = from_id_str.split(",")

            if _fromGroup is not None:
                # Check if _to group exists, if so add from _fromName
                if _toGroup is not None:
                    # Get existing list of IDs from _to group
                    to_id_str = str(_toGroup.value)
                    to_ids = to_id_str.split(",")

                    # Iterate and check if IDs are already present
                    # If not present in _toName, then add else pass
                    for _id in from_ids:
                        if _id in to_ids:
                            pass
                        else:
                            to_id_str += ',' + _id

                    _toGroup.value = to_id_str
                    cls.cm.save()
                    Console.ok("Copy from Group [{}] to Group [{}] successful!"
                               .format(_fromName, _toName))

                # Create a new group & copy details from _fromName
                else:
                    group_obj = cls.cm.db_obj_dict("group",
                                                   name=_toName,
                                                   value=from_id_str,
                                                   type=_fromGroup.type,
                                                   cloud=_fromGroup.cloud,
                                                   user=_fromGroup.user)
                    cls.cm.add_obj(group_obj)
                    cls.cm.save()
                    """
                    group_obj = model.GROUP(
                        _toName,
                        from_id_str,
                        _fromGroup.type,
                        cloud=_fromGroup.cloud,
                        user=_fromGroup.user
                    )
                    cls.cm.add(group_obj)
                    """
                    Console.ok(
                        "Created a new group [{}] and added ID [{}] to it"
                        .format(_toName, from_id_str))

            # _fromName group does not exist, error!
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
        try:
            args_a = {
                "name": _nameA
            }
            args_b = {
                "name": _nameB
            }

            # groupA = cls.cm.find_by_name(model.GROUP, _nameA)
            # groupB = cls.cm.find_by_name(model.GROUP, _nameB)

            groupA = cls.cm.find("group", output="object", **args_a).first()
            groupB = cls.cm.find("group", output="object", **args_b).first()

            if groupA is not None \
                    and groupB is not None:
                id_str_a = groupA.value
                id_str_b = groupB.value
                merge_str = id_str_a + ',' + id_str_b

                # Copy default parameters
                user = groupA.user
                cloud = groupA.cloud

                """
                mergeGroup = model.GROUP(
                    mergeName,
                    merge_str,
                    user=user,
                    cloud=cloud
                )
                cls.cm.add(mergeGroup)
                """

                mergeGroup = cls.cm.db_obj_dict("group",
                                                name=mergeName,
                                                value=merge_str,
                                                user=user,
                                                cloud=cloud)
                cls.cm.add_obj(mergeGroup)
                cls.cm.save()

                Console.ok(
                    "Merge of group [{}] & [{}] to group [{}] successful!"
                    .format(_nameA, _nameB, mergeName))
            else:
                Console.error("Your groups [{}] and/or [{}] do not exist!"
                              .format(_nameA, _nameB))
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def to_dict(cls, item):
        """
        Method to convert input to a dict
        :param item:
        :return:
        """
        d = {item.id: {}}
        for key in item.__dict__.keys():
            if not key.startswith("_sa"):
                d[item.id][key] = str(item.__dict__[key])
        return d

    # TODO we have a dict transformer elsewhere
    @classmethod
    def transform_dict(cls, dictionary):
        """
        Method to transform a dict,
            to display multiple rows
            per instance of a group
        :param dictionary:
        :return:
        """
        d = {}
        i = 0

        for key in dictionary.keys():
            item = dictionary[key]
            for value in item['value'].split(','):
                d[i] = {}
                d[i]['name'] = item['name']
                d[i]['cloud'] = item['cloud']
                d[i]['user'] = item['user']
                d[i]['value'] = value
                d[i]['type'] = item['type']
                i += 1
        return d

    # TODO Bug. This needs to go to the CLoudProviderOpenstackAPI
    # TODO Bug naturally the india implementation here is buggy
    @classmethod
    def getUser(cls, cloudname):
        """
        Method to get the user information
            from the cloudmesh database
            for a given cloud
        :param cloudname:
        :return:
        """
        try:
            # currently support India cloud
            if cloudname in ["juno", "kilo"]:
                d = ConfigDict("cloudmesh.yaml")
                credentials = d["cloudmesh"]["clouds"][cloudname][
                    "credentials"]
                for key, value in credentials.iteritems():
                    if key == "OS_USERNAME":
                        return value
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)
