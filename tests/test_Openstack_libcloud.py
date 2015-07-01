""" run with

nosetests -v --nocapture

or

nosetests -v

"""
from __future__ import print_function
from cloudmesh_base.util import HEADING
from cloudmesh_client.iaas.openstack_libcloud import OpenStack_libcloud

class Test_pass:
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_dummy(self):
        HEADING()

        cloud = OpenStack_libcloud("india")

        print(cloud.limits())
        assert True
