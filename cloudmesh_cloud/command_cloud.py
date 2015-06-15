from __future__ import print_function
from cmd3.console import Console


class command_cloud(object):
    @classmethod
    def list(cls):
        Console.ok("list")

    @classmethod
    def set(cls, key, value):
        Console.ok("Set")
        print(key, value)

    @classmethod
    def get(cls, key):
        Console.ok("Get")
        print(key)
