from __future__ import print_function
# from cloudmesh_client.shell.console import Console

from cloudmesh_client.db import CloudmeshDatabase

from cloudmesh_client.common.todo import TODO

from cloudmesh_client.cloud.ListResource import ListResource



class Reservation(ListResource):

    cm = CloudmeshDatabase()
    
    def info(cls, user=None, project=None):
        """
        prints if the user has access to the reservation an on which host.

        :param user:
        :param project:
        :return:
        """
        TODO.implement()

    def add_from_file(cls, filename):
        """

        :param filename:
        :return:
        """
        TODO.implement()
    
    @classmethod
    def add(cls,
            name,
            start,
            end,
            user=None,
            project=None,
            hosts=None,
            description=None,
            cloud=None):
        """

        :param name: Name of reservation
        :param start: Start time of reservation
        :param end: End time of reservation
        :param user: Reserved by this user
        :param project: Reservation project
        :param hosts: Reserved hosts
        :param description: Description
        :param cloud: Cloud into which reservation done
        :return:
        """
        obj_d = cls.cm.db_obj_dict("reservation",
                                    name=name,
                                    hosts=hosts,
                                    start=start,
                                    end=end,
                                    description=description,
                                    cloud=cloud,
                                    user=user,
                                    project=project)
        cls.cm.add_obj(obj_d)
        cls.cm.save()

    @classmethod
    def delete(cls,
               name=None,
               start=None,
               end=None,
               user=None,
               project=None,
               hosts=None):
        """

        :param name: Name of reservation
        :param start: Start time of reservation
        :param end: End time of reservation
        :param user: Reserved by this user
        :param project: Reservation project
        :param hosts: Hosts reserved
        :return:
        """
     
        args = {}

        if name is not None:
            args['name'] = name
        if start is not None:
            args['start_time'] = start
        if end is not None:
            args['end_time'] = end
        if user is not None:
            args['user'] = user
        if project is not None:
            args['project'] = project
        if hosts is not None:
            args['hosts'] = hosts

        # TODO: Improve this logic
        result = cls.cm.find("RESERVATION", output="object", **args).first()
        while result is not None:
            cls.cm.delete(result)
            result = cls.cm.find("RESERVATION", output="object", **args).first()

    @classmethod
    def delete_from_file(cls, filename):
        """

        :param filename:
        :return:
        """
        TODO.implement()
    
    @classmethod
    def suspend(cls, names=None):
        TODO.implement()

    @classmethod
    def clear(cls, names=None):
        TODO.implement()

    @classmethod
    def refresh(cls, names=None):
        TODO.implement()

    @classmethod
    def resume(cls, names=None):
        TODO.implement()

    @classmethod
    def list(cls,
             name=None,
             start=None,
             end=None,
             user=None,
             project=None,
             hosts=None):

        """

        :param name: Name of reservation
        :param start: Start time of reservation
        :param end: End time of reservation
        :param user: Reserved by this user
        :param project: Reservation project
        :param hosts: Hosts reserved
        :return:
        """
       
        args = {}

        if name is not None:
            args['name'] = name
        if start is not None:
            args['start_time'] = start
        if end is not None:
            args['end_time'] = end
        if user is not None:
            args['user'] = user
        if project is not None:
            args['project'] = project
        if hosts is not None:
            args['hosts'] = hosts

        # print(args)
        result = cls.cm.find("RESERVATION", **args)
        # print("RESULT:- {}".format(result))
        return result

    @classmethod
    def update(cls,
               name,
               start,
               end,
               user=None,
               project=None,
               hosts=None,
               description=None,
               cloud=None):

        args = {}

        if name is not None:
            args['name'] = name
        if start is not None:
            args['start_time'] = start
        if end is not None:
            args['end_time'] = end
        if user is not None:
            args['user'] = user
        if project is not None:
            args['project'] = project
        if hosts is not None:
            args['hosts'] = hosts
        if description is not None:
            args['description'] = description
        if cloud is not None:
            args['cloud'] = cloud

        cls.cm.update("RESERVATION", **args)
