""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_base.util import HEADING
from cloudmesh_client.iaas.openstack.compute import compute

class Test_pass:
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """connecting"""
        HEADING()
        cloud = compute("india")

        assert True

    """
    cloud = openstack("india")

    name ="%s-%04d" % (cloud.credential["OS_USERNAME"], 1)
    out = cloud.vm_create(name, "m1.tiny", "6d2bca76-8fff-4d57-9f29-50378539b4fa")
    pprint(out)

    """

    # cloud = openstack("india")
    # flavors = cloud.get_flavors()
    # for flavor in flavors:
    # print(flavor)

    # keys = cloud.list_key_pairs()
    # for key in keys:
    # print key.name
    """
    print cloud.find_user_id()

    """

    """
    for i in range (1,3):
        name ="%s-%04d" % (cloud.credential["OS_USERNAME"], i)
        out = cloud.vm_create(name, "m1.tiny", "6d2bca76-8fff-4d57-9f29-50378539b4fa")
        <pprint(out)
    """

    """
    print cloud.find('name', name)
    """

    # cloud.rename("gvonlasz-0001","gregor")
