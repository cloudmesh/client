from __future__ import print_function
# from cloudmesh_client.shell.console import Console

from cloudmesh_client.common.todo import TODO

class Reservation(object):

    '''
    TODO: implement functions that support
        see ReservationCommand
    '''

    def info(self, user=None, project=None):
        '''
        prints if the user has access to the reservation an on which host.

        :param user:
        :param project:
        :return:
        '''
        TODO('implement')

    def add_from_file(self, filename):
        '''

        :param filename:
        :return:
        '''
        TODO("implement")

    def add(self,
            names, # list of names can be a parameter
            start,
            end,
            user=None,
            project=None,
            hosts=None,
            description=None):
        TODO("implement")

    def delete(self,
            names=None, # list of names can be a parameter
            start=None,
            end=None,
            user=None,
            project=None,
            hosts=None):
        TODO("implement")

    def delete(self, parameters_tbd):
        TODO("implement")

    def delete_from_file(self, filename):
        '''

        :param filename:
        :return:
        '''
        TODO("implement")

    def suspend(self, names=None):
        TODO("implement")

    def resume(self, names=None):
        TODO("implement")

    def list(self,
            names=None, # list of names can be a parameter
            start=None,
            end=None,
            user=None,
            project=None,
            hosts=None):
        TODO("implement")

    def update(self,
               names=None, # list of names can be a parameter
               start=None,
               end=None,
               description=None):
        TODO("implement")



