from cmd3.console import Console
from cloudmesh_base.Shell import Shell
from os.path import expanduser

class Command_vm(object):

    @classmethod
    def start(cls, name, count, cloud, image, flavor, group):
        """
        starts a vm
        :param name: name of the virtual machine
        :type name: string
        :param count: give the number of servers to start
        :type count: integer
        :param cloud: give a cloud to work on, if not given, selected or default cloud will be used
        :type cloud: integer
        :param image: image name
        :type image: string
        :param flavor:flavor name. m1.medium, for example
        :type flavor: string
        :param group: the group name of server
        :type group: string
        :return:
        """

        Console.ok('start {} {} {} {} {} {}'.format(name, count, cloud, image, flavor, group))

        raise NotImplemented("Not implemented yet")


    @classmethod
    def delete(cls, name_or_id, group, cloud, force=False):
       """
       deletes a vm

       :param name_or_id: name or id of the vm to be deleted
       :type name_or_id: list
       :param group: the group name of server
       :type group: string
       :param cloud: the cloud name
       :type cloud: string
       :param force: forces the delete process
       :type force: bool

       :return:
       """

       Console.ok('delete: {} {} {} {}'.format(name_or_id, group, cloud, force))
       raise NotImplemented("Not implemented yet")

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
    def loging(cls, name, user, ip, cloud, key, commands):
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

    #http://cloudmesh.github.io/introduction_to_cloud_computing/cloudmesh/shell/_vm-shell.html
