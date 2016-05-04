""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_secgroup.py:Test_secgroup.test_001

nosetests -v --nocapture tests/test_secgroup.py

or

nosetests -v tests/test_secgroup.py

"""

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default

from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from pprint import pprint
from cloudmesh_client.shell.console import Console
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
'''
cm secgroup list
cm secgroup list --cloud=kilo
cm secgroup add  cm-gregor-default web 80 80 tcp  0.0.0.0/0
cm secgroup add  cm-gregor-default ssh 22 22 tcp  0.0.0.0/0
cm secgroup upload --cloud=kilo
'''


# noinspection PyPep8Naming
class Test_secgroup:

    data = dotdict({
        "dgroup": "{}-default".format(Default.user),
        "cloud": Default.cloud,
        "group": "cm-{}-test".format(Default.user),
        "wrong_cloud": "no_cloud",
        "rules": {
            "rule_http": "80 80 tcp  0.0.0.0/0",
            "rule_https": "443 443 tcp  0.0.0.0/0",
            "rule_ssh": "22 22 tcp  0.0.0.0/0",
        },
        "image": Default.get_image(category=Default.cloud),
        "flavor": Default.get_flavor(category=Default.cloud),
        "vm": "{}_testsecgroup".format(Default.user),
    })
    for rule in data.rules:
        data[rule] = data.rules[rule]

    data.tenant = ConfigDict("cloudmesh.yaml")["cloudmesh.clouds"][data.cloud]["credentials"]["OS_TENANT_NAME"]

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c="-")
        print(command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return str(result)

    def setup(self):
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_001(self):
        HEADING("cm secgroup add ...")
        for rule in self.data.rules:
            command = "cm secgroup add  {} {} {}".format(self.data.group, rule, self.data["rules"][rule])
            result = self.run(command)

        command = "cm secgroup list"
        result = self.run(command)

        for rule in self.data.rules:
            assert rule in result

    def test_002(self):
        HEADING("cm secgroup delete ...")

        command = "cm secgroup delete {group}".format(**self.data)

        result = self.run(command)

        result = self.run("cm secgroup list")

        assert self.data.group not in result

    def test_003(self):

        HEADING("secgroup api")

        data = dotdict({
            'cloud': "cm",
            'groupname': 'gvonlasz-default'
        })
        provider = CloudProvider(data.cloud).provider

        groups = None
        rules = provider.list_secgroup(data.cloud)

        """
        # passed
        def add_group(cloud, groupname):
            provider = CloudProvider(cloud).provider
            return provider.create_secgroup(groupname)

        # passed
        def delete_group(cloud, groupname):
            provider = CloudProvider(data.cloud).provider
            return provider.delete_secgroup(groupname)

        # passed
        def add_rule(cloud, groupname, rulename):
            ret = None
            provider = CloudProvider(data.cloud).provider
            # fetch rule from db
            cm = CloudmeshDatabase()
            db_rule = cm.find(kind="secgrouprule", category="general", name=rulename, scope='first', output='dict')
            kwargs = {}
            kwargs["protocol"] = db_rule["protocol"]
            kwargs["cidr"] = db_rule["cidr"]
            kwargs["from_port"] = db_rule["fromPort"]
            kwargs["to_port"] = db_rule["toPort"]
            group = get_group(cloud, groupname)
            if group:
                groupid = group["id"]
                kwargs["uuid"] = groupid
                print (kwargs)
                ret = provider.add_secgroup_rule(**kwargs)
            return ret

        # passed
        def delete_rule(cloud, groupname, rulename):
            ret = None
            provider = CloudProvider(data.cloud).provider
            ruleid = get_rule(cloud, groupname, rulename)
            if ruleid:
                ret = provider.delete_secgroup_rule(ruleid)
            else:
                Console.error("Rule does not exist - Rule:{}, Group:{}".format(rulename, groupname))
            return ret

        # passed
        def list_groups(cloud):
            provider = CloudProvider(cloud).provider
            groups = provider.list_secgroup(cloud)
            return groups

        # passed
        def get_group(cloud, groupname):
            provider = CloudProvider(cloud).provider
            groups = provider.list_secgroup(cloud)
            ret = None
            for groupkey in groups:
                group = groups[groupkey]
                if group["name"] == groupname:
                    ret = group
                    break
            return ret

        # passed
        def list_rules(cloud, groupname):
            provider = CloudProvider(cloud).provider
            groups = provider.list_secgroup(cloud)
            for id in groups:
                group = groups[id]
                if groupname == group["name"]:
                    return group["rules"]
            return None

        # passed
        def get_rule(cloud, groupname, rulename):
            rules = list_rules(cloud, groupname)
            # find properties for db rule

            cm = CloudmeshDatabase()
            db_rule = cm.find(kind="secgrouprule", category="general", name=rulename, scope='first', output='dict')

            #db_rule = {u'from_port': 80,
            #          u'ip_protocol': u'tcp',
            #          u'ip_range': {u'cidr': u'0.0.0.0/0'},
            #          u'to_port': 80},
            ruleid = None
            for rule in rules:

                if 'cidr' in rule['ip_range']:
                    if (db_rule["fromPort"] == str(rule['from_port']) and
                        db_rule["toPort"] == str(rule['to_port']) and
                        db_rule["protocol"] == rule['ip_protocol'] and
                        db_rule["cidr"] == rule['ip_range']['cidr']
                        ):
                        ruleid = rule['id'] #uuid for the rule
            return ruleid
        """

        # testing each individual method defined in this test
        #
        # list/get of groups/rules
        # all passed
        # pprint (list_groups(data.cloud))
        # print("dgroup", self.data.dgroup)
        # dgroup = self.data.dgroup
        # pprint (get_group(data.cloud, "default"))
        # pprint (list_rules(data.cloud, "default"))
        # pprint (get_rule(data.cloud, "default", "ssh"))

        # print ("...should be None")
        # pprint(get_group(data.cloud, dgroup))

        '''
        # testing adding and deleting groups
        # all passed
        print ("...should be None")
        pprint(get_group(data.cloud, "fwtest"))
        print ("...should return the newly created object")
        pprint(add_group(data.cloud, "fwtest"))
        print ("...should be NOT None")
        pprint(get_group(data.cloud, "fwtest"))
        print ("...deleting")
        pprint(delete_group(data.cloud, "fwtest"))
        print ("...should be None")
        pprint(get_group(data.cloud, "fwtest"))
        '''

        '''
        # testing adding and deleting rules
        # all passed
        print ("...should return the newly created object")
        pprint(add_group(data.cloud, "fwtest"))
        print ("...adding ssh rule")
        pprint(add_rule(data.cloud, "fwtest", "ssh"))
        print ("...listing the group. Should have the ssh rule int it")
        pprint(get_group(data.cloud, "fwtest"))
        print ("...deleting ssh rule")
        pprint(delete_rule(data.cloud, "fwtest", "ssh"))
        print ("...listing the group. ssh rule should be gone")
        pprint(get_group(data.cloud, "fwtest"))
        print ("...deleting the testing group")
        pprint(delete_group(data.cloud, "fwtest"))
        '''

    def test_004(self):
        '''
        A through test of deleting/updating secgroups.
        It creates in the db a testing group with 3 rules;
        Uploading the secgroup to cloud;
        booting a vm with this newly created group;
        deleting the secgroup (should fail as being used);
        updating rules for the secgroup
        (should succeed - updating rules, but not creating duplicated group);
        cleaning up...
            delete the testing vm
            deleting the testing secgroup
        '''

        HEADING("creating testing group in db and populate with rules")
        for rule in self.data.rules:
            command = "cm secgroup add  {} {} {}".format(self.data.group, rule, self.data["rules"][rule])
            result = self.run(command)

        HEADING("uploading the newly created secgroup to default cloud")
        command = "cm secgroup upload {} --cloud={}".format(self.data.group, self.data.cloud)
        result = self.run(command)

        HEADING("listing secgroup in default cloud")
        command = "cm secgroup list --cloud={}".format(self.data.cloud)
        result = self.run(command)
        assert "80" in result and self.data.group in result

        HEADING("booting a vm with the test secgroup")
        command = "cm vm boot --name={vm} --cloud={cloud} --image={image}" + \
                  " --flavor={flavor} --secgroup={group}"
        result = self.run(command)
        assert "OK." in result

        HEADING("cm secgroup delete ... Deleting a secgroup that is being used")
        command = "cm secgroup delete {} --cloud={}".format(self.data.group, self.data.cloud)
        result = self.run(command)
        assert "ERROR" in result and "in use" in result

        HEADING("adding new rule to the test secgroup (change in db)")
        command = "cm secgroup add {} ssh 8765 8765 tcp 0.0.0.0/0".format(self.data.group)
        result = self.run(command)
        HEADING("updating the teseting secgroup in the default cloud (upload to cloud)")
        command = "cm secgroup upload {} --cloud={}".format(self.data.group, self.data.cloud)
        result = self.run(command)

        HEADING("cm secgroup list --cloud={}".format(self.data.cloud))
        command = "cm secgroup list --cloud={}".format(self.data.cloud)
        result = self.run(command)
        assert "8765" in result

        HEADING("Cleaning up......")
        HEADING("deleting the test vm and the test secgroup")
        command = "cm vm delete {}".format(self.data.vm)
        result = self.run(command)
        command = "cm secgroup delete {} --cloud={}".format(self.data.group, self.data.cloud)
        result = self.run(command)
        command = "cm secgroup list --cloud={}".format(self.data.cloud)
        result = self.run(command)
        assert self.data.group not in result
