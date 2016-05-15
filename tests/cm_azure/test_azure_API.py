""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_azure_API.py:Test_azure_api.test_001
python setup.py install; py.test tests/cm_cloud/test_azure_API.py:Test_azure_api.test_001
nosetests -v --nocapture tests/test_list.py

or

nosetests -v tests/test_list.py

"""

from pprint import pprint

from cloudmesh_client import ConfigDict
from cloudmesh_client.cloud.iaas.provider.azure.CloudProviderAzureAPI import CloudProviderAzureAPI
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default


class Test_azure_API:
    provider = None
    credentials = None
    clouddefault = None
    cloud_name = "azure"
    data = dotdict({
        "cloud": Default.cloud,
        "format": "json",
        "user": "fake",
        "wrong_cloud": "no_cloud",
        "key": "my_default_key",
        "value": "my_default_value"
    })

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c="-")
        print(command)
        parameter = command.split(" ")
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print(result)
        return str(result)

    def setup(self):
        cloud_name = "azure"
        d = ConfigDict("cloudmesh.yaml")
        cloud_details = d["cloudmesh"]["clouds"][cloud_name]
        self.credentials = d["cloudmesh"]["clouds"][cloud_name]['credentials']
        self.clouddefault = d["cloudmesh"]["clouds"][cloud_name]['default']
        self.provider = CloudProviderAzureAPI(cloud_name, cloud_details)
        self.cloud_name = "azure"

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_001(self):
        HEADING("List VMs")
        pprint(self.provider.list_vm(self.cloud_name))

    def test_002(self):
        HEADING("List Images")
        pprint(self.provider.list_image(self.cloud_name))

    def test_003(self):
        HEADING("List Flavors")
        pprint(self.provider.list_flavor(self.cloud_name))

    def test_004(self):
        HEADING("Create VM test")
        vm_name = "test-001"
        image_id = self.clouddefault["image"]
        flavor_id = self.clouddefault["flavor"]
        self.provider.boot_vm(name=vm_name, image=image_id, flavor=flavor_id)
        # pprint(self.provider.list_secgroup_rules(self.cloud_name))



# TODO: define tests to test each of the important methods defined in
#           cp = CloudProviderAzureAPI(cloudname, cloud_details)
