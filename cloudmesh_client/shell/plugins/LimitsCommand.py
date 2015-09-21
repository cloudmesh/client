from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console


class LimitsCommand(object):

    topics = {"limits": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command limits")

    @command
    def do_limits(self, args, arguments):
        """
        ::

            Usage:
                limits [CLOUD...] [--format=FORMAT]

            Current usage data with limits on a selected project/tenant

            Arguments:

              CLOUD          Cloud name to see the usage

            Options:

               -v       verbose mode

        """
        # pprint(arguments)
        clouds = arguments["CLOUD"]
        output_format = arguments["--format"]
        Console.ok('limits {} {}'.format(clouds, output_format))
        pass


if __name__ == '__main__':
    command = cm_shell_limits()
    command.do_limits("list")
    command.do_limits("a=x")
    command.do_limits("x")
