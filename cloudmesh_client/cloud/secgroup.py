from __future__ import print_function

import os

# from cloudmesh_client.db import model
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from novaclient import client
import requests
from cloudmesh_client.cloud.ListResource import ListResource

requests.packages.urllib3.disable_warnings()


# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming
class SecGroup(ListResource):
    cm_db = CloudmeshDatabase()  # Instance to communicate with the cloudmesh database

    @classmethod
    def convert_list_to_dict(cls, os_result):
        d = {}
        for i, obj in enumerate(os_result):
            d[i] = {}
            d[i]["Id"] = obj.id
            d[i]["Name"] = obj.name
            d[i]["Description"] = obj.description
        return d

    # noinspection PyPep8
    @classmethod
    def convert_rules_to_dict(cls, os_result):
        d = {}
        for i, obj in enumerate(os_result):
            d[i] = {}
            d[i]["IP Protocol"] = obj["ip_protocol"]
            d[i]["From Port"] = obj["from_port"]
            d[i]["To Port"] = obj["to_port"]
            if obj["ip_range"]["cidr"]:
                ip_range = obj["ip_range"]["cidr"]
            else:
                ip_range = "0.0.0.0/0"
            d[i]["IP Range"] = ip_range

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

            nova = client.Client("2",
                                 credentials["OS_USERNAME"],
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

        if not cls.get(label, tenant, cloudname):

            # Create the security group in OS cloud
            try:
                # nova_client = CloudProvider.set(cloudname)
                cloud_provider = CloudProvider(cloudname).provider.provider
                secgroup = cloud_provider.security_groups \
                    .create(name=label,
                            description="Security group {}".format(label))

                if secgroup:
                    uuid = secgroup.id
                else:
                    print(
                        "Failed to create security group, {}".format(secgroup))
                    return None
            except Exception, e:
                print(
                    "Exception creating security group in cloud, {}".format(e))
                return None

            secgroup_obj = cls.cm_db.db_obj_dict("secgroup",
                                                 name=label,
                                                 uuid=uuid,
                                                 cloud=cloudname,
                                                 user=user,
                                                 project=tenant)
            """
            secgroup_obj = model.SECGROUP(
                label,
                uuid=uuid,
                cloud=cloudname,
                user=user,
                project=tenant
            )
            cls.cm_db.add(secgroup_obj)
            """

            cls.cm_db.add_obj(secgroup_obj)
            cls.cm_db.save()
            return uuid

        else:
            print("Security group [{}], for cloud [{}], and tenant [{}] "
                  "already exists!".format(label, cloudname, tenant))
            return None

    @classmethod
    def list(cls, project, cloudname="general"):
        """
        This method queries the database to fetch list of secgroups
        filtered by cloud, tenant.
        :param project:
        :param cloud:
        :return:
        """
        # noinspection PyUnreachableCode
        try:
            """
            elements = cls.cm_db.query(model.SECGROUP).filter(
                model.SECGROUP.cloud == cloud,
                model.SECGROUP.project == project
            ).all()

            d = cls.toDict(elements)
            """

            # nova_client = CloudProvider.set(cloud)
            cloud_provider = CloudProvider(cloudname).provider.provider
            os_result = cloud_provider.security_groups.list()
            d = SecGroup.convert_list_to_dict(os_result)

            return dict_printer(d,
                                order=["Id",
                                       "Name",
                                       "Description"],
                                output="table")

        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def get(cls, name, project, cloud="general"):
        """
        This method queries the database to fetch secgroup
        with given name filtered by cloud.
        :param name:
        :param project:
        :param cloud:
        :return:
        """
        try:
            args = {
                "name": name,
                "cloud": cloud,
                "project": project
            }

            """
            secgroup = cls.cm_db.query(model.SECGROUP).filter(
                model.SECGROUP.name == name,
                model.SECGROUP.cloud == cloud,
                model.SECGROUP.project == project
            ).first()
            """
            secgroup = cls.cm_db.find("secgroup", output="object",
                                      **args).first()
            return secgroup

        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def add_rule(cls, cloudname, secgroup, from_port, to_port, protocol, cidr):
        try:
            # Get the nova client object
            # nova_client = CloudProvider.set(secgroup.cloud)
            cloud_provider = CloudProvider(cloudname).provider.provider
            # Create add secgroup rules to the cloud
            rule_id = cloud_provider.security_group_rules.create(secgroup.uuid,
                                                                 ip_protocol=protocol,
                                                                 from_port=from_port,
                                                                 to_port=to_port,
                                                                 cidr=cidr)
            """
            ruleObj = model.SECGROUPRULE(
                uuid=str(rule_id),
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
            """

            ruleObj = cls.cm_db.db_obj_dict("secgrouprule",
                                            uuid=str(rule_id),
                                            name=secgroup.name,
                                            groupid=secgroup.uuid,
                                            cloud=secgroup.cloud,
                                            user=secgroup.user,
                                            project=secgroup.project,
                                            fromPort=from_port,
                                            toPort=to_port,
                                            protocol=protocol,
                                            cidr=cidr)

            cls.cm_db.add_obj(ruleObj)
            cls.cm_db.save()

            Console.ok("Added rule [{} | {} | {} | {}] to secgroup [{}]"
                       .format(from_port, to_port, protocol, cidr,
                               secgroup.name))
        except Exception as ex:
            Console.error(ex.message, ex)
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
            """
            rule = cls.cm_db.query(model.SECGROUPRULE).filter(
                model.SECGROUPRULE.groupid == uuid
            ).all()
            """

            args = {
                "groupid": uuid
            }

            rule = cls.cm_db.find("secgrouprule", **args)
            # d = cls.toDict(rule)
            return (dict_printer(rule,
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

    @classmethod
    def delete_secgroup(cls, label, cloudname, tenant):
        try:
            # Find the secgroup from the cloud
            # nova_client = CloudProvider.set(cloud)
            cloud_provider = CloudProvider(cloudname).provider.provider
            sec_group = cloud_provider.security_groups.find(name=label)
            if not sec_group:
                return None

            # delete the secgroup in the cloud
            cloud_provider.security_groups.delete(sec_group)

            # perform local db deletion
            sec_group = cls.get(label, tenant, cloudname)
            if sec_group:
                # Delete all rules for group
                cls.delete_all_rules(sec_group)
                cls.cm_db.delete(sec_group)
                return "Security Group [{}] for cloud [{}], & tenant [{}] deleted" \
                    .format(label, cloudname, tenant)
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)

        return

    @classmethod
    def delete_rule(cls, cloudname, secgroup, from_port, to_port, protocol, cidr):
        try:
            args = {
                "groupid": secgroup.uuid,
                "fromPort": from_port,
                "toPort": to_port,
                "protocol": protocol,
                "cidr": cidr
            }

            rule = cls.cm_db.find("secgrouprule", output="object",
                                  **args).first()

            """
            rule = cls.cm_db.query(model.SECGROUPRULE).filter(
                model.SECGROUPRULE.groupid == secgroup.uuid,
                model.SECGROUPRULE.fromPort == from_port,
                model.SECGROUPRULE.toPort == to_port,
                model.SECGROUPRULE.protocol == protocol,
                model.SECGROUPRULE.cidr == cidr
            ).first()
            """

            if rule is not None:
                # get the nova client for cloud
                # nova_client = CloudProvider.set(secgroup.cloud)
                cloud_provider = CloudProvider(cloudname).provider.provider
                # delete the rule from the cloud
                cloud_provider.security_group_rules.delete(rule.uuid)
                # delete the local db record
                cls.cm_db.delete(rule)
                return "Rule [{} | {} | {} | {}] deleted" \
                    .format(from_port, to_port, protocol, cidr)
            else:
                return None

        except Exception as ex:
            Console.error(ex.message, ex)

        return

    @classmethod
    def delete_all_rules(cls, secgroup):
        try:
            """
            rules = cls.cm_db.query(model.SECGROUPRULE).filter(
                model.SECGROUPRULE.groupid == secgroup.uuid
            ).all()
            """

            args = {
                "groupid": secgroup.uuid
            }
            rules = cls.cm_db.find("secgrouprule", output="object", **args)

            if rules is not None:
                for rule in rules:
                    cls.cm_db.delete(rule)
                    Console.ok("Rule [{} | {} | {} | {}] deleted"
                               .format(rule.fromPort, rule.toPort,
                                       rule.protocol, rule.cidr))
            else:
                pass
        except Exception as ex:
            Console.error(ex.message, ex)

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
    nova = CloudProvider.set("india")

    # groups = nova.security_groups.list()
    # print(groups)
    # print("\n\n")
    # d = SecGroup.convert_list_to_dict(groups)
    # print(d)

    # security_group = nova.security_groups.create(name="oct17_secgroup", description="Created by Gourav")
    print("Created sec group\n")

    # rule = nova.security_group_rules.create(security_group.id, ip_protocol="icmp",
    #                                        from_port=-1, to_port=-1, cidr="0.0.0.0/0")
    print("Created sec group rules\n")
    # print(rule)

    security_group = nova.security_groups.find(name="oct17_secgroup")
    rules = security_group.rules
    print(rules)

    d = SecGroup.convert_rules_to_dict(rules)
    print(d)

    nova.security_group_rules.delete('6220f8a4-e4fb-4340-bfe7-ffa028a7c6af')
    print("Deleted Sec Group Rule")
