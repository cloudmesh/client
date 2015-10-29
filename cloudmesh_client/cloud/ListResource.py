
from abc import ABCMeta, abstractmethod

#class ListResource(metaclass=ABCMeta):

class ListResource(object):

    __metaclass__ = ABCMeta

    @classmethod
    @abstractmethod
    def info(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def list(cls, **kwargs):
        raise NotImplementedError()


    @classmethod
    @abstractmethod
    def clear(cls, **kwargs):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def refresh(cls, **kwargs):
        raise NotImplementedError()

    '''
    # @abstractmethod
    @classmethod
    def get(cls, **kwargs):
        raise NotImplementedError()

    # @abstractmethod
    @classmethod
    def copy(cls, **kwargs):
        raise NotImplementedError()

    # @abstractmethod
    @classmethod
    def merge(cls, **kwargs):
        raise NotImplementedError()

    # @abstractmethod
    @classmethod
    def __delitem__(cls, a, b):
        raise NotImplementedError()

    # @abstractmethod
    @classmethod
    def __add__(cls, a, b):
        raise NotImplementedError()

    # @abstractmethod
    @classmethod
    def __iadd__(cls, a, b):
        raise NotImplementedError()

    # @abstractmethod
    @classmethod
    def __isub__(cls, a, b):
        raise NotImplementedError()

    # @abstractmethod
    @classmethod
    def __concat__(cls, a, b):
        raise NotImplementedError()

    # @abstractmethod
    @classmethod
    def __contains__(cls, a, b):
        raise NotImplementedError()

    # @abstractmethod
    @classmethod
    def __sub__(cls, a, b):
        raise NotImplementedError()

    # @abstractmethod
    @classmethod
    def __getitem__(cls, item):
        raise NotImplementedError()

    # @abstractmethod
    @classmethod
    def __setitem__(cls, item):
        raise NotImplementedError()

    # @abstractmethod
    @classmethod
    def count(self):
        raise NotImplementedError()
    '''
