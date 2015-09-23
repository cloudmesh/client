from __future__ import print_function

import os
import uuid as UUID

from cloudmesh_client.db import model
from cloudmesh_client.common import tables
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase

class SecGroup(object):

    cm_db = CloudmeshDatabase() # Instance to communicate with the cloudmesh database

    @classmethod
    def set_os_environ(cls, cloudname):
        """Set os environment variables on a given cloudname"""
        try:
            d = ConfigDict("cloudmesh.yaml")
            credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]
            for key, value in credentials.iteritems():
                if key == "OS_CACERT":
                    os.environ[key] = Config.path_expand(value)
                else:
                    os.environ[key] = value

                print("Key: " + key + ", Value: " + os.environ[key])
        except Exception, e:
            print(e)

    # noinspection PyPep8Naming
    @classmethod
    def remove_subjectAltName_warning(cls, content):
        result = []
        for line in content.split("\n"):
            if "Certificate has no `subjectAltName`" in line:
                pass
            elif "SecurityWarning" in line:
                pass
            else:
                result.append(line)
        return "\n".join(result)

    @classmethod
    def create(cls, label, cloudname=None, tenant=None):
        """
        Method creates a new security group in database
        & returns the uuid of the created group
        :param label:
        :param cloudname:
        :param tenant:
        :return:
        """
        # Get user from cloudmesh.yaml
        user = cls.getUser(cloudname)
        # Generate UUID
        uuid = str(UUID.uuid1())

        if not cls.get_secgroup(label, tenant, cloudname):
            secgroup_obj = model.SECGROUP(
                label,
                uuid=uuid,
                cloud=cloudname,
                user=user,
                project=tenant
            )
            cls.cm_db.add(secgroup_obj)
            cls.cm_db.save()
            return uuid

        else:
            return None

        #args = ["--insecure", "secgroup-create", label,
        #        "\" Security group for cloud: [{}], tenant: [{}]\""
        #            .format(cloudname, tenant)]

        #result = Shell.execute("nova", args)
        #return result

    @classmethod
    def list_secgroup(cls, project, cloud="general"):
        """
        This method queries the database to fetch list of secgroups
        filtered by cloud, tenant.
        :param project:
        :param cloud:
        :return:
        """
        try:
            elements = cls.cm_db.query(model.SECGROUP).filter(
                model.SECGROUP.cloud == cloud,
                model.SECGROUP.project == project
            ).all()

            d = cls.toDict(elements)
            return (tables.dict_printer(d,
                                 order=["uuid",
                                        "user",
                                        "cloud",
                                        "name",
                                        "project"],
                                 output="table"))

        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

    @classmethod
    def get_secgroup(cls, name, project, cloud="general"):
        """
        This method queries the database to fetch secgroup
        with given name filtered by cloud.
        :param name:
        :param project:
        :param cloud:
        :return:
        """
        try:
            secgroup = cls.cm_db.query(model.SECGROUP).filter(
                model.SECGROUP.name == name,
                model.SECGROUP.cloud == cloud,
                model.SECGROUP.project == project
            ).first()
            return secgroup

        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

    @classmethod
    def add_rule(cls, secgroup, from_port, to_port, protocol, cidr):
        try:
            ruleObj = model.SECGROUPRULE(
                name=secgroup.name,
                groupid=secgroup.uuid,
                cloud=secgroup.cloud,
                user=secgroup.user,
                project=secgroup.project,
                fromPort=from_port,
                toPort=to_port,
                protocol=protocol,
                cidr=cidr
            )
            cls.cm_db.add(ruleObj)
            cls.cm_db.save()
            Console.ok("Added rule [{} | {} | {} | {}] to secgroup [{}]"
                       .format(from_port, to_port, protocol, cidr, secgroup.name))
        except Exception as ex:
            Console.error(ex.message, ex)
        finally:
            cls.cm_db.close()
        return

    @classmethod
    def get_rules(cls, uuid):
        """
        This method gets the security group rule
        from the cloudmesh database
        :param uuid:
        :return:
        """
        try:
            rule = cls.cm_db.query(model.SECGROUPRULE).filter(
                model.SECGROUPRULE.groupid == uuid
            ).all()

            d = cls.toDict(rule)
            return (tables.dict_printer(d,
                                 order=["user",
                                        "cloud",
                                        "name",
                                        "fromPort",
                                        "toPort",
                                        "protocol",
                                        "cidr"],
                                 output="table"))

        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()

    @classmethod
    def delete_secgroup(cls, label, cloud, tenant):
        try:
            secgroup = cls.get_secgroup(label,tenant,cloud)
            if secgroup:
                # Delete all rules for group
                cls.delete_all_rules(secgroup)
                cls.cm_db.delete(secgroup)
                return "Security Group [{}] for cloud [{}], & tenant [{}] deleted"\
                    .format(label, cloud, tenant)
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)
        finally:
            cls.cm_db.close()

        return

    @classmethod
    def delete_rule(cls, secgroup, from_port, to_port, protocol, cidr):
        try:
            rule = cls.cm_db.query(model.SECGROUPRULE).filter(
                model.SECGROUPRULE.groupid == secgroup.uuid,
                model.SECGROUPRULE.fromPort == from_port,
                model.SECGROUPRULE.toPort == to_port,
                model.SECGROUPRULE.protocol == protocol,
                model.SECGROUPRULE.cidr == cidr
            ).first()

            if rule:
                cls.cm_db.delete(rule)
                return "Rule [{} | {} | {} | {}] deleted"\
                        .format(from_port, to_port, protocol, cidr)
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()
        return

    @classmethod
    def delete_all_rules(cls, secgroup):
        try:
            rules = cls.cm_db.query(model.SECGROUPRULE).filter(
                model.SECGROUPRULE.groupid == secgroup.uuid
            ).all()

            if rules:
                for rule in rules:
                    cls.cm_db.delete(rule)
                    Console.ok("Rule [{} | {} | {} | {}] deleted"
                               .format(rule.fromPort, rule.toPort, rule.protocol, rule.cidr))
            else:
                pass
        except Exception as ex:
            Console.error(ex.message, ex)

        finally:
            cls.cm_db.close()
        return

    @classmethod
    def getUser(cls, cloudname):
        try:
            #currently support India cloud
            if cloudname == "india":
                d = ConfigDict("cloudmesh.yaml")
                credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]
                for key, value in credentials.iteritems():
                    if key == "OS_USERNAME":
                        return value
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)


    @classmethod
    def toDict(cls, item):
        """
        Method converts the item to a dict
        :param item:
        :return:
        """
        # Convert to dict & print table
        d = {}
        # If list, iterate to form dict
        if isinstance(item, list):
            for element in item:
                d[element.id] = {}
                for key in element.__dict__.keys():
                    if not key.startswith("_sa"):
                        d[element.id][key] = str(element.__dict__[key])
        # Form dict without iterating
        else:
            d[item.id] = {}
            for key in item.__dict__.keys():
                if not key.startswith("_sa"):
                    d[item.id][key] = str(item.__dict__[key])

        # return the dict
        return d