from cloudmesh_client.shell.command import command
from cloudmesh_client.cloud.hpc.hpc import Hpc


class HpcCommand:
    topics = {"hpc": "hpc"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init hpc command")

    @command
    def do_hpc(self, args, arguments):
        """
        ::

            Usage:
                hpc queue [--name=NAME][--cluster=CLUSTER][--format=FORMAT]
                hpc info [--cluster=CLUSTER][--format=FORMAT]
                hpc run SCRIPT [--cluster=CLUSTER][--dir=DIR][--format=FORMAT]
                hpc kill job==NAME [--cluster=CLUSTER][--format=FORMAT]
                hpc kill all [--cluster=CLUSTER][--format=FORMAT]
                hpc status [--cluster=CLUSTER][job=NAME]

            Options:
               --format=FORMAT  the output format [default: json]

            Examples:
                cm hpc queue
                    lists the details of the queues of the default hpc cluster

                cm hpc queue --name=NAME
                    lists the details of the named queue of the default hpc
                    cluster

                cm hpc info
                    lists the details of the hpc cluster
                    hpc cluster

                cm hpc run SCRIPT
                    submits the script to the cluster. THe script will be
                    copied prior to execution into the home directory on the
                    remote machine. If a DIR is specified it will be copied
                    into that dir.
                    The name of the script is either specified in the script
                    itself, or if not the default nameing scheme of
                    cloudmesh is used using the same index incremented name
                    as in vms fro clouds: cloudmeshusername-index

                cm hpc kill all
                    kills all jobs on the default hpc cluster

                cm hpc kill all -cluster=all
                    kills all jobs on all clusters

                cm kill job=NAME
                    kills a job with a given name

                cm hpc default cluster=NAME
                    sets the default hpc cluster

                cm hpc status
                    returns the status of all jobs

                cm hpc status job=NAME
                    returns the status of the named job

        """

        format = arguments['--format']
        if arguments["queue"]:
            print(Hpc.read_squeue(format))
        if arguments["info"]:
            print(Hpc.read_sinfo(format))

