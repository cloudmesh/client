import json

from cloudmesh_base.Shell import Shell
from cloudmesh_client.common.Printer import dict_printer
from cloudmesh_client.common.TableParser import TableParser
from cloudmesh_client.common.ConfigDict import Config, ConfigDict


class Hpc(object):
    @classmethod
    def queue(cls, cluster, format='json', job=None):
        args = 'squeue '
        if job:
            args += '--job={} '.format(job)
        f = '--format=%all'
        args += f
        result = Shell.ssh(cluster, args)
        #
        # TODO: this will not work as some jobs could have error in their names
        # if result.__contains__('error'):
        #    return result

        parser = TableParser()
        d = parser.to_dict(result)

        if format == 'json':
            return json.dumps(d, indent=4, separators=(',', ': '))

        else:
            return (dict_printer(d,
                                 order=['jobid',
                                        'partition',
                                        'name',
                                        'user',
                                        'st',
                                        'time',
                                        'nodes',
                                        'nodelist'],
                                 output=format))

    @classmethod
    def info(cls, format='json', all=False):

        if all:
            result = Shell.ssh("comet", 'sinfo --format=\"%all\"')
        else:
            result = Shell.ssh(
                "comet",
                'sinfo --format=\"%P|%a|%l|%D|%t|%N\"')

        parser = TableParser()
        d = parser.to_dict(result)

        if format == 'json':
            return json.dumps(d, indent=4, separators=(',', ': '))

        else:
            return (dict_printer(d,
                                 order=['partition',
                                        'avail',
                                        'timelimit',
                                        'nodes',
                                        'state',
                                        'nodelist'],
                                 output=format))

    @classmethod
    def test(cls, cluster, time):
        result = Shell.ssh(cluster,
                           "srun -n1 -t {} echo '#CLOUDMESH: Test ok'".format(
                               time))
        return result

    @classmethod
    def run(cls, cluster, cmd, **kwargs):
        # determine the script name..
        d = ConfigDict("cloudmesh.yaml")
        username = d["cloudmesh"]["profile"][
            "firstname"]  # FIX: need to determine the cloudmesh name

        if not kwargs['-name']:
            old_count = Shell.ssh(cluster,
                                  "ls {}*.sh | wc -l | sed 's/$/ count/'".
                                  format(username))
            c = [f for f in old_count.splitlines() if 'count' in f]
            script_count = c[0].split()[0]
        else:
            script_count = kwargs['-name']

        script = username + '-' + script_count

        # overwrite defaults
        option_mapping = {'-t': '1',
                          '-N': '1',
                          '-p': '',
                          '-o': script + '.out'}
        map(lambda (k, v):
            option_mapping.__setitem__(k, kwargs.get(k) or v),
            option_mapping.iteritems())

        # create the script...
        result = ['#!/bin/sh']
        for key, value in option_mapping.iteritems():
            result.append('#SBATCH {} {}'.format(key, value))

        # append the commands...
        result.extend(["srun -l echo '#CLOUDMESH: Starting'",
                       'srun -l {}'.format(cmd),
                       "srun -l echo '#CLOUDMESH: Test ok'"])
        result = '\n'.join(result)
        # print(result)

        script_name = script + '.sh'
        _from = '~/.cloudmesh/{}'.format(script_name)
        _to = '{}:~/'.format(cluster)
        # write the script to local
        with open(Config.path_expand(_from), 'w') as local_file:
            local_file.write(result)

        # copy to remote host
        Shell.scp(_from, _to)
        Shell.ssh(cluster,
                  'dos2unix {}'.format(script_name))

        # delete local file
        Shell.execute('rm', _from)

        # run the sbatch command
        sbatch_result = Shell.ssh(
            cluster,
            'sbatch {}'.format(script_name))

        return (sbatch_result +
                '\n .The output file {} is in ~ directory of the cluster'.
                format(option_mapping['-o']))
