from abc import ABCMeta, abstractmethod, abstractproperty


class CloudmeshProviderBase(object):
    __metaclass__ = ABCMeta

    def initialize(self, cloudname, cm_user=None):
        self.nodes = None
        self.flavors = None
        self.data = None
        self.images = None
        self.cloudname = cloudname
        self.user = cm_user
        self.credential = None
        self.driver = None

    @abstractproperty
    def mapping(self):
        pass

    @abstractmethod
    def list(self, kind, output=dict):
        """

        :param kind: exactly one of vm, flavor, image, default
        :param output:
        :return:
        """
        return {}

    @abstractmethod
    def boot(self, cloud, user, name, image, flavor, key, meta):
        return {}

    # define this
    @classmethod
    def flatten_image(cls, d):
        """
        flattens the data from a single image returned with libcloud.

        :param d: the data for that image
        :type d: dict
        :return: the flattened dict
        :rtype: dict
        """
        return d

    # define this
    @classmethod
    def flatten_vm(cls, d):
        """
        flattens the data from a single vm returned by libloud

        :param d: the data for that vm
        :type d: dict
        :return: the flattened dict
        :rtype: dict
        """
        return d

    # define this
    @classmethod
    def flatten_flavor(cls, d):
        """
        flattens the data from a single vm returned by libloud

        :param d: the data for that vm
        :type d: dict
        :return: the flattened dict
        :rtype: dict
        """
        return d

    @classmethod
    def flatten_vms(cls, d):
        return cls.flatten(cls.flatten_vm, d)

    @classmethod
    def flatten_images(cls, d):
        return cls.flatten(cls.flatten_image, d)

    @classmethod
    def flatten_flavor(cls, d):
        return cls.flatten(cls.flatten_flavor, d)

    @classmethod
    def flatten(cls, transform, d):
        result = {}
        for element in d:
            n = transform(d[element])
            result[element] = dict(n)
        return result
