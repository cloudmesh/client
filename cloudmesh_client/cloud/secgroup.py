from __future__ import print_function

import os
import uuid as UUID

from cloudmesh_client.db import model
from cloudmesh_client.common import tables
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.common.authenticate import Authenticate

from novaclient import client
import requests

requests.packages.urllib3.disable_warnings()


class SecGroup(object):
    cm_db = CloudmeshDatabase()  # Instance to communicate with the cloudmesh database

    @classmethod
    def convert_list_to_dict(cls, os_result):
        d = {}
        for i, obj in enumerate(os_result):
            d[i] = {}
            d[i]["Id"], d[i]["Name"], d[i]["Description"] = obj.id, obj.name, obj.name
        return d

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

            nova = client.Client("2", credentials["OS_USERNAME"],
                                 credentials["OS_PASSWORD"],
                                 credentials["OS_TENANT_NAME"],
                                 credentials["OS_AUTH_URL"],
                                 Config.path_expand(credentials["OS_CACERT"]))
            return nova
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
        uuid = None

        if not cls.get_secgroup(label, tenant, cloudname):

            # Create the security group in OS cloud
            try:
                nova_client = Authenticate.get_environ(cloudname)
                secgroup = nova_client.security_groups \
                    .create(name=label,
                            description="Security group {}".format(label))

                if secgroup:
                    uuid = secgroup.id
                else:
                    print("Failed to create security group, {}".format(secgroup))
                    return None
            except Exception, e:
                print("Exception creating security group in cloud, {}".format(e))
                return None

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
            print("Security group [{}], for cloud [{}], and tenant [{}] "
                  "already exists!".format(label, cloudname, tenant))
            return None

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
            """
            elements = cls.cm_db.query(model.SECGROUP).filter(
                model.SECGROUP.cloud == cloud,
                model.SECGROUP.project == project
            ).all()

            d = cls.toDict(elements)
            """

            nova_client = Authenticate.get_environ(cloud)
            os_result = nova_client.security_groups.list()
            d = SecGroup.convert_list_to_dict(os_result)

            return tables.dict_printer(d,
                                       order=["Id",
                                              "Name",
                                              "Description"],
                                       output="table")

            """
            return (tables.dict_printer(d,
                                        order=["uuid",
                                               "user",
                                               "cloud",
                                               "name",
                                               "project"],
                                        output="table"))
            """

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
                       .format(from_port, to_port, protocol, cidr,
                               secgroup.name))
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
            secgroup = cls.get_secgroup(label, tenant, cloud)
            if secgroup:
                # Delete all rules for group
                cls.delete_all_rules(secgroup)
                cls.cm_db.delete(secgroup)
                return "Security Group [{}] for cloud [{}], & tenant [{}] deleted" \
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
                return "Rule [{} | {} | {} | {}] deleted" \
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
                               .format(rule.fromPort, rule.toPort,
                                       rule.protocol, rule.cidr))
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


if __name__ == '__main__':
    nova = Authenticate.get_environ("india")

    security_groups = nova.security_groups.list()
    print(security_groups)
    print("\n\n")

    for group in security_groups:
        print(group.description)
        print("\n")
