""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_libcloud/test_libcloud_api.py:Test_libcloud_native.test_001

nosetests -v --nocapture tests/libcloud/test_libcloud_api.py

or

nosetests -v tests/test_image.py

"""

from __future__ import print_function

import re
from pprint import pprint

from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider

from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.util import HEADING


# noinspection PyPep8Naming
class Test_libcloud_native(object):
    """
    Tests the libcloud native connection to chameleon
    """

    driver = None
    credential = None
    clouddefault = None

    def setup(self):
        cloud = "cybera-ec2"
        config = ConfigDict("cloudmesh.yaml")
        self.credential = config['cloudmesh']['clouds'][cloud]['credentials']
        self.clouddefault = config['cloudmesh']['clouds'][cloud]['default']
        # pprint(dict(self.credential))

        auth_url = self.credential["EC2_URL"]

        data = re.match(r'^http[s]?://(.+):([0-9]+)/([a-zA-Z/]*)',
                        auth_url,
                        re.M | re.I)
        host, port, path = data.group(1), data.group(2), data.group(3)
        print("host: " + host)
        print("port: " + port)
        print("path: " + path)

        extra_args = {'path': path}
        cls = get_driver(Provider.EC2_US_EAST)
        self.driver = cls(
            self.credential['EC2_ACCESS_KEY'],
            self.credential['EC2_SECRET_KEY'],
            host=host,
            port=port,
            **extra_args)
        print("DRIVER", self.driver)
        assert "libcloud.compute.drivers.ec2.EC2NodeDriver object at" in str(self.driver)

    def test_002(self):
        """list VMs"""
        HEADING()
        pprint(self.driver)
        nodes = self.driver.list_nodes()
        pprint("Nodes", nodes)
        assert True

    def test_003(self):
        """list images"""
        HEADING()
        print(self.driver)
        images = self.driver.list_images()
        print("Images", images)
        assert len(images) > 0

    def test__004(self):
        """list flavors"""
        HEADING()
        print(self.driver)
        sizes = self.driver.list_sizes()
        print("Flavor", sizes[0])
        assert len(sizes) > 0

    def test_005(self):
        # specify flavor and image
        HEADING()
        print(self.driver)
        myflavor = self.clouddefault['flavor']
        sizes = self.driver.list_sizes()
        size = [s for s in sizes if s.id == myflavor][0]
        print(size)
        assert True

    def test_006(self):
        # Changed "name" -> "id" (diff from openstack)
        HEADING()
        print(self.driver)
        myimage = self.clouddefault['image']
        images = self.driver.list_images()
        image = [i for i in images if i.name == myimage][0]
        print(image)
        assert True

    def test_007(self):
        """launch a new VM"""
        HEADING()
        print(self.driver)

        myimage = self.clouddefault['image']
        images = self.driver.list_images()
        image = [i for i in images if i.name == myimage][0]

        myflavor = self.clouddefault['flavor']
        sizes = self.driver.list_sizes()
        size = [s for s in sizes if s.id == myflavor][0]

        name = "{:}-libcloud".format(self.credential['userid'])
        node = self.driver.create_node(name=name, image=image, size=size)
        print(node)
        assert True

    def test_008(self):
        """check if the new VM is in the list"""
        HEADING()
        print(self.driver)
        nodes = self.driver.list_nodes()
        print(nodes)
        assert True

    '''
    def test_009(self):
        """public ip"""
        HEADING()
        # wait the node to be ready before assigning public IP
        sleep(10)

        # public IPs
        # get the first pool - public by default
        # create an ip in the pool
        elastic_ip = self.driver.ex_allocate_address()

        # attach the ip to the node
        self.driver.ex_associate_address_with_node(node, elastic_ip)

        # check updated VMs list to see if public ip is assigned
        nodes = self.driver.list_nodes()
        print (nodes)
        assert True


    def test_010(self):
        """remove node"""
        HEADING()
        # delete the ip

        # delete vm
        node.destroy()
        assert True
    '''
