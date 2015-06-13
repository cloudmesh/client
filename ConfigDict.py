from __future__ import print_function

import ruamel.yaml
import os.path

from cloudmesh_base.util import path_expand

class todo(object):
    @classmethod
    def implemet(cls):
        raise NotImplementedError("Please implement")

class ConfigDict(object):

    def __init__(self, filename, load_order=None):
        """
        not yet completed

        :param filename:
        :param load_order:
        :return:
        """
        if load_order is None:
            self.load_order = [".", "~/.cloudmesh"]
        for path in self.load_order:
            name = path_expand("{:}/{:}".format(path, filename))
            if os.path.isfile(name):
                self.load(name)
                self.filename = name

    def load(self, filename):
        """loads the filename"""
        with open(path_expand(filename),'r') as f:
            content = f.read()
        self.data = ruamel.yaml.load(content, ruamel.yaml.RoundTripLoader)

    def save(self, filename=None):
        """
        saves the configuration in the given filename, if it is none the filename at load time is used.

        :param filename:
        :return:
        """
        content = ruamel.yaml.dump(self.data, Dumper=ruamel.yaml.RoundTripDumper)
        with open(path_expand(self.filename),'w') as f:
            f.write(content)

    def __getitem__(self, item):
        if "." in item:
            keys = item.split(".")
        else:
            return self.data[item]
        element = self.data[keys[0]]
        for key in keys[1:]:
            element = element[key]
        return element

    def __str__(self):
        """

        :return:
        """
        return (ruamel.yaml.dump(self.data, Dumper=ruamel.yaml.RoundTripDumper))

    def info(self):
        """

        :return:
        """
        print (type(self.data))
        print (self.data)

    @classmethod
    def check(cls, filename):
        """
        checks the filename if it is syntactically corrrect and does not include tabs

        :param filename:
        :return:
        """
        todo.implement()

def main():
    d = ConfigDict("cmd3.yaml")
    print (d, end='')
    d.info()
    d.save()

    print (d["meta"])
    print (d["meta.kind"])
    print (d["meta"]["kind"])

if __name__ == "__main__":
    main()