from __future__ import absolute_import

from cloudmesh_client.db import model
from cloudmesh_client.common import tables
from cloudmesh_client.shell.console import Console
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase

class Group(object):

    cm_db = CloudmeshDatabase() # Instance to communicate with the cloudmesh database

    @classmethod
    def list(cls, format="table", cloud="general"):
        try:
            d = cls.cm_db.all(model.GROUP)
            print(d)
            return (tables.dict_printer(d,
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
        try:
            group = cls.get_group(name=name, cloud=cloud)
            if group:
                d = cls.toDict(group)
                print(d)
            else:
                return None

            return tables.dict_printer(d,
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
    def add(cls, name, type="vm", user=None, id=None, cloud="general"):
        # user logged into cloudmesh
        user = cls.cm_db.user or user

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
                    id_str += ',' + id # add the id to the group
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

        finally:
            cls.cm_db.close()

    @classmethod
    def delete(cls,  name=None, cloud="general"):
        try:
            group = cls.get_group(name=name, cloud=cloud)
            if group:
                cls.cm_db.delete(group)
                return "Delete Success"
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

    @classmethod
    def copy(cls, _fromName, _toName):
        try:
            _fromGroup = cls.cm_db.find_by_name(model.GROUP, _fromName)
            _toGroup = cls.cm_db.find_by_name(model.GROUP,_toName)

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
                    Console.ok("Created a new group [{}] and added ID [{}] to it"
                               .format(_toName, from_id_str))

            # _fromName group does not exist, error!
            else:
                Console.error("Group [{}] does not exist in the cloudmesh database!"
                              .format(_fromName))
                return None

        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

    @classmethod
    def merge(cls, _nameA, _nameB, mergeName):
        try:
            groupA = cls.cm_db.find_by_name(model.GROUP, _nameA)
            groupB = cls.cm_db.find_by_name(model.GROUP, _nameB)

            if groupA and groupB:
                id_str_a = groupA.value
                id_str_b = groupB.value
                merge_str = id_str_a + ',' + id_str_b
                mergeGroup = model.GROUP(
                    mergeName,
                    merge_str,
                    user=cls.cm_db.user
                )

                cls.cm_db.add(mergeGroup)
                cls.cm_db.save()
                Console.ok("Merge of group [{}] & [{}] to group [{}] successful!"
                           .format(_nameA, _nameB, mergeName))
            else:
                Console.error("Your groups [{}] and/or [{}] do not exist!"
                              .format(_nameA, _nameB))
        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

    @classmethod
    def toDict(cls, item):
        d = {}
        d[item.id] = {}
        for key in item.__dict__.keys():
            if not key.startswith("_sa"):
                d[item.id][key] = str(item.__dict__[key])
        return d