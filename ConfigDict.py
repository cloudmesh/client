from __future__ import print_function

import ruamel.yaml

class ConfigDict(object):


    def load(filename):

data = ruamel.yaml.load(inp, ruamel.yaml.RoundTripLoader)

print(ruamel.yaml.dump(data, Dumper=ruamel.yaml.RoundTripDumper), end='')
