""" run with

python setup.py install; nosetests -v --nocapture  tests/test_keys.py:Test_keys.test_001

nosetests -v --nocapture

or

nosetests -v

"""

from pprint import pprint

# from cloudmesh_client.keys.SSHKeyManager import SSHKeyManager
# from cloudmesh_client.keys.SSHkey import SSHkey
# from cloudmesh_client.db.SSHKeyDBManager import SSHKeyDBManager
# from cloudmesh_client.common.tables import dict_printer

from cloudmesh_base.util import HEADING
#
from cloudmesh_base.Shell import Shell


def run(command):
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    return result


class Test_keys:
    def setup(self):
        pass

    def tearDown(self):
        pass

    """
    def test_001(self):
        reading the keys from ~/.ssh
        HEADING()

        mykeys = SSHKeyManager()

        banner("ssh keys")
        mykeys.get_from_dir("~/.ssh")


        assert len(mykeys) > 0

    def test_002(self):
        reading the keys from github
        HEADING()

        # from cloudmesh_client.common import cloudmesh_yaml
        #config = ConfigDict(filename=cloudmesh_yaml")
        #git_username = config['cloudmesh']['github']['username']
        git_username = 'laszewsk'

        mykeys = SSHKeyManager()

        banner("git hub")
        mykeys.get_from_git(git_username)

        count1 = len(mykeys)

        banner("all")
        mykeys.get_all(git_username)

        count2 = len(mykeys)

        # d = mykeys.dict()
        print (mykeys.table)

        mykeys.__delitem__('github-0')
        print (mykeys.table)

        assert count1 > 0 and count2 >0


    def test_003(self):
        testing properties in SSHKey
        HEADING()


        sshkey = SSHkey("~/.ssh/id_rsa.pub")
        pprint (sshkey.key)
        print ("Fingerprint:", sshkey.fingerprint)
        pprint (sshkey.__key__)
        print ("sshkey", sshkey)
        print ("str", str(sshkey))
        print (sshkey.type)
        assert True

    def test_004(self):
        HEADING()
        sshdb = SSHKeyDBManager()
        sshdb.delete_all()
        sshdb.add("~/.ssh/id_rsa.pub")

        d = sshdb.dict()
        print d
        print dict_printer(d, output="table")

        d = sshdb.find('PauloR@bebop')
        print ('find function: ', d)

        sshdb.delete('PauloR@bebop')

        d = sshdb.object_to_dict(sshdb.find_all())
        print ("DICT", d)

    def test_005(self):
        HEADING()
        sshm = SSHKeyManager()
        print sshm.get_from_yaml()
    """

    def test_001(self):
        """
        cm key add --name=testkey ~/.ssh/id_rsa.pub
        """
        HEADING()
        result = run("cm key add --name=testkey ~/.ssh/id_rsa.pub")
        print result
        assert "OK." in result

    def test_002(self):
        """
        cm key add --git --name=testkey ~/.ssh/id_rsa.pub
        """
        HEADING()
        result = run("cm key add --git --name=testkey ~/.ssh/id_rsa.pub")
        print result
        assert "OK." in result

    def test_003(self):
        """
        key add --ssh --name=testkey
        """
        HEADING()
        result = run("key add --ssh --name=testkey")
        print result
        assert "OK." in result

    def test_004(self):
        """
        cm key list
        """

        HEADING()
        result = run("cm key list")
        print result
        assert "OK." in result

    def test_005(self):
        """
        cm key list --source=db
        """

        HEADING()
        result = run("cm key list --source=db")
        print result
        assert "OK." in result

    def test_006(self):
        """
        cm key list --source=db --format=json
        """

        HEADING()
        result = run("cm key list --source=db --format=json")
        print result
        assert "OK." in result

    def test_007(self):
        """
        cm key list --source=db --format=yaml
        """

        HEADING()
        result = run("cm key list --source=db --format=yaml")
        print result
        assert "OK." in result

    def test_008(self):
        """
        cm key list --source=db --format=yaml
        """

        HEADING()
        result = run("cm key list --source=db --format=yaml")
        print result
        assert "OK." in result

    def test_009(self):
        """
        cm key list --source=git
        """

        HEADING()
        result = run("cm key list --source=git")
        print result
        assert "OK." in result

    def test_010(self):
        """
        cm key list --source=cloudmesh
        """

        HEADING()
        result = run("cm key list --source=cloudmesh")
        print result
        assert "OK." in result

    def test_011(self):
        """
        cm key list --source=ssh
        """

        HEADING()
        result = run("cm key list --source=ssh")
        print result
        assert "OK." in result

    def test_012(self):
        """
        cm key list --source=cloudmesh
        """

        HEADING()
        result = run("cm key list --source=cloudmesh")
        print result
        assert "OK." in result

    def test_013(self):
        """
        cm key get testkey
        """

        HEADING()
        result = run("cm key get testkey")
        print result
        assert "OK." in result

    def test_014(self):
        """
        cm key default testkey
        """

        HEADING()
        result = run("cm key default testkey")
        print result
        assert "OK." in result

    def test_015(self):
        """
        cm key delete testkey
        """

        HEADING()
        result = run("cm key delete testkey")
        print result
        assert "OK." in result

    def test_016(self):
        """
        cm key delete --all
        """

        HEADING()
        result = run("cm key delete --all")
        print result
        assert "OK." in result


