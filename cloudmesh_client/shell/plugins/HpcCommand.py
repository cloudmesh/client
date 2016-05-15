from cloudmesh_client.cloud.experiment import Experiment
from cloudmesh_client.cloud.hpc.BatchProvider import BatchProvider
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.util import yn_choice
from cloudmesh_client.default import Default
from cloudmesh_client.shell.command import PluginCommand, HPCPluginCommand, \
    CometPluginCommand
from cloudmesh_client.shell.command import command
from cloudmesh_client.shell.console import Console


# noinspection PyBroadException
class HpcCommand(PluginCommand, HPCPluginCommand, CometPluginCommand):
    topics = {"hpc": "system"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init hpc command")

    # noinspection PyUnusedLocal
    @command
    def do_hpc(self, args, arguments):
        # noinspection PyPep8
        """
                ::

                    Usage:
                        hpc queue [--job=NAME][--cluster=CLUSTER][--format=FORMAT]
                        hpc info [--cluster=CLUSTER][--format=FORMAT]
                        hpc run list [ID] [--cluster=CLUSTER]
                        hpc run output [ID] [--cluster=CLUSTER]
                        hpc run rm [ID] [--cluster=CLUSTER]
                        hpc run SCRIPT [--queue=QUEUE] [--t=TIME] [--N=nodes] [--name=NAME] [--cluster=CLUSTER][--dir=DIR][--group=GROUP][--format=FORMAT]
                        hpc delete --job=NAME [--cluster=CLUSTER][--group=GROUP]
                        hpc delete all [--cluster=CLUSTER][--group=GROUP][--format=FORMAT]
                        hpc status [--job=name] [--cluster=CLUSTER] [--group=GROUP]
                        hpc test --cluster=CLUSTER [--time=SECONDS]

                    Options:
                       --format=FORMAT  the output format [default: table]

                    Examples:

                        Special notes

                           if the group is specified only jobs from that group are
                           considered. Otherwise the default group is used. If the
                           group is set to None, all groups are used.

                        cm hpc queue
                            lists the details of the queues of the hpc cluster

                        cm hpc queue --job=NAME
                            lists the details of the job in the queue of the hpc cluster

                        cm hpc info
                            lists the details of the hpc cluster

                        cm hpc run SCRIPT
                            submits the script to the cluster. The script will be
                            copied prior to execution into the home directory on the
                            remote machine. If a DIR is specified it will be copied
                            into that dir.
                            The name of the script is either specified in the script
                            itself, or if not the default naming scheme of
                            cloudmesh is used using the same index incremented name
                            as in vms fro clouds: cloudmes husername-index

                        cm hpc delete all
                            kills all jobs on the default hpc group

                        cm hpc delete --job=NAME
                            kills a job with a given name or job id

                        cm default cluster=NAME
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

                    Examples:
                        cm hpc queue
                        cm hpc queue --job=xxx
                        cm hpc info
                        cm hpc delete --job=6
                        cm hpc delete all
                        cm hpc status
                        cm hpc status --job=6
                        cm hpc run uname
                        cm hpc run ~/test.sh --cluster=india
                """

        format = arguments['--format']
        cluster = arguments['--cluster'] or Default.cluster
        arguments["CLUSTER"] = cluster

        if cluster is None:
            Console.error("Default cluster doesn't exist")
            return

        batch = BatchProvider(cluster)

        if arguments["queue"]:
            name = arguments['--job']
            result = batch.queue(cluster, format=format, job=name)
            Console.msg(result)

        elif arguments["info"]:
            Console.msg(batch.info(cluster, format))

        elif arguments['delete'] and arguments['all']:
            group = arguments['--group'] or Default.get(name='group')
            if group is None:
                Console.error('set default group using: default group=<value> --cloud=general')
                return
            Console.ok(batch.delete(cluster, None, group))

        elif arguments["delete"]:
            job = arguments['--job']
            Console.ok(batch.delete(cluster, job))

        elif arguments["status"]:
            name = arguments['--job']
            result = batch.queue(cluster, format=format, job=name)
            Console.msg(result)

        elif arguments["test"]:
            time_secs = arguments['--time']
            if time_secs:
                time = '00:00:' + time_secs
            else:
                time = '00:00:10'  # give a  default time of 10 secs
            print(batch.test(cluster, time))

        elif arguments["run"] and arguments["list"]:
            # hpc experiment list [--cluster=CLUSTER]
            if arguments["ID"]:
                print("# List of experiment {ID} on Cluster {CLUSTER}".format(**arguments))
                result = Experiment.list(cluster, id=arguments["ID"], format="list")
                if result is not None:
                    print("\n".join(result))
                else:
                    Console.error("Could not find experiment {ID} on {CLUSTER}".format(**arguments))
            else:
                print("# List of experiments on Cluster {CLUSTER}".format(**arguments))
                ids = Experiment.list(cluster, id=None, format="list")
                if ids is not None:
                    print(", ".join([str(i) for i in ids]))
                else:
                    Console.error("Could not find experiment {ID} on {CLUSTER}".format(**arguments))

        elif arguments["run"] and arguments["rm"]:
            # hpc experiment list [--cluster=CLUSTER]
            if arguments["ID"]:

                force = yn_choice("Would you like to delete experiment {ID} on Cluster {CLUSTER}".format(**arguments))
                if force:
                    try:
                        result = Experiment.rm(cluster, id=arguments["ID"])
                        Console.ok("Experiment {ID} on Cluster {CLUSTER} deleted".format(**arguments))
                    except:
                        Console.error("Could not delete experiment {ID} on {CLUSTER}".format(**arguments))
            else:
                result = Experiment.list(cluster, id=None, format="list")
                if result is not None:
                    arguments['experiments'] = ", ".join([str(i) for i in result])
                else:
                    Console.error("Could not find experiment {ID} on {CLUSTER}".format(**arguments))
                    return ""

                force = yn_choice("Would you like to delete the experiments {experiments} on Cluster {CLUSTER}".format(
                    **arguments))
                if force:
                    try:
                        result = Experiment.rm(cluster, id=None)
                        Console.ok("Experiments {experiments} on Cluster {CLUSTER} deleted".format(**arguments))
                    except:
                        Console.error("Could delete the experiments on {CLUSTER}".format(**arguments))
                return ""

        elif arguments["run"] and arguments["output"]:
            # hpc experiment list [--cluster=CLUSTER]
            if arguments["ID"]:
                print("# List of experiment {ID} on Cluster {CLUSTER}".format(**arguments))
                result = Experiment.output(cluster, id=arguments["ID"], format="list")
                if result is not None:
                    print("\n".join(result))
                else:
                    Console.error("Could not find experiment {ID} on {CLUSTER}".format(**arguments))
            else:
                print("# List of experiments on Cluster {CLUSTER}".format(**arguments))
                ids = Experiment.output(cluster, id=None, format="list")
                if ids is not None:
                    print(", ".join([str(i) for i in ids]))
                else:
                    Console.error("Could not find experiment {ID} on {CLUSTER}".format(**arguments))

        elif arguments["run"]:
            queue = arguments['--queue'] or Default.get(name='queue')
            # if not queue:
            #    Console.error('set default queue using: default queue=<value>')
            #    return
            group = arguments['--group'] or Default.get(name='group')
            if group is None:
                Console.error('set default group using: default group=<value> --cloud=general')
                return

            script = arguments['SCRIPT']
            arg_dict = {
                '-name': arguments['--name'],
                '-p': queue,
                '-t': arguments['--t'],
                '-N': arguments['--N']
            }

            result = batch.run(cluster, group, script, **arg_dict)
            if isinstance(result, dict):
                print(Printer.attribute(result))
                Console.ok("Experiment {count}: Started batch job {job_id} on {cluster}".format(**result))
            else:
                Console.error(result)

        return ""
