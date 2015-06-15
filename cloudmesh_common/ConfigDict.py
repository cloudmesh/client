from __future__ import print_function

import ruamel.yaml
import os.path
import json
import re

class todo(object):
    @classmethod
    def implemet(cls):
        raise NotImplementedError("Please implement")

def path_expand(path):
    current_dir = "." + os.path.sep
    if path.startswith(current_dir):
        cwd = str(os.getcwd())
        path = path.replace(current_dir, cwd, 1)
    location = os.path.expandvars(os.path.expanduser(path))
    return location


def find_file(filename, load_order=None, verbose=False):
    if load_order is None:
        load_order = [".", "~/.cloudmesh"]
    for path in load_order:
        name = path_expand(path + os.path.sep + filename)
        if verbose:
            print ("try finding file", name)
        if os.path.isfile(name):
            if verbose:
                print ("Found File", name)
            return name
    return None

class ConfigDict(object):

    def __init__(self,
                 filename,
                 load_order=None,
                 verbose=False):
        """
        Creates a dictionary from a yaml configuration file
        while using the filename to load it in the specified load_order.
        The load order is an array of paths in which the file is searched.
        By default the load order is set to . and ~/.cloudmesh

        :param filename: the filename
        :type filename: string
        :param load_order: an array with path names in with the filename is looked for.
        :type load_order: list of strings
        :return: an instance of ConfigDict
        :rtype: ConfigDict
        """
        if load_order is None:
            self.load_order = [".", "~/.cloudmesh"]
        for path in self.load_order:
            name = path_expand(path + os.path.sep + filename)
            if verbose:
                    print ("try Loading ConfigDict", name)
            if os.path.isfile(name):
                if verbose:
                    print ("Loading ConfigDict", name)
                self.load(name)
                self.filename = name
                return

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

    def __setitem__(self, item, value):
        if "." in item:
            keys = item.split(".")
        else:
            element = self.data[item]

        element = self.data[keys[0]]
        for key in keys[1:]:
            element = element[key]
        element = value

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

    @property
    def json(self):
        """
        string of the json formated object

        :return: json string version
        """
        return (json.dumps(self.data, indent=4))

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

    print (d["meta"])
    print (d["meta.kind"])
    print (d["meta"]["kind"])

    # this does not yet work
    d.data["meta"]["test"] = 'Gregor'
    print (d)
    d.save()

    import os
    os.system("cat cmd3.yaml")

    print(d.json)
    print(d.filename)

if __name__ == "__main__":
    main()