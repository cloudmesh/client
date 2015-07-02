from cmd3.console import Console
from cloudmesh_base.Shell import Shell
from os.path import expanduser

class Command_vm(object):

    @classmethod
    def start(cls, name, count, cloud, image, flavor, group):
        """
        starts a vm

        :return:
        """
        Console.ok('start {} {} {} {} {} {}'.format(name, count, cloud, image, flavor, group))

        raise NotImplemented("Not implemented yet")


    @classmethod
    def delete(cls, name_or_id, group, cloud, force):
        """
        deletes a vm
        :return:
        """
        Console.ok('delete: {} {} {} {}'.format(name_or_id, group, cloud, force))
        raise NotImplemented("Not implemented yet")

    @classmethod
    def ip_assign(cls, name_or_id, cloud):

        Console.ok('ip_assign {} {}'.format(name_or_id, cloud))
        raise NotImplemented("Not implemented yet")

    @classmethod
    def ip_show(cls, name_or_id, group, cloud, output_format, refresh):

        Console.ok('ip_show {} {} {} {} {}'.format(name_or_id, group, cloud, output_format, refresh))
        raise NotImplemented("Not implemented yet")

    @classmethod
    def loging(cls, name, user, ip, cloud, key, commands):

        Console.ok('login {} {} {} {} {} {}'.format(name, user, ip, cloud, key, commands))
        raise NotImplemented("Not implemented yet")

    @classmethod
    def list(cls, cloud, group, refresh, output_format, columns, detail):

        Console.ok('list {} {} {} {} {} {}'.format(cloud, group, refresh, output_format, columns, detail))

        raise NotImplemented("Not implemented yet")

    #http://cloudmesh.github.io/introduction_to_cloud_computing/cloudmesh/shell/_vm-shell.html
