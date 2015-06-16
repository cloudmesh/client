from __future__ import print_function
from cmd3.console import Console


class command_cloud(object):

    @classmethod
    def list(cls, filename):
        Console.ok("list")
        print(filename)

    @classmethod
    def  read_rc_file(cls, host, user, filename):
        Console.ok("register")
        print(user, host, filename)

    @classmethod
    def check_yaml_for_completeness(cls, filename):
        Console.ok("check")
        print(filename)

    @classmethod
    def register(cls, filename):
        Console.ok("register")
        print(filename)

    @classmethod
    def test(cls, filename):
        Console.ok("register")
        print(filename)

    @classmethod
    def fill_out_form(cls, filename):
        Console.ok("form")
        print(filename)
