class CloudmeshCloud(object):
    def __init__(self, filename=None):
        if filename is None:
            filename = "cloudmehs.yaml"
        self.config = ConfigDict(filename)

    def get(self, cloud):
        if cloud in config["cloudmesh"]["clouds"]:
            return config["cloudmesh"]["clouds"][cloud]
