""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_libcloud/test_libcloud_api.py:Test_image.test_001

nosetests -v --nocapture tests/libcloud/test_libcloud_api.py

or

nosetests -v tests/test_image.py

"""

from cloudmesh_client.util import HEADING
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.ConfigDict import ConfigDict




class Test_libcloud_api():
    """
        This class tests the ImageCommand
    """

    def test_001(self):


        from libcloud.compute.types import Provider
        from libcloud.compute.providers import get_driver

        config = ConfigDict('cloudmesh.yaml')
        print (config)
        credential = dict(config["cloudmesh"]["clouds"]["chameleon-ec2"]["credentials"])
        print (credential)
        EC2_ACCESS_KEY = credential['EC2_ACCESS_KEY']
        EC2_SECRET_KEY = credential['EC2_SECRET_KEY']

        Driver = get_driver(Provider.EC2)
        conn = Driver(EC2_ACCESS_KEY, EC2_SECRET_KEY)

        keys = conn.list_key_pairs()

        print (keys)


    '''
    def test_002(self):
        """
        test key list
        :return:
        """
        HEADING()


        from pprint import pprint

        cloud = "chameleon-ec2"
        provider = CloudProvider(cloud).provider

        print (provider, type(provider))

        # pprint (provider.__dict__)
        # pprint (dir(provider))

        #r = provider.list_flavor(cloud)
        #pprint(r)

        for kind in ["key"]: # ["image", "vm", "flavor", "key"]: # , "flavor", "vm", "limits", "quota"]:
            r = provider.list(kind, cloud)
            pprint(r)

        assert True
    '''