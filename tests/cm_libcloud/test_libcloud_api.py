""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_libcloud/test_libcloud_api.py:Test_image.test_001

nosetests -v --nocapture tests/libcloud/test_libcloud_api.py

or

nosetests -v tests/test_image.py

"""

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING
from cloudmesh_client.cloud.iaas.CloudProvider import CloudProvider
import json



class Test_libcloud_api():
    """
        This class tests the ImageCommand
    """

    def test_001(self):
        """
        test image refresh
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

        for kind in ["image"]: # , "flavor", "vm", "limits", "quota"]:
            r = provider.list(kind, cloud)
            pprint(r)

        assert True