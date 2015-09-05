""" run with


python setup.py install; nosetests -v --nocapture  tests/test_iaas_openstack_compute.py:Test_openstack.test_001

nosetests -v --nocapture  tests/test_iaas_openstack_compute.py

or

nosetests --nocapture  tests/test_iaas_openstack_compute.py

"""

from cloudmesh_base.util import HEADING
from cloudmesh_client.iaas.openstack.compute import compute
from pprint import pprint
from cloudmesh_base.util import banner

class Test_openstack:

    cloud = compute("india")


    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """images"""
        HEADING()
        banner("get_images()")
        pprint(self.cloud.get_images())
        banner("images")
        pprint(self.cloud.images)

        assert True


    def test_002(self):
        """flavors"""
        HEADING()
        banner("get_flavors()")
        pprint(self.cloud.get_flavors())
        banner("flavors")
        pprint(self.cloud.flavors)

    def test_003(self):
        """vms"""
        HEADING()

        banner("get_vms()")
        pprint(self.cloud.get_servers())
        banner("servers")
        print ("TTTT")
        r = self.cloud.servers
        pprint (r)

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
