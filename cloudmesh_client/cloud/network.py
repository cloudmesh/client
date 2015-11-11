from __future__ import print_function


class Network(object):
    @classmethod
    def fixed_ip_get(cls, cloud, fixed_ip):
        pass

    @classmethod
    def fixed_ip_reserve(cls, cloud, fixed_ip):
        pass

    @classmethod
    def fixed_ip_unreserve(cls, cloud, fixed_ip):
        pass

    @classmethod
    def floating_ip_associate(cls, cloud, server, floating_ip):
        pass

    @classmethod
    def floating_ip_disassociate(cls, cloud, server, floating_ip):
        pass

    @classmethod
    def floating_ip_create(cls, cloud, floating_pool=None):
        pass

    @classmethod
    def floating_ip_delete(cls, cloud, floating_ip):
        pass

    @classmethod
    def floating_ip_list(cls, cloud):
        pass

    @classmethod
    def floating_ip_pool_list(cls, cloud):
        pass
