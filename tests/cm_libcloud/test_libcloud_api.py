""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_libcloud/test_libcloud_api.py:Test_libcloud_api.test_001

nosetests -v --nocapture tests/libcloud/test_libcloud_api.py

or

nosetests -v tests/test_image.py

"""

from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
from cloudmesh_client.common.util import HEADING


# noinspection PyMethodMayBeStatic,PyPep8Naming
class Test_libcloud_api(object):
    """
        This class tests the ImageCommand
    """

    '''
    def test_001(self):


        from libcloud.compute.types import Provider
        from libcloud.compute.providers import get_driver

        config = ConfigDict('cloudmesh.yaml')
        # print (config)
        credential = dict(config["cloudmesh"]["clouds"]["chameleon-ec2"]["credentials"])
        pprint (dict(credential))
        EC2_ACCESS_KEY = credential['EC2_ACCESS_KEY']
        EC2_SECRET_KEY = credential['EC2_SECRET_KEY']

        Driver = get_driver(Provider.EC2)
        conn = Driver(EC2_ACCESS_KEY, EC2_SECRET_KEY)

        keys = conn.list_images()

        print (keys)


    '''

    def test_001(self):
        """test image list :return: """
        HEADING()

        from pprint import pprint

        cloud = "chameleon-ec2"
        provider = CloudProvider(cloud).provider

        print(provider, type(provider))

        # pprint (provider.__dict__)
        # pprint (dir(provider))

        # r = provider.list_flavor(cloud)
        # pprint(r)

        for kind in ["image"]:  # ["image", "vm", "flavor", "key"]: # , "flavor", "vm", "limits", "quota"]:
            r = provider.list(kind, cloud)
            pprint(r)

        assert True

    def test_002(self):
        """ test flavor list :return:  """
        HEADING()

        from pprint import pprint

        cloud = "chameleon-ec2"
        provider = CloudProvider(cloud).provider

        # print (provider, type(provider))

        # r = provider.list_flavor(cloud)
        # pprint(r)

        kind = 'flavor'

        r = provider.list(kind, cloud)
        pprint(r)

        assert 't2.small' in str(r)

        r = provider.list_flavor(cloud)
        pprint(r)

        assert 't2.small' in str(r)

        r = provider.provider.list_sizes(cloud)
        pprint(r)

        assert 't2.small' in str(r)

    def test_003(self):
        """ test vm list:return:  """
        HEADING()

        from pprint import pprint

        cloud = "chameleon-ec2"
        provider = CloudProvider(cloud).provider

        print(provider, type(provider))

        # pprint (provider.__dict__)
        # pprint (dir(provider))

        # r = provider.list_flavor(cloud)
        # pprint(r)

        for kind in ["vm"]:  # ["image", "vm", "flavor", "key"]: # , "flavor", "vm", "limits", "quota"]:
            r = provider.list(kind, cloud)
            pprint(r)

        assert True

    def test_004(self):
        """ test key list:return:"""
        HEADING()

        from pprint import pprint

        cloud = "chameleon-ec2"
        provider = CloudProvider(cloud).provider

        print(provider, type(provider))

        # pprint (provider.__dict__)
        # pprint (dir(provider))

        # r = provider.list_flavor(cloud)
        # pprint(r)

        for kind in ["key"]:  # ["image", "vm", "flavor", "key"]: # , "flavor", "vm", "limits", "quota"]:
            r = provider.list(kind, cloud)
            pprint(r)

        assert True
