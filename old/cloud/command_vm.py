from cmd3.console import Console
from cloudmesh_base.Shell import Shell
from os.path import expanduser
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from cloudmesh_client.common.ConfigDict import ConfigDict
import libcloud.security
from cloudmesh_client.common.ConfigDict import Config
from time import sleep
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase


class Command_vm(object):


    # TODO DOES NOT INTERFACE WITH DATABASE

    @classmethod
    def start(cls, name, count, cloud, image, flavor, group):
        """
        TODO: group has not been used yet. fix that

        starts a virtual Machine (VM) or a set of VMs

        :param name: name of the virtual machine
        :type name: string, None
        :param count: give the number of servers to start
        :type count: integer, None
        :param cloud: give a cloud to work on, if not given, selected or default cloud will be used
        :type cloud: integer, None
        :param image: image name
        :type image: string, None
        :param flavor:flavor name. m1.medium, for example
        :type flavor: string, None
        :param group: the group name of server
        :type group: string, None
        :return:
        """

        # TODO: vm start (without arguments) use default cloud, image, flavor, group.
        if cloud is None:  # use default values for cloud, image and flavor
            pass


        config = CloudRegister.get(cloud)
        if cm_type in ["openstack"]:
            provider = Provider.OPENSTACK
            OpenStack = get_driver(provider)
            try:
                cloud_credentials = config['credentials']
            except Exception, e:
                Console.error(e.message)
                return

            # TODO: THIS MAY BE JUST TRUE IF THE CERT PATH EXISTS IN CREDENTIAL

            # set path to cacert and enable ssl connection
            libcloud.security.CA_CERTS_PATH = [Config.path_expand(cloud_credentials['OS_CACERT'])]
            libcloud.security.VERIFY_SSL_CERT = True

            auth_url = "%s/tokens/" % cloud_credentials['OS_AUTH_URL']

            driver = OpenStack(cloud_credentials['OS_USERNAME'],
                               cloud_credentials['OS_PASSWORD'],
                               ex_force_auth_url=auth_url,
                               ex_tenant_name=cloud_credentials['OS_TENANT_NAME'],
                               ex_force_auth_version='2.0_password',
                               ex_force_service_region='regionOne')

            # obtain available images
            # type of images: <class 'libcloud.compute.base.NodeImage'>
            images = driver.list()
            if not [i for i in images if i.name == image]:
                Console.error("Image {:} not found".format(image))
                return
            image = [i for i in images if i.name == image][0]

            # sizes/flavors
            sizes = driver.list_sizes()
            if not [i for i in sizes if i.name == flavor]:
                Console.error("Flavor {:} not found".format(flavor))
                return
            size = [i for i in sizes if i.name == flavor][0]

            if count is None:
                count = 1
            count = int(count)

            def __findsufix():
                # TODO: THIS IS A BIG BUG AS THE NEXT VM NAME IS NOT MANAGED BY SUFFIX
                """
                    Virtual machine name (VM) format:
                      string-001, string-002, ..., string-n
                    returns the max sufix from the VM list. It will be used in the new vm name in order to avoid
                    VMs with the same name.

                    :return: max sufix
                    :return type: string
                """
                nodes = driver.list_nodes()
                sufix = 1
                for i in nodes:
                    n = 0
                    try:
                        n = int(i.name.split('-', 1)[1])  # not always is int(i.name.split('-', 1)[1] a digit
                    except:
                        pass
                    if sufix <= n:
                        sufix = n + 1
                sufix = str(sufix).zfill(3)
                return sufix

            # set vm name
            sufix = __findsufix()
            c = CloudmeshDatabase()
            if name is None:
                c.name(cloud_credentials['OS_USERNAME'] + "-" + sufix)
            else:
                c.name(name + "-" + sufix)

            # launch a new VM
            Console.ok("Booting Virtual Machine...")
            for i in range(0, count):
                name = c.get_name()
                try:
                    node = driver.create_node(name=name, image=image, size=size)
                except Exception, e:
                    Console.error("{:} virtual machines have not been created. {:}".format(count - i, e.message))
                    return
                c.name(c.next_name())

            # wait the node to be ready before assigning public IP
            sleep(10)
            Console.ok("Virtual Machine created")
        else:
            Console.error('cloud {:} not found'.format(cloud))

    @classmethod
    def delete(cls, name_or_id, group, cloud, force=False):
        """
       deletes a VM or a set of VM

       :param name_or_id: name or id of the vm to be deleted
       :type name_or_id: list of strings
       :param group: the group name of server
       :type group: string
       :param cloud: the cloud name
       :type cloud: string
       :param force: forces the delete process
       :type force: bool

       :return:
       """
        # TODO: delete by group. set default cloud

        # default cloud. fix this
        if cloud is None:
            cloud = "india"

        if cloud == "india":
            OpenStack = get_driver(Provider.OPENSTACK)
            try:
                # get cloud credential from yaml file
                confd = ConfigDict("cloudmesh.yaml")
                cloudcred = confd['cloudmesh']['clouds']['india']['credentials']
            except Exception, e:
                Console.error(e.message)
                return

            # set path to cacert and enable ssl connection
            libcloud.security.CA_CERTS_PATH = [Config.path_expand(cloudcred['OS_CACERT'])]
            libcloud.security.VERIFY_SSL_CERT = True

            auth_url = "%s/tokens/" % cloudcred['OS_AUTH_URL']

            driver = OpenStack(cloudcred['OS_USERNAME'],
                               cloudcred['OS_PASSWORD'],
                               ex_force_auth_url=auth_url,
                               ex_tenant_name=cloudcred['OS_TENANT_NAME'],
                               ex_force_auth_version='2.0_password',
                               ex_force_service_region='regionOne')

            # gets all the VMs
            nodes = driver.list_nodes()

            def __destroy_node(node):
                """
                    deletes a Virtual Machine

                :param node: node to be deleted
                :type node: Node
                :return:
                """
                try:
                    while True:
                        answer = ""
                        if not force:
                            answer = raw_input("Would you like to delete {:}? y/n".format(node.name))
                        if answer.lower() == 'y' or answer.lower() == 'yes' or force:
                            break
                        elif answer.lower() != 'n' and answer.lower() != 'no':
                            Console.ok("Invalid option")
                        else:
                            Console.ok("Operation aborted")
                            return

                    driver.destroy_node(node)
                    Console.ok("Virtual Machine {:} deleted".format(node.name))

                except Exception, e:
                    Console.error("Could not delete Virtual Machine {:}. {:}".format(node.name, e.message))

            def __deleteNode(*args):
                """
                    finds a node to be deleted

                    :param *args: [name], [prefix], [start], [end]
                    :param name: full name of the vm
                    :type name: string
                    :param prefix: fist part of the vm name. Example: full name: sample-[5-12], prefix: 'sample'
                    :type prefix: string
                    :param start: first virtual machine. Example: full name: sample-[5-12], start: '5'
                    :type start: string
                    :param end: last virtual machine. Example: full name: sample-[12-99], end: 99
                    :type end: string

                """
                if len(args) == 1:  # only one vm
                    name = args[0]
                    for i in nodes:
                        if i.name == name:
                            __destroy_node(i)
                            return
                    Console.error("Virtual Machine {:} not found".format(name))
                else:  # interval of vms like sample-[1-10]
                    prefix = args[0]
                    start = args[1].zfill(3)
                    end = args[2].zfill(3)

                    for i in range(int(start), int(end) + 1):
                        name = prefix + "-" + str(i).zfill(3)  # name of the vms to be deleted
                        flag = False
                        for j in nodes:
                            if name == j.name:
                                __destroy_node(j)
                                flag = True
                                break
                        if not flag:
                            Console.error("Virtual Machine {:} not found".format(name))

                            # name_or_id is a list of strings. A string is one of:
                            # sample_[100-9999]. Deletes vm starting at 100 until 9999
                            # sample. Deletes vm named sample

            for i in name_or_id:
                name = i.strip()
                if name[-1] == ']':  # vm name like sample-[1-10]
                    a = (name.split('[')[1]).split(']')[0].split('-')
                    prefix = name.split('-')[0]  # example: prefix is the sting 'sample' from sample-[10-12]
                    start = a[0]  # type: str
                    end = a[1]  # type: str
                    __deleteNode(prefix, start, end)
                else:  # vm name like sample-daniel
                    __deleteNode(name)

    @classmethod
    def ip_assign(cls, name_or_id, cloud):
        """

        :param name_or_id: name or id of the machine
        :type name: string
        :param cloud: cloud name
        :type cloud: string
        :return:
        """
        Console.ok('ip_assign {} {}'.format(name_or_id, cloud))
        raise NotImplemented("Not implemented yet")

    @classmethod
    def ip_show(cls, name_or_id, group, cloud, output_format, refresh):
        """
        TODO
        shows the ip of a vm

        :param name_or_id: name or id of the machine
        :type name_or_id: list?
        :param group: the group name of server
        :type group: string
        :param cloud: cloud name
        :type cloud: string
        :param output_format: output format
        :type output_format: string
        :param refresh:
        :type refresh: bool?
        :return:
        """
        Console.ok('ip_show {} {} {} {} {}'.format(name_or_id, group, cloud, output_format, refresh))
        raise NotImplemented("Not implemented yet")

    @classmethod
    def login(cls, name, user, ip, cloud, key, commands):
        """
        TODO
        :param name:
        :param user:
        :param ip:
        :param cloud:
        :param key:
        :param commands:
        :return:
        """
        Console.ok('login {} {} {} {} {} {}'.format(name, user, ip, cloud, key, commands))
        raise NotImplemented("Not implemented yet")

    @classmethod
    def list(cls, cloud, group, refresh, output_format, columns, detail):
        """
        TODO

        :param cloud: cloud name
        :param group: the group name of server
        :param refresh:
        :param output_format:
        :param columns:
        :param detail:
        :return:
        """

        Console.ok('list {} {} {} {} {} {}'.format(cloud, group, refresh, output_format, columns, detail))

        raise NotImplemented("Not implemented yet")

        # http://cloudmesh.github.io/introduction_to_cloud_computing/cloudmesh/shell/_vm-shell.html
