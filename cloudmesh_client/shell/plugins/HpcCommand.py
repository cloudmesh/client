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
                hpc sinfo [--format=FORMAT]

            Options:
               --format=FORMAT  the output format [default: json]

            Examples:
                cm hpc squeue
                cm hpc sinfo

        """

        format = arguments['--format']
        if arguments["squeue"]:
            print(Hpc.read_squeue(format))
        if arguments["sinfo"]:
            print(Hpc.read_sinfo(format))

