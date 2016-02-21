from __future__ import print_function

import requests
from pprint import pprint

from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.cloud.ListResource import ListResource

requests.packages.urllib3.disable_warnings()


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
    def refresh(cls, cloud):
        """
        This method would refresh the secgroup list by first clearing
        the database, then inserting new data
        :param cloud: the cloud name
        """
        return cls.cm_db.refresh('secgroup', cloud)

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
    def create(cls, label, cloud=None):
        """
        Method creates a new security group in database
        & returns the uuid of the created group
        :param label:
        :param cloud:
        :param tenant:
        :return:
        """
        # Create the security group in given cloud
        try:
            cloud_provider = CloudProvider(cloud).provider
            secgroup = cloud_provider.create_secgroup(label)
            if secgroup:
                uuid = secgroup.id
                return uuid
            else:
                print("Failed to create security group, {}".format(secgroup))
        except Exception, e:
            print(
                "Exception creating security group in cloud, {}".format(e))

        return None

    @classmethod
    def list(cls, cloud="general", format="table"):
        """
        This method queries the database to fetch list of secgroups
        filtered by cloud.
        :param cloud:
        :return:
        """
        try:
            elements = cls.cm_db.find("secgroup",
                                      category=cloud)
            #pprint(elements)
            (order, header) = CloudProvider(cloud).get_attributes("secgroup")

            return dict_printer(elements,
                                order=order,
                                header=header,
                                output=format)

        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def enable_ssh(cls, secgroup_name='default', cloud="general"):
        ret = False
        cloud_provider = CloudProvider(cloud).provider.provider
        secgroups = cloud_provider.security_groups.list()
        for asecgroup in secgroups:
            if asecgroup.name == secgroup_name:
                rules = asecgroup.rules
                rule_exists = False
                # structure of a secgroup rule:
                # {u'from_port': 22, u'group': {}, u'ip_protocol': u'tcp', u'to_port': 22, u'parent_group_id': u'UUIDHERE', u'ip_range': {u'cidr': u'0.0.0.0/0'}, u'id': u'UUIDHERE'}
                for arule in rules:
                    if arule["from_port"] == 22 and \
                                    arule["to_port"] == 22 and \
                                    arule["ip_protocol"] == 'tcp' and \
                                    arule["ip_range"] == {'cidr': '0.0.0.0/0'}:
                        # print (arule["id"])
                        rule_exists = True
                        break
                if not rule_exists:
                    cloud_provider.security_group_rules.create(
                        asecgroup.id,
                        ip_protocol='tcp',
                        from_port=22,
                        to_port=22,
                        cidr='0.0.0.0/0')
                # else:
                #    print ("The rule allowing ssh login did exist!")
                ret = True
                break

        # print ("*" * 80)
        # d = SecGroup.convert_list_to_dict(secgroups)
        # print (d)
        return ret

    @classmethod
    def get(cls, name, cloud="general"):
        """
        This method queries the database to fetch secgroup
        with given name filtered by cloud.
        :param name:
        :param cloud:
        :return:
        """
        try:
            args = {
                "name": name,
                "category": cloud,
            }
            secgroup = cls.cm_db.find("secgroup",
                                      output="object",
                                      **args).first()
            return secgroup

        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def add_rule(cls, cloud, secgroup, from_port, to_port, protocol, cidr):
        try:
            # Get the nova client object
            cloud_provider = CloudProvider(cloud).provider

            # Create add secgroup rules to the cloud
            args = {
                'uuid': secgroup.uuid,
                'protocol': protocol,
                'from_port': from_port,
                'to_port': to_port,
                'cidr': cidr
            }
            rule_id = cloud_provider.add_secgroup_rule(**args)

            # create local db record
            ruleObj = cls.cm_db.db_obj_dict("secgrouprule",
                                            uuid=str(rule_id),
                                            name=secgroup.name,
                                            groupid=secgroup.uuid,
                                            category=secgroup.category,
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
            if "This rule already exists" in ex.message:
                Console.ok("Rule already exists. Added rule.")
                return
            else:
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
            args = {
                "groupid": uuid
            }

            rule = cls.cm_db.find("secgrouprule", **args)

            # check if rules exist
            if rule is None:
                return "No rules for security group [{}] in the database. Try cm secgroup refresh."

            # return table
            return (dict_printer(rule,
                                 order=["user",
                                        "category",
                                        "name",
                                        "fromPort",
                                        "toPort",
                                        "protocol",
                                        "cidr"],
                                 output="table"))

        except Exception as ex:
            Console.error(ex.message, ex)

        return None

    @classmethod
    def delete_secgroup(cls, label, cloud):
        try:
            # Find the secgroup from the cloud
            cloud_provider = CloudProvider(cloud).provider
            result = cloud_provider.delete_secgroup(label)
            return result
        except Exception as ex:
            Console.error(ex.message, ex)

    @classmethod
    def delete_rule(cls, cloud, secgroup, from_port, to_port, protocol, cidr):
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

            if rule is not None:
                # get the nova client for cloud
                cloud_provider = CloudProvider(cloud).provider
                # delete the rule from the cloud
                cloud_provider.delete_secgroup_rule(rule.uuid)
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
    nova = CloudProvider.set("kilo")

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
