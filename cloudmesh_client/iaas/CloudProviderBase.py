class CloudProviderBase (object):

    def boot(self, cloud, names, goup, label, image, flavor, key):
        return {}

    def delete(self, names):
        pass

    def images(self, clouds, query):
        return {}

    def flavors(self, clouds, query):
        return {}

    def vms(self, clouds, query):
        return {}

    def update(self, clouds, kind):
        pass
