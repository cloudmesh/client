from __future__ import print_function
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console


class QuotaCommand(object):

    topics = {"quota": "cloud"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command quota")


class cm_shell_quota:
    def activate_cm_shell_quota(self):
        self.register_command_topic('cloud', 'quota')

    @command
    def do_quota(self, args, arguments):
        """
        ::

            Usage:
                quota [CLOUD...] [--format=FORMAT]

            print quota limit on a current project/tenant

            Arguments:

              CLOUD          Cloud name

            Options:

               -v       verbose mode

        """
        # pprint(arguments)
        clouds = arguments["CLOUD"]
        output_format = arguments["--format"]
        Console.ok('quota {} {}'.format(clouds, output_format))
        pass


if __name__ == '__main__':
    command = cm_shell_quota()
    command.do_quota("list")
    command.do_quota("a=x")
    command.do_quota("x")
