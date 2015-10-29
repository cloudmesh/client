from cloudmesh_client.shell.console import Console
from cloudmesh_client.shell.command import command
from cloudmesh_client.cloud.hpc.hpc import Hpc
from cloudmesh_client.cloud.default import Default


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
                hpc run SCRIPT --p=PARTITION [--t=TIME] [--N=nodes] [--name=NAME] [--cluster=CLUSTER][--dir=DIR][--group=GROUP][--format=FORMAT]
                hpc kill job==NAME [--cluster=CLUSTER][--group=GROUP][--format=FORMAT]
                hpc kill all [--cluster=CLUSTER][--group=GROUP][--format=FORMAT]
                hpc status [--cluster=CLUSTER][--group=GROUP][--job=ID]
                hpc test --cluster=CLUSTER [--time=SECONDS]

            Options:
               --format=FORMAT  the output format [default: json]

            Examples:

                Special notes

                   if the group is specified only jobs from that group are
                   considered. Otherwise the default group is used. If he
                   group is set to None, all groups are used.

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

                cm hpc status job=ID
                    returns the status of the named job

                cm hpc test --cluster=CLUSTER --time=SECONDS
                    submits a simple test job to the named cluster and returns
                    if the job could be successfully executed. This is a
                    blocking call and may take a long time to complete
                    dependent on if the queuing system of that cluster is
                    busy. It will only use one node/core and print the message

                    #CLOUDMESH: Test ok

                    in that is being looked for to identify if the test is
                    successful. If time is used, the job is terminated
                    after the time is elapsed.
        """

        format = arguments['--format']
        cluster = arguments['--cluster']

        if arguments["queue"]:
            print(Hpc.queue(cluster, format=format))

        if arguments["info"]:
            print(Hpc.info(format))

        if arguments["kill"]:
            Console.error("Not yet implemented.")

        if arguments["status"]:
            job_id = arguments['--job']
            print(Hpc.queue(cluster, job=job_id))

        if arguments["run"]:
            # If cluster is not specified, get default
            if not cluster:
                cluster = Default.get("cluster") or "india" # TODO: need to clarify if throw error

            cmd = arguments['SCRIPT']
            arg_dict = {
                '-name' : arguments['--name'],
                '-p' : arguments['--p'],
                '-t' : arguments['--t'],
                '-N' : arguments['--N']
            }
            Console.ok(Hpc.run(cluster, cmd, **arg_dict))

        if arguments["test"]:
            time_secs = arguments['--time']
            if time_secs:
                time = '00:00:'+time_secs
            else:
                time = '00:00:10'  # give a  default time of 10 secs
            print(Hpc.test(cluster, time))


