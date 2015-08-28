#! /usr/bin/env python

from cmd import Cmd
from mixin import MixIn, makeWithMixins, makeWithMixinsFromString
import plugins
import sys
import os
import pkgutil
import inspect
from cloudmesh_base.util import path_expand

__all__ = []


def get_addons(path):
    path = path_expand(path)
    print "-> Searching in path", path

    for loader, name, is_pkg in pkgutil.walk_packages(path):
        print "-> Loading add on:", name
        module = loader.find_module(name).load_module(name)

        for name, value in inspect.getmembers(module):
            if name.startswith('__'):
                continue
            if name in __all__:
                continue
            globals()[name] = value
            __all__.append(name)


def plugins():
    return __all__


def get_class(modname, classname):
    ''' Returns a class of "classname" from module "modname". '''
    module = __import__(modname)
    classobj = getattr(module, classname)
    return classobj


def get_plugins(names=None, verbose=False):
    class_list = []
    if names is None:
        names = plugins()
    for classname in plugins():
        try:
            class_list.append(get_class("plugins", classname))
        except:
            # ignore wrong class load
            if verbose:
                print "WARNING: ignoring class", classname
            pass
    return class_list


class Shell(Cmd):
    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print "Hello, %s" % name

    def do_quit(self, args):
        """Quits the program."""
        sys.exit()

    do_q = do_quit
    do_EOF = do_quit


if __name__ == '__main__':
    get_addons("plugins")
    plugins = get_plugins()
    print plugins

    # import cloudmesh_job
    # p = os.path.dirname(cloudmesh_job.__file__)
    # print p
    # get_addons(p)
    SuperShell = makeWithMixins(Shell, plugins)
    shell = SuperShell()
    shell.prompt = '> '
    shell.cmdloop('Cloudmesh Shell...')
