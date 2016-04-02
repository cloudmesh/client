from .general.attributes import Attributes as GeneralAttributes
from .openstack.attributes import Attributes as OpenstackAttributes
from .libcloud.attributes import Attributes as LibcloudAttributes


class Attributes(object):
    @classmethod
    def get(cls, kind, provider='general'):
        if provider == "general":
            return GeneralAttributes.get(kind)
        elif provider == "openstack":
            return OpenstackAttributes.get(kind)
        elif provider == "libcloud":
            return LibcloudAttributes.get(kind)
        else:
            ValueError("provider {} not found".format(provider))
            return None, None
