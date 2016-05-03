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
            "rule_ssh": "443 443 tcp  0.0.0.0/0",
        }
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

        # passed
        def add_group(cloud, groupname):
            provider = CloudProvider(cloud).provider
            return provider.create_secgroup(groupname)

        # passed
        def delete_group(cloud, groupname):
            provider = CloudProvider(data.cloud).provider
            return provider.delete_secgroup(groupname)

        def add_rule(cloud, groupname, rulename):
            ret = None
            provider = CloudProvider(data.cloud).provider
            # fetch rule from db
            cm = CloudmeshDatabase()
            db_rule = cm.find(kind="secgrouprule", category="general", name=rulename, scope='first', output='dict')
            kwargs = db_rule
            group = get_group(cloud, groupname)
            if group:
                groupid = group["id"]
                kwargs["uuid"] = groupid
                print (kwargs)
                ret = provider.add_secgroup_rule(kwargs)
            return ret

        def delete_rule(cloud, groupname, rulename):
            pass

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

            Console.error("not implemented", traceflag=False)

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

        # testing each individual method defined in this test
        #
        pprint (list_groups(data.cloud))
        print("dgroup", self.data.dgroup)
        dgroup = self.data.dgroup
        # pprint (get_group(data.cloud, "default"))
        # pprint (list_rules(data.cloud, "default"))
        # pprint (get_rule(data.cloud, "default", "ssh"))

        # testing adding and deleting groups
        # all passed
        print ("...should be None")
        pprint(get_group(data.cloud, dgroup))

        '''

        print ("...should return the newly created object")
        pprint(add_group(data.cloud, "fwtest"))
        print ("...should be NOT None")
        pprint(get_group(data.cloud, "fwtest"))
        print ("...deleting")
        pprint(delete_group(data.cloud, "fwtest"))
        print ("...should be None")
        pprint(get_group(data.cloud, "fwtest"))
        '''

        ''' Not yet completed
        # testing adding and deleting rules
        print ("...should return the newly created object")
        pprint(add_group(data.cloud, "fwtest"))
        print ("...adding ssh rule")
        pprint(add_rule(data.cloud, "fwtest", "ssh"))
        print ("...listing the group. Should have the ssh rule int it")
        pprint(get_group(data.cloud, "fwtest"))
        print ("...deleting the testing group")
        pprint(delete_group(data.cloud, "fwtest"))
        '''
