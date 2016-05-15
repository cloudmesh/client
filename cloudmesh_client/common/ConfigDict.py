from __future__ import print_function

import json
import os.path
from collections import OrderedDict
import sys
import yaml
import shutil

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.BaseConfigDict import BaseConfigDict
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.common.util import path_expand
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.util import backup_name


def custom_print(data_structure, indent, attribute_indent=4):
    for key, value in data_structure.items():
        print("\n%s%s:" % (' ' * attribute_indent * indent, str(key)), end=' ')
        if isinstance(value, OrderedDict):
            custom_print(value, indent + 1)
        elif isinstance(value, dict):
            custom_print(value, indent + 1)
        else:
            print("%s" % (str(value)), end=' ')


def ordered_dump(data, stream=None, Dumper=yaml.Dumper, **kwds):
    """
    writes the dict into an ordered yaml.
    :param data: The ordered dict
    :param stream: the stream
    :param Dumper: the dumper such as yaml.SafeDumper
    """

    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


# noinspection PyPep8Naming
def dprint(OD, mode='dict', s="", indent=' ' * 4, level=0):
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def fstr(s):
        return s if is_number(s) else '"%s"' % s

    if mode != 'dict':
        kv_tpl = '("%s", %s)'
        ST = 'OrderedDict([\n'
        END = '])'
    else:
        kv_tpl = '"%s": %s'
        ST = '{\n'
        END = '}'
    for i, k in enumerate(OD.keys()):
        if type(OD[k]) in [dict, OrderedDict]:
            level += 1
            s += (level - 1) * indent + kv_tpl % (k, ST + dprint(OD[k], mode=mode,
                                                                 indent=indent, level=level) + (
                                                      level - 1) * indent + END)
            level -= 1
        else:
            s += level * indent + kv_tpl % (k, fstr(OD[k]))
        if i != len(OD) - 1:
            s += ","
        s += "\n"
    return s


class Config(object):
    @classmethod
    def check_file_for_tabs(cls, filename, verbose=True):
        """identifies if the file contains tabs and returns True if it
        does. It also prints the location of the lines and columns. If
        verbose is set to False, the location is not printed.
        :param filename: the filename
        :type filename: str
        :rtype: True if there are tabs in the file
        """
        filename = path_expand(filename)
        file_contains_tabs = False
        with file(filename) as f:
            lines = f.read().split("\n")

        line_no = 1
        for line in lines:
            if "\t" in line:
                file_contains_tabs = True
                location = [
                    i for i in range(len(line)) if line.startswith('\t', i)]
                if verbose:
                    print("Tab found in line", line_no, "and column(s)",
                          location)
            line_no += 1
        return file_contains_tabs

    @classmethod
    def path_expand(cls, path):
        """
        expands the path while replacing environment variables, ./, and ~/
        :param path: the path to be expanded
        :type path: string
        :return:the new path
        :rtype: string
        """
        current_dir = "." + os.path.sep
        if path.startswith(current_dir):
            cwd = str(os.getcwd())
            path = path.replace(current_dir, cwd, 1)
        location = os.path.expandvars(os.path.expanduser(path))
        return location

    @classmethod
    def find_file(cls, filename, load_order=None, verbose=False):
        """
        find the specified file in the list of directories that are given in the
        array load_order
        :param filename: the file name
        :type filename: str
        :param load_order: an array with path names in with the filename is looked for.
        :type load_order: list of str
        :param verbose:
        :type verbose: bool
        :return: file name if successful
        :rtype: string if the file exists or None otherwise
        """
        if load_order is None:
            load_order = [".", os.path.join("~", ".cloudmesh")]
        for path in load_order:
            name = Config.path_expand(path + os.path.sep + filename)
            if verbose:
                print("try finding file", name)
            if os.path.isfile(name):
                if verbose:
                    print("Found File", name)
                return name
        return None


class ConfigDict(object):
    versions = ['4.1']

    def __init__(self,
                 filename,
                 load_order=None,
                 verbose=False,
                 etc=False):
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

        self.data = None
        if etc:
            import cloudmesh_client.etc
            load_order = [os.path.dirname(cloudmesh_client.etc.__file__)]

        if load_order is None:
            self.load_order = [".", os.path.join("~", ".cloudmesh")]
        else:
            self.load_order = load_order

        for path in self.load_order:
            name = Config.path_expand(os.path.join(path, filename))
            if verbose:
                print("try Loading ConfigDict", name)
            if os.path.isfile(name):
                if verbose:
                    print("Loading ConfigDict", name)
                self.load(name)
                self.filename = name
                return

        # Create default yaml file
        raise ValueError("Could not find file {:} in {:}".format(filename, self.load_order))

    def load(self, filename):
        """
        loads the configuration from the yaml filename
        :param filename:
        :type filename: string
        :return:
        """
        self.data = BaseConfigDict(filename=Config.path_expand(filename))
        try:
            version = str(self.data["meta"]["version"])
            if version not in self.versions:
                Console.error("The yaml file version must be {}".format(', '.join(self.versions)))
                sys.exit(1)
        except Exception as e:
            Console.error("Your yaml file ~/.cloudmesh/cloudmesh.yaml is not up to date.", traceflag=False)
            Console.error(e.message, traceflag=False)
            sys.exit(1)
            # return self.data

    def write(self, filename=None, output="dict", attribute_indent=4):
        """
        This method writes the dict into various outout formats. This includes a dict,
        json, and yaml
        :param filename: the file in which the dict is written
        :param output: is a string that is either "dict", "json", "yaml"
        :param attribute_indent: character indentation of nested attributes in
        """
        if filename is not None:
            location = path_expand(filename)
        else:
            location = self['meta']['location']

            # with open('data.yml', 'w') as outfile:
            #    outfile.write( yaml.dump(data, default_flow_style=True) )

        # Make a backup
        self.make_a_copy(location)

        f = os.open(location, os.O_CREAT | os.O_TRUNC |
                    os.O_WRONLY, stat.S_IRUSR | stat.S_IWUSR)
        if output == "json":
            os.write(f, self.json())
        elif output in ['yml', 'yaml']:
            # d = dict(self)
            # os.write(f, yaml.dump(d, default_flow_style=False))
            os.write(f, ordered_dump(OrderedDict(self),
                                     Dumper=yaml.SafeDumper,
                                     default_flow_style=False,
                                     indent=attribute_indent))
        elif output == "print":
            os.write(f, custom_print(self, attribute_indent))
        else:
            os.write(f, self.dump())
        os.close(f)

    def make_a_copy(self, location=None):
        """
        Creates a backup of the file specified in the location. The backup
        filename  appends a .bak.NO where number is a number that is not yet
        used in the backup directory.
        TODO: This function should be moved to another file maybe XShell
        :param location: the location of the file to be backed up
        """
        import shutil
        dest = backup_name(location)
        shutil.copyfile(location, dest)

    def save(self, filename=None):
        """
        saves the configuration in the given filename,
        if it is none the filename at load time is used.
        :param filename: the file name
        :type filename: string
        :return:
        """
        content = self.data.yaml()
        with open(Config.path_expand(self.filename), 'w') as f:
            f.write(content)

    def __setitem__(self, item, value):
        """
        sets an item with the given value while using . formatted keys
        set('a.b.c", value)
        :param item:
        :type item:
        :param value:
        :type value:
        :return:
        """
        keys = None
        if "." in item:
            keys = item.split(".")
        else:
            element = self.data[item]

        element = self.data[keys[0]]
        for key in keys[1:]:
            element = element[key]
        element = value

    def __getitem__(self, item):
        """
        gets an item form the dict. The key is . separated
        use it as follows get("a.b.c")
        :param item:
        :type item:
        :return:
        """
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
        returns the dict in yaml format
        :return: returns the yaml output of the dict
        :rtype: string
        """
        return self.data.yaml()

    @property
    def yaml(self):
        """
        returns the dict in yaml format
        :return: returns the yaml output of the dict
        :rtype: string:
        """
        return self.data.yaml()

    def info(self):
        """
        prints out the dict type and its content
        """
        print(type(self.data))
        print(self.data)

    @property
    def json(self, start=None):
        """
        :param start: start key in dot notation
        returns the dict in json format
        :return: json string version
        :rtype: string
        """
        if start is not None:
            data = self.data[start]
        return json.dumps(self.data, indent=4)

    @classmethod
    def check(cls, filename):
        """
        checks the filename if it is syntactically correct and does not include tabs
        :param filename:
        :type filename: string
        :return:
        """
        TODO.implement()

    @classmethod
    def getUser(cls, cloud):
        try:
            config = d = ConfigDict("cloudmesh.yaml")

            d = ConfigDict("cloudmesh.yaml")

            #
            # bug: cloud is none when adding a group
            #

            config = d["cloudmesh"]["clouds"][cloud]
            credentials = config["credentials"]
            cloud_type = config["cm_type"]

            if cloud_type == "openstack":
                return credentials["OS_USERNAME"]
            else:
                raise ValueError("getUser for this cloud type not yet "
                                 "supported: {}".format(cloud))
        except Exception as ex:
            Console.error("problem getting user")


# noinspection PyPep8Naming
def Username():
    d = ConfigDict("cloudmesh.yaml")

    if "user" not in d["cloudmesh"]["profile"]:
        raise RuntimeError("Profile username is not set in yaml file.")

    user = d["cloudmesh"]["profile"]["user"]
    return user


def main():
    d = ConfigDict("cloudmesh.yaml")
    print(d, end='')
    d.info()

    print(d["meta"])
    print(d["meta.kind"])
    print(d["meta"]["kind"])

    # this does not yet work
    d.data["cloudmesh"]["profile"]["firstname"] = 'ABC'
    print(d)
    d.save()

    import os

    os.system("cat cmd3.yaml")

    print(d.json)
    print(d.filename)
    print("YAML")
    print(d.yaml)


if __name__ == "__main__":
    main()
