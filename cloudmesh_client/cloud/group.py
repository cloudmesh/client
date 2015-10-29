from __future__ import absolute_import

from cloudmesh_client.db import model
from cloudmesh_base.Shell import Shell
from cloudmesh_client.common import tables
from cloudmesh_client.cloud.nova import Nova
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.ListResource import ListResource

class Group(ListResource):
    cm_db = CloudmeshDatabase()  # Instance to communicate with the cloudmesh database

    @classmethod
    def list(cls, format="table", cloud="general"):
        """
        Method to get list of groups in
            the cloudmesh database
        :param format:
        :param cloud:
        :return:
        """
        try:
            d = cls.cm_db.all(model.GROUP)
            # Transform the dict to show multiple rows per vm
            newdict = Group.transform_dict(d)
            return (tables.dict_printer(newdict,
                                        order=["user",
                                               "cloud",
                                               "name",
                                               "value",
                                               "type"],
                                        output=format))
        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

    @classmethod
    def get_info(cls, cloud="general", name=None, format="table"):
        """
        Method to get info about a group
        :param cloud:
        :param name:
        :param format:
        :return:
        """
        try:
            group = cls.get_group(name=name, cloud=cloud)
            if group:
                d = cls.to_dict(group)
                # Transform the dict to show multiple rows per vm
                newdict = Group.transform_dict(d)
            else:
                return None

            return tables.dict_printer(newdict,
                                       order=["user",
                                              "cloud",
                                              "name",
                                              "value",
                                              "type"],
                                       output=format)
        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

    @classmethod
    def add(cls, name, type="vm", id=None, cloud="general"):
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
        user = cls.getUser(cloud) or cls.cm_db.user

        try:
            # See if group already exists. If yes, add id to the group
            existing_group = cls.cm_db.find_by_name(model.GROUP, name)

            # Existing group
            if existing_group:
                id_str = str(existing_group.value)
                ids = id_str.split(',')

                # check if id is already in group
                if id in ids:
                    Console.error("ID [{}] is already part of Group [{}]"
                                  .format(id, name))
                else:
                    id_str += ',' + id  # add the id to the group
                    existing_group.value = id_str
                    cls.cm_db.save()
                    Console.ok("Added ID [{}] to Group [{}]"
                               .format(id, name))

            # Create a new group
            else:
                group_obj = model.GROUP(
                    name,
                    id,
                    type,
                    cloud=cloud,
                    user=user
                )
                cls.cm_db.add(group_obj)
                cls.cm_db.save()
                Console.ok("Created a new group [{}] and added ID [{}] to it"
                           .format(name, id))

        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()
        return

    @classmethod
    def get_group(cls, name, cloud="general"):
        """
        This method queries the database to fetch group(s)
        with given name filtered by cloud.
        :param name:
        :param cloud:
        :return:
        """
        try:
            group = cls.cm_db.query(model.GROUP).filter(
                model.GROUP.name == name,
                model.GROUP.cloud == cloud,
            ).first()
            return group

        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def delete(cls, name=None, cloud="general"):
        """
        Method to delete a group from
            the cloudmesh database
        :param name:
        :param cloud:
        :return:
        """
        try:
            group = cls.get_group(name=name, cloud=cloud)

            if group:
                # Delete VM from cloud before deleting group
                vm_ids = group.value.split(",")
                for vm_id in vm_ids:
                    try:
                        # Submit request to delete VM
                        args = ["delete", vm_id]
                        result = Shell.execute("nova", args)
                        print(Nova.remove_subjectAltName_warning(result))
                    except Exception as e:
                        Console.error("Failed to delete VM {}, error: {}"
                                      .format(vm_id, e))
                        continue

                # Delete group record in local db
                cls.cm_db.delete(group)
                return "Delete Success"
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

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
            group = cls.get_group(name=name, cloud=cloud)

            if group:
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
                    cls.cm_db.save()

                    # If delete flag set, then delete group
                    if del_group:
                        Group.delete(name, cloud)

                    return "Successfully removed ID [{}] from the group [{}]"\
                        .format(id, name)
                else:
                    Console.error("The ID [{}] supplied does not belong to group [{}]"
                                  .format(id, name))
                    return None
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

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
            _fromGroup = cls.cm_db.find_by_name(model.GROUP, _fromName)
            _toGroup = cls.cm_db.find_by_name(model.GROUP, _toName)

            # Get IDs from _fromName group
            from_id_str = str(_fromGroup.value)
            from_ids = from_id_str.split(",")

            if _fromGroup:
                # Check if _to group exists, if so add from _fromName
                if _toGroup:
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
                    cls.cm_db.save()
                    Console.ok("Copy from Group [{}] to Group [{}] successful!"
                               .format(_fromName, _toName))

                # Create a new group & copy details from _fromName
                else:
                    group_obj = model.GROUP(
                        _toName,
                        from_id_str,
                        _fromGroup.type,
                        cloud=_fromGroup.cloud,
                        user=_fromGroup.user
                    )
                    cls.cm_db.add(group_obj)
                    cls.cm_db.save()
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

        finally:
            cls.cm_db.close()

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
            groupA = cls.cm_db.find_by_name(model.GROUP, _nameA)
            groupB = cls.cm_db.find_by_name(model.GROUP, _nameB)

            if groupA and groupB:
                id_str_a = groupA.value
                id_str_b = groupB.value
                merge_str = id_str_a + ',' + id_str_b
                # Copy default parameters
                user = groupA.user
                cloud = groupA.cloud

                mergeGroup = model.GROUP(
                    mergeName,
                    merge_str,
                    user=user,
                    cloud=cloud
                )

                cls.cm_db.add(mergeGroup)
                cls.cm_db.save()
                Console.ok(
                    "Merge of group [{}] & [{}] to group [{}] successful!"
                    .format(_nameA, _nameB, mergeName))
            else:
                Console.error("Your groups [{}] and/or [{}] do not exist!"
                              .format(_nameA, _nameB))
        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

    @classmethod
    def to_dict(cls, item):
        """
        Method to convert input to a dict
        :param item:
        :return:
        """
        d = {}
        d[item.id] = {}
        for key in item.__dict__.keys():
            if not key.startswith("_sa"):
                d[item.id][key] = str(item.__dict__[key])
        return d

    @classmethod
    def transform_dict(cls, dict):
        """
        Method to transform a dict,
            to display multiple rows
            per instance of a group
        :param dict:
        :return:
        """
        d = {}
        i = 0

        for key in dict.keys():
            item = dict[key]
            for value in item['value'].split(','):
                d[i] = {}
                d[i]['name'] = item['name']
                d[i]['cloud'] = item['cloud']
                d[i]['user'] = item['user']
                d[i]['value'] = value
                d[i]['type'] = item['type']
                i += 1
        return d

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
            if cloudname == "india":
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
