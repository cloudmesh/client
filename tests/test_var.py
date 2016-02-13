""" run with

python setup.py install; nosetests -v --nocapture tests/test_var.py:Test_var.test_001

nosetests -v --nocapture tests/test_default.py

or

nosetests -v tests/test_vm.py

"""
from cloudmesh_base.Shell import Shell
from cloudmesh_base.util import HEADING

from cloudmesh_client.var import Var


def run(command):
    print(command)
    parameter = command.split(" ")
    shell_command = parameter[0]
    args = parameter[1:]
    result = Shell.execute(shell_command, args)
    print(result)
    return result


class Test_default():
    """

    """

    def setup(self):
        pass

    def test_001(self):
        """
        delete defaults
        :return:
        """
        HEADING()
        Var.clear()
        print (Var.list())
        assert Var.list() == None

    def _check(self, content):
        result = Var.list()
        print(result)
        assert content in str(result)

    def test_002(self):
        """
        set default variable
        :return:
        """
        HEADING()
        name = "myvar"
        value = "myvalue"
        Var.set(name, value)
        print (Var.list())
        assert Var.get(name) == value
        self._check(value)

    def test_003(self):
        """
        delete default variable
        :return:
        """
        HEADING()
        Var.clear()
        name = "deleteme"
        value = "myvalue"
        Var.set(name, value)
        print (Var.list())
        Var.delete(name)
        print (Var.list())
        self._check("None")


    '''
    def test_003(self):
        """cm default test=testValue --cloud=mycloud"""
        HEADING()
        result = run("cm default test=testValue --cloud=mycloud")
        print ("HHHH", result)

        assert "ok." in result

    def test_009(self):
        """cm default test --cloud=mycloud"""
        HEADING()
        run("cm default test=testValue --cloud=mycloud")
        result = run("cm default test --cloud=mycloud")
        assert "testValue" in result

    def test_010(self):
        """cm default doesnotexist --cloud=mycloud"""
        HEADING()
        result = run("cm default doesnotexist --cloud=mycloud")
        assert "No default values found" in result

    def test_011(self):
        """cm default delete test"""
        HEADING()
        run("cm default test=testValue --cloud=mycloud")
        result = run("cm default delete test --cloud=mycloud")
        print result
        assert "Deleted key" in result

    def test_012(self):
        """cm default delete doesnotexist --cloud=mycloud"""
        HEADING()
        result = run("cm default delete doesnotexist --cloud=mycloud")
        assert "Key doesnotexist not present" in result

    '''

    def test_999(self):
        """
        clear the defaults
        :return:
        """
        HEADING()

        Var.clear()
        Var.list()
        assert True

    '''
    def test_002(self):
        """
        tries to start a vm with an invalid image
        :return:
        """
        HEADING()
        result = run ("cm vm start --cloud=india --flavor=m1.medium --image=futuresystems/linux>windows")

        assert "not found" in result
    '''
