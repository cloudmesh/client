import json
from datetime import datetime
import textwrap

from cloudmesh_base.Shell import Shell
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.common.TableParser import TableParser
from cloudmesh_client.common.ConfigDict import Config, ConfigDict
from cloudmesh_client.cloud.hpc.BatchProviderBase import BatchProviderBase
from pprint import pprint


class BatchProviderSLURM(BatchProviderBase):
    kind = "slurm"

    @classmethod
    def queue(cls, cluster, format='json', job=None):
        try:
            args = 'squeue '
            if job is not None:
                if job.isdigit():
                    args += ' -j {} '.format(job)  # search by job id
                else:
                    args += ' -n {} '.format(job)  # search by job name
            f = '--format=%all'
            args += f
            result = Shell.ssh(cluster, args)

            # TODO: process till header is found...(Need a better way)
            l = result.splitlines()
            for i, res in enumerate(l):
                if 'ACCOUNT|GRES|' in res:
                    result = "\n".join(l[i:])
                    break

            parser = TableParser(strip=True)
            d = parser.to_dict(result)

            # add cluster and updated to each entry
            for key in d.keys():
                d[key]['cluster'] = cluster
                d[key]['updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if format == 'json':
                return json.dumps(d, indent=4, separators=(',', ': '))

            else:
                return (dict_printer(d,
                                     order=['cluster',
                                            'jobid',
                                            'partition',
                                            'name',
                                            'user',
                                            'st',
                                            'time',
                                            'nodes',
                                            'nodelist',
                                            'updated'],
                                     output=format))
        except Exception as ex:
            return ex

    @classmethod
    def info(cls, cluster, format='json', all=False):

        if all:
            result = Shell.ssh(cluster, 'sinfo --format=\"%all\"')
        else:
            result = Shell.ssh(
                cluster,
                'sinfo --format=\"%P|%a|%l|%D|%t|%N\"')

        # ignor leading lines till header is found
        l = result.splitlines()
        for i, res in enumerate(l):
            if 'PARTITION|AVAIL|' in res:
                result = "\n".join(l[i:])
                break

        parser = TableParser(strip=False)
        d = parser.to_dict(result)

        # add cluster and updated to each entry
        for key in d.keys():
            d[key]['cluster'] = cluster
            d[key]['updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if format == 'json':
            return json.dumps(d, indent=4, separators=(',', ': '))

        else:
            return (dict_printer(d,
                                 order=['cluster',
                                        'partition',
                                        'avail',
                                        'timelimit',
                                        'nodes',
                                        'state',
                                        'nodelist',
                                        'updated'],
                                 output=format))

    @classmethod
    def test(cls, cluster, time):
        result = Shell.ssh(cluster,
                           "srun -n1 -t {} echo '#CLOUDMESH: Test ok'".format(
                               time))
        return result

    @classmethod
    def run(cls, cluster, cmd, **kwargs):

        print ("CCCC>", cluster)
        # determine the script name..

        #
        # TODO: script count is variable in data base, we test if fil exists and if it
        # does increase counter till we find one that does not, that will be new counter.
        # new couner will than be placed in db.
        #
        # define get_script_name(dirctory, prefix, counter)
        # there maybe s a similar thing already in the old cloudmesh
        #

        # if not kwargs['-name']:
        #
        #    old_count = Shell.ssh(cluster,
        #                          "ls {}*.sh | wc -l | sed 's/$/ count/'".
        #                          format(username))
        #    c = [f for f in old_count.splitlines() if 'count' in f]
        #    script_count = c[0].split()[0]
        # else:
        #    script_count = kwargs['-name']

        config = cls.read_config(cluster)
        cls.incr()
        data = {
            "cluster": cluster,
            "count": cls.counter(),
            "username": config["credentials"]["username"],
            "remote_experiment_dir": config["default"]["experiment_dir"],
            "queue": config["default"]["queue"],
            "id": None
        }
        data["script_base_name"] = "{username}-{count}".format(**data)
        data["script_name"] = "{username}-{count}.sh".format(**data)
        data["script_output"] = "{username}-{count}.out".format(**data)
        data["remote_experiment_dir"] = \
            "{remote_experiment_dir}/{count}".format(**data).format(**data)

        data["nodes"] = 1
        data["tasks_per_node"] = 1
        # overwrite defaults
        option_mapping = {'-t': '{tasks_per_node}'.format(**data),
                          '-N': '{nodes}'.format(**data),
                          '-p': '{queue}'.format(**data),
                          '-o': '{script_output}'.format(**data),
                          '-D': '{remote_experiment_dir}'.format(**data)}

        map(lambda (k, v):
            option_mapping.__setitem__(k, kwargs.get(k) or v),
            option_mapping.iteritems())

        config = cls.read_config(cluster)
        project = None
        try:
            project = config["credentials"]["project"]
            if project.lower() not in ["tbd", "none"]:
                option_mapping["-A"] = project
        except:
            pass

        for key in option_mapping:
            data[key] = option_mapping[key]

        # create the options for the script
        options = ""
        for key, value in option_mapping.iteritems():
            options += '#SBATCH {} {}\n'.format(key, value)

        data["command"] = cmd
        data["options"] = options

        script = textwrap.dedent(
            """
            #! /bin/sh
            {options}
            echo '#CLOUDMESH: BATCH ENVIRONMENT'
            echo 'BASIL_RESERVATION_ID:' $BASIL_RESERVATION_ID
            echo 'SLURM_CPU_BIND:' $SLURM_CPU_BIND
            echo 'SLURM_JOB_ID:' $SLURM_JOB_ID
            echo 'SLURM_JOB_CPUS_PER_NODE:' $SLURM_JOB_CPUS_PER_NODE
            echo 'SLURM_JOB_DEPENDENCY:' $SLURM_JOB_DEPENDENCY
            echo 'SLURM_JOB_NAME:' $SLURM_JOB_NAME
            echo 'SLURM_JOB_NODELIST:' $SLURM_JOB_NODELIST
            echo 'SLURM_JOB_NUM_NODES:' $SLURM_JOB_NUM_NODES
            echo 'SLURM_MEM_BIND:' $SLURM_MEM_BIND
            echo 'SLURM_TASKS_PER_NODE:' $SLURM_TASKS_PER_NODE
            echo 'MPIRUN_NOALLOCATE:' $MPIRUN_NOALLOCATE
            echo 'MPIRUN_NOFREE:' $MPIRUN_NOFREE
            echo 'SLURM_NTASKS_PER_CORE:' $SLURM_NTASKS_PER_CORE
            echo 'SLURM_NTASKS_PER_NODE:' $SLURM_NTASKS_PER_NODE
            echo 'SLURM_NTASKS_PER_SOCKET:' $SLURM_NTASKS_PER_SOCKET
            echo 'SLURM_RESTART_COUNT:' $SLURM_RESTART_COUNT
            echo 'SLURM_SUBMIT_DIR:' $SLURM_SUBMIT_DIR
            echo 'MPIRUN_PARTITION:' $MPIRUN_PARTITION
            srun -l echo '#CLOUDMESH: Starting'
            srun -l {command}
            srun -l echo '#CLOUDMESH: Test ok'
            """
        ).format(**data).replace("\r\n", "\n").strip()

        print (script)
        pprint(option_mapping)
        pprint(data)

        cls.create_remote_dir(cluster, data["remote_experiment_dir"])

        _from = Config.path_expand('~/.cloudmesh/{script_name}'.format(**data))
        _to = '{cluster}:{remote_experiment_dir}'.format(**data)
        data["from"] = _from
        data["to"] = _to
        data["script"] = script
        # write the script to local
        print(_from)
        print(_to)

        with open(_from, 'w') as local_file:
            local_file.write(script)

        # copy to remote host
        Shell.scp(_from, _to)

        # delete local file
        # Shell.execute('rm', _from)
        # import sys; sys.exit()

        # run the sbatch command

        cmd = 'sbatch {remote_experiment_dir}/{script_name}'.format(**data)
        data["cmd"] = cmd

        print ("CMD>", cmd)
        result = Shell.ssh(cluster, cmd)

        data["output"] = result

        # find id
        for line in result.split("\n"):
            print ("LLL>", line)
            if "Submitted batch job" in line:
                data["id"] = int(line.replace("Submitted batch job ", "").strip())
                break

        pprint(data)

        #
        # HACK, should not depend on Model.py
        #

        # from cloudmesh_client.db.model import BATCHJOB
        # name = ""
        # BATCHJOB(name,
        #         cluster=data["cluster"],
        #         id=data["id"],
        #         script=data["script"]) # has user and username which seems wrong

        # here what we have in data and want to store the - options are obviously wrong
        # and need to be full names
        """
        {'-D': '/N/u/gvonlasz/experiment/3',
         '-N': '1',
         '-o': 'gvonlasz-3.out',
         '-p': 'delta',
         '-t': '1',
         'cluster': 'india',
         'cmd': 'sbatch /N/u/gvonlasz/experiment/3/gvonlasz-3.sh',
         'command': 'uname',
         'count': 3,
         'from': '/Users/big/.cloudmesh/gvonlasz-3.sh',
         'id': 1346,
         'options': '#SBATCH -t 1\n#SBATCH -o gvonlasz-3.out\n#SBATCH -N 1\n#SBATCH -p delta\n#SBATCH -D /N/u/gvonlasz/experiment/3\n',
         'output': 'Submitted batch job 1346',
         'queue': 'delta',
         'remote_experiment_dir': '/N/u/gvonlasz/experiment/3',
         'script': "#! /bin/sh\n#SBATCH -t 1\n#SBATCH -o gvonlasz-3.out\n#SBATCH -N 1\n#SBATCH -p delta\n#SBATCH -D /N/u/gvonlasz/experiment/3\n\nsrun -l echo '#CLOUDMESH: Starting'\nsrun -l uname\nsrun -l echo '#CLOUDMESH: Test ok'",
         'script_base_name': 'gvonlasz-3',
         'script_name': 'gvonlasz-3.sh',
         'script_output': 'gvonlasz-3.out',
         'to': 'india:/N/u/gvonlasz/experiment/3',
         'username': 'gvonlasz'}
        """

        """
        we also want to store what part of the .out file,

        BASIL_RESERVATION_ID:
        SLURM_CPU_BIND:
        SLURM_JOB_ID: 1351
        SLURM_JOB_CPUS_PER_NODE: 12
        SLURM_JOB_DEPENDENCY:
        SLURM_JOB_NAME: gvonlasz-8.sh
        SLURM_JOB_NODELIST: d001
        SLURM_JOB_NUM_NODES: 1
        SLURM_MEM_BIND:
        SLURM_TASKS_PER_NODE: 12
        MPIRUN_NOALLOCATE:
        MPIRUN_NOFREE:
        SLURM_NTASKS_PER_CORE:
        SLURM_NTASKS_PER_NODE:
        SLURM_NTASKS_PER_SOCKET:
        SLURM_RESTART_COUNT:
        SLURM_SUBMIT_DIR: /N/u/gvonlasz
        MPIRUN_PARTITION:

        so maybe we want to use some of the names here as they reflect the env vars
        """

        #
        # add data to database
        #

        return data

    @classmethod
    def delete(cls, cluster, job):
        """
        This method is used to terminate a job with the specified
        job_id or job_name in a given cluster
        :param cluster: the cluster like comet
        :param job: the job id or name
        :return: success message or error
        """
        try:
            args = 'scancel '
            if job.isdigit():
                args += job
            else:
                args += "-n {}".format(job)

            Shell.ssh(cluster, args)
            return "Job {} killed successfully".format(job)
        except Exception as ex:
            return ex


if __name__ == "__main__":
    from pprint import pprint

    print(Hpc.queue("comet", format="json"))
