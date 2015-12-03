import json

from cloudmesh_base.Shell import Shell
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.common.TableParser import TableParser
from cloudmesh_client.common.ConfigDict import Config, ConfigDict
from datetime import datetime

import textwrap
from pprint import pprint

class Hpc(object):

    @classmethod
    def get_script_base_name(cls):
        # config = cls.read_hpc_config(cluster)
        return "gregor"

    @classmethod
    def count(cls):
        return "0"

    @classmethod
    def create_remote_experiment_dir(cls, cluster):
        config = cls.read_hpc_config(cluster)
        data = {"dir": config["default"]["experiment_dir"]}
        Shell.ssh(cluster, "mkdir -p {dir}".format(**data))
        return data["dir"]

    @classmethod
    def read_hpc_config(cls, cluster):
        """
        reads in the cluster config from the yaml file and returns the specific cluster informationt

        newhpc:
            experiment:
                    name: gregor-00000
            active:
            - comet
            - juliet
            clusters:
                india:
                    cm_heading: India HPC CLuster
                    cm_host: india
                    cm_label: indiahpc
                    cm_type: slurm
                    cm_type_version: 14.11.9
                    credentials:
                        project: None
                    default:
                        queue: delta
                        experiment_dir: ./experiment

        :param cls:
        :param cluster:
        :return:
        """
        hpc = "newhpc" # change to hpc when transition is made

        try:
            config = cls.config
        except:
            cls.config = None
        if cls.config is None:
            cls.config = ConfigDict("cloudmesh.yaml")["cloudmesh.newhpc"]
            pprint (cls.config)
            cls.experiment_name_format = cls.config["experiment"]["name"]
        return cls.config["clusters"][cluster]


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

        username = ConfigDict("cloudmesh.yaml")["cloudmesh.profile.username"]

        #
        # TODO: script count is variable in data base, we test if fil exists and if it
        # does increase counter till we find one that does not, that will be new counter.
        # new couner will than be placed in db.
        #
        # define get_script_name(dirctory, prefix, counter)
        # there maybe s a similar thing already in the old cloudmesh
        #

        #if not kwargs['-name']:
        #
        #    old_count = Shell.ssh(cluster,
        #                          "ls {}*.sh | wc -l | sed 's/$/ count/'".
        #                          format(username))
        #    c = [f for f in old_count.splitlines() if 'count' in f]
        #    script_count = c[0].split()[0]
        #else:
        #    script_count = kwargs['-name']

        data = {
            "cluster": cluster,
            "count": cls.count(),
            "username": username
        }
        data["script_base_name"] = "{username}-{count}".format(**data)
        data["script_name"] = "{username}-{count}.sh".format(**data)
        data["script_output"] = "{username}-{count}.out".format(**data)
        config = cls.read_hpc_config(cluster)
        data["remote_experiment_dir"] = config["default"]["experiment_dir"]
        data["remote_experiment_dir"] = \
            "{remote_experiment_dir}/{script_base_name}".format(**data)

        # overwrite defaults
        option_mapping = {'-t': '1',
                          '-N': '1',
                          '-p': '',
                          '-o': '{remote_experiment_dir}/{script_output}'.format(**data)}

        map(lambda (k, v):
            option_mapping.__setitem__(k, kwargs.get(k) or v),
            option_mapping.iteritems())


        config = cls.read_hpc_config(cluster)
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
            srun -l echo '#CLOUDMESH: Starting'
            srun -l {command}
            srun -l echo '#CLOUDMESH: Test ok'
            """
        ).format(**data).replace("\r\n","\n")

        print (script)
        pprint(option_mapping)
        pprint(data)

        cls.create_remote_experiment_dir(cluster)


        _from = Config.path_expand('~/.cloudmesh/{script_name}'.format(**data))
        _to = '{cluster}:{remote_experiment_dir}'.format(**data)
        # write the script to local
        print(_from)
        print(_to)

        with open(_from, 'w') as local_file:
            local_file.write(script)

        # copy to remote host
        Shell.scp(_from, _to)


        # delete local file
        # Shell.execute('rm', _from)

        # run the sbatch command
        sbatch_result = Shell.ssh(
            cluster,
            'sbatch {remote_experiment_dir}/{script_name}'.format(**data)
        )

        return (sbatch_result +
                '\nThe output file {script_output} is in the home directory of the cluster'.
                format(**data))

    @classmethod
    def kill(cls, cluster, job):
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

    print(Hpc.queue("comet",format="json"))

