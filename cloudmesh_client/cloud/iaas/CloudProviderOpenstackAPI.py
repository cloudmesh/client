from cloudmesh_client.cloud.iaas.CloudProviderBase import CloudProviderBase
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.common.ConfigDict import Config, ConfigDict

from keystoneclient.auth.identity import v3
from keystoneclient import session
from novaclient import client
import requests

from cloudmesh_client.common.Printer import attribute_printer
from cloudmesh_client.common.Printer  import dict_printer
from cloudmesh_base.Shell import Shell
from cloudmesh_client.common.TableParser import TableParser
from cloudmesh_client.cloud.nova import Nova

requests.packages.urllib3.disable_warnings()


# TODO: unset as not allowing to smoothly switch
def set_os_environ(cloudname):
    """Set os environment variables on a given cloudname"""
    # TODO: this has a severe bug as it is not unsetting variabes
    # Also this coded duplicates in part from register
    try:
        d = ConfigDict("cloudmesh.yaml")
        credentials = d["cloudmesh"]["clouds"][cloudname]["credentials"]
        for key, value in credentials.iteritems():
            if key == "OS_CACERT":
                os.environ[key] = Config.path_expand(value)
            else:
                os.environ[key] = value
    except Exception, e:
        print(e)

#
# we already have a much better convert to dict function
#
# TODO: this function will be deprectaed
@classmethod
def convert_to_dict(cls, openstack_result):
    d = {}
    for i, key in enumerate(openstack_result.keys()):
        d[i] = {}
        if "id" not in key:
            d[i]["Quota"], d[i]["Limit"] = key, openstack_result[key]
    return d


class CloudProviderOpenstackAPI(CloudProviderBase):
    def __init__(self, cloud_name, cloud_details):
        self.initialize(cloud_name, cloud_details)

    def _ksv3_auth(self, credentials):
        # auth to identity v3
        ksauth = v3.Password(auth_url=credentials["OS_AUTH_URL"],
                             username=credentials["OS_USERNAME"],
                             password=credentials["OS_PASSWORD"],
                             project_name=credentials["OS_PROJECT_NAME"],
                             user_domain_name=credentials["OS_USER_DOMAIN_ID"],
                             project_domain_name=credentials[
                                 "OS_PROJECT_DOMAIN_ID"])

        return ksauth

    def initialize(self, cloud_name, cloud_details):
        self.cloud = cloud_name
        self.default_flavor = cloud_details["default"]["flavor"]
        self.default_image = cloud_details["default"]["image"]
        version = 2
        credentials = cloud_details["credentials"]
        cert = False
        if "OS_CACERT" in credentials:
            if credentials["OS_CACERT"] is not False:
                cert = Config.path_expand(credentials["OS_CACERT"])
        auth_url = credentials["OS_AUTH_URL"]
        ksversion = auth_url.split("/")[-1]

        if "v2.0" == ksversion:
            self.nova = client.Client(version,
                                      credentials["OS_USERNAME"],
                                      credentials["OS_PASSWORD"],
                                      credentials["OS_TENANT_NAME"],
                                      credentials["OS_AUTH_URL"],
                                      cert)
        elif "v3" == ksversion:
            sess = session.Session(auth=self._ksv3_auth(credentials),
                                   verify=cert)
            self.nova = client.Client(2, session=sess)

    def mode(self, source):
        """
        Sets the source for the information to be returned. "db" and "cloud"
        :param source: the database can be queried in mode "db",
        the database can be bypassed in mode "cloud"
        """
        TODO.implement()

    def list(self):
        """
        Returns list of all the vm instances.
        :return:List of Servers
        """
        return self.nova.servers.list()

    def boot(self, name, image=None, flavor=None, cloud="India", key=None,
             secgroup=None, meta=None):
        """
        Spawns a VM instance on the cloud.
        If image and flavor passed as none, it would consider the defaults specified in cloudmesh.yaml.

        :param name: Name of the instance to be started
        :param image: Image id to be used for the instance
        :param flavor: Flavor to be used for the instance
        :param cloud: Cloud on which to spawn the machine. Defaults to 'India'.
        :param key: Key to be used for the instance
        :param secgroup: Security group for the instance
        :param meta: A dict of arbitrary key/value metadata to store for this server
        """
        if image is None:
            image = self.default_image
        if flavor is None:
            flavor = self.default_flavor

        server = self.nova.servers.create(name, image, flavor, meta=meta,
                                          key_name=key,
                                          security_groups=secgroup)
        # return the server id
        return server.__dict__["id"]

    def delete(self, name, group=None, force=None):
        """
        Deletes a machine on the target cloud indicated by the id
        :param id: Name or ID of the instance to be deleted
        :param group: Security group of the instance to be deleted
        :param force: Force delete option
        :return:
        """
        server = self.nova.servers.find(name=name)
        server.delete()

    def get_ips(self, name, group=None, force=None):
        """
        Returns the ip of the instance indicated by name_or_id
        :param name_or_id:
        :param group:
        :param force:
        :return: IP address of the instance
        """
        server = self.nova.servers.find(name=name)
        return self.nova.servers.ips(server)

    def create_assign_floating_ip(self, server_name):
        """
        Function creates a new floating ip and associates it with the machine specified.
        :param server_name: Name of the machine to which the floating ip needs to be assigned.
        :return: Floating IP | None if floating ip already assigned.
        """

        float_pool = self.nova.floating_ip_pools.list()[0].name

        floating_ip = self.nova.floating_ips.create(pool=float_pool)
        server = self.nova.servers.find(name=server_name)
        try:
            server.add_floating_ip(floating_ip)
        except Exception, e:
            print (e)
            self.nova.floating_ips.delete(floating_ip)
            return None

        return floating_ip.ip

    # TODO: define this
    def get_image(self, **kwargs):
        """
        finds the image based on a query
        TODO: details TBD
        """
        TODO.implement()

    # TODO: define this
    def get_flavor(self, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        TODO.implement()

    # TODO: define this
    def get_vm(self, **kwargs):
        """
        finds the flavor based on a query
        TODO: details TBD
        """
        TODO.implement()

    @classmethod
    def list_limits(cls, cloud, output="table", tenant=None):
        try:
            # nova = CloudProvider.set(cloud)
            result = cls.nova.limits.get(tenant_id=tenant)._info["absolute"]
            return attribute_printer(result, output=output)
        except Exception, e:
            return e

    def list(cls, cloud, start, end, tenant, format):
        # TODO: consider named arguments
        #def list(cls, cloud, start=None,
        #         end=None, tenant=None, output="table"):
        # set the environment variables
        set_os_environ(cloud)
        try:
            # execute the command
            args = ["usage"]
            if start is not None:
                args.extend(["--start", start])
            if end is not None:
                args.extend(["--end", end])
            if tenant is not None:
                args.extend(["--tenant", tenant])

            result = Shell.execute("nova", args)
            result = Nova.remove_subjectAltName_warning(result)

            lines = result.splitlines()
            dates = lines[0]

            table = '\n'.join(lines[1:])

            dates = dates.replace("Usage from ", "").\
                replace("to", "").replace(" +", " ")[:-1].split()

            #
            # TODO: for some reason the nova command has returned not the
            # first + char, so we could not ignore the line we may set - as
            # additional comment char, but that did not work
            #
            d = TableParser.convert(result, comment_chars="+#")


            d["0"]["start"] = "start"
            d["0"]["end"] = "end"

            d["1"]["start"] = dates[0]
            d["1"]["end"] = dates[1]

            del d['0']

            return dict_printer(d,
                                       order=["start",
                                              "end",
                                              "servers",
                                              "cpu hours",
                                              "ram mb-hours",
                                              "disk gb-hours"],
                                       output=format)

        except Exception, e:
            return e
