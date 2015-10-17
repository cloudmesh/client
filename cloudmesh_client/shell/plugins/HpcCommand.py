from cloudmesh_client.shell.command import command
from cloudmesh_client.cloud.hpc.hpc import Hpc


class HpcCommand:
    topics = {"cloud": "hpc"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init hpc command")

    @command
    def do_hpc(self, args, arguments):
        """
        ::

            Usage:
                hpc squeue [--format=FORMAT]

            Options:
               --format=FORMAT  the output format [default: json]

            Examples:
                cm hpc squeue

        """

        format = arguments['--format']
        if arguments["squeue"]:
            print(Hpc.read_squeue(format))

