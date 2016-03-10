from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security
from __future__ import print_function
from cloudmesh_client.common.ConfigDict import ConfigDict
from time import sleep
from pprint import pprint


""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_libcloud/test_libcloud_api.py:Test_image.test_001

nosetests -v --nocapture tests/libcloud/test_libcloud_api.py

or

nosetests -v tests/test_image.py

"""

from cloudmesh_client.util import HEADING
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.ConfigDict import ConfigDict


from pprint import pprint

class Test_libcloud_api():
    """
    Tests the libcloud native connection to chameleon
    """

    def test_001(self):
        self.config = ConfigDict("cloudmesh.yaml")
        self.credentials = self.config['cloudmesh']['clouds']['aws']['credentials']
        self.default = self.conf['cloudmesh']['clouds']['aws']['default']
        pprint(self.credentials)

        self.cls = cls = get_driver(Provider.EC2_US_EAST)
        self.driver = cls(
            self.credentials['EC2_ACCESS_KEY'],
            self.credentials['EC2_SECRET_KEY'])

    def test_002(self):
        """list VMs"""
        self.nodes = self.driver.list_nodes()
        print (self.nodes)
        assert True


    def test_003(self):
        """list images"""
        self.images = self.driver.list()
        #print images[0]
        assert True

    def test__004(self):
        """list flavors"""
        self.sizes = self.driver.list_sizes()
        # print sizes
        assert True


    def test_005(self):
        # specify flavor and image
        self.myflavor = self.default['flavor']
        self.myimage = self.default['image']
        assert True

    def test_006(self):

        # Changed "name" -> "id" (diff from openstack)
        size = [s for s in self.sizes if s.id == self.myflavor][0]
        image = [i for i in self.images if i.id == self.myimage][0]
        assert True

    def test_007(self):
        """launch a new VM"""
        name = "{:}-libcloud".format(self.credential['userid'])
        node = self.driver.create_node(name=name, image=self.image, size=self.size)
        assert True

    def test_008(self):
        """check if the new VM is in the list"""
        nodes = self.driver.list_nodes()
        print (nodes)
        assert True

    def test_009(self):
        """public ip"""

        # wait the node to be ready before assigning public IP
        sleep(10)

        # public IPs
        # get the first pool - public by default
        # create an ip in the pool
        elastic_ip = self.driver.ex_allocate_address()

        # attach the ip to the node
        self.driver.ex_associate_address_with_node(self.node, elastic_ip)

        # check updated VMs list to see if public ip is assigned
        nodes = self.driver.list_nodes()
        print (nodes)
        assert True


    def test_010(self):
        """remove node"""

        # delete the ip

        # delete vm
        self.node.destroy()
        assert True
