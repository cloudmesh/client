from __future__ import print_function
from ..command_decorator import command


class BarCommand(object):

    topics = {"bar": "example"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init Bar")

    @command
    def do_bar(self, arg, arguments):
        """
        ::

          Usage:
                bar -f FILE
                bar FILE
                bar list

          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

        """
        print(arguments)
