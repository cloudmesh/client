from cloudmesh_base.Shell import Shell
from cloudmesh_client.common import tables
import json


class Hpc(object):
    @staticmethod
    def _clean(str):
        if str == '':
            str = 'None'
        return str.strip().lower().replace(":", "_"). \
            replace("(", "_").replace(")", "").replace("/", "_")

    @classmethod
    def queue(cls, cluster, format='json', job=None):
        args = 'squeue '
        if job:
            args += '--job={} '.format(job)
        f = '--format=%all'
        args += f
        result = Shell.ssh(cluster, args)
        if result.__contains__('error'):
            return result

        lines = result.splitlines()

        print lines[0]
        headers = [Hpc._clean(h) for h in lines[0].split("|")]

        lines = lines[1:]

        print '\n'.join(headers)
        # print lines

        d = {}
        for line in lines:
            data = [h.strip() for h in line.split("|")]
            print headers
            entry = {}
            for i in range(0, len(headers)):
                entry[headers[i]] = data[i]
            d[entry['jobid']] = entry

        if format == 'json':
            return json.dumps(d, indent=4, separators=(',', ': '))

        else:
            return (tables.dict_printer(d,
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

        lines = result.splitlines()

        headers = [Hpc._clean(h) for h in lines[0].split("|")]

        i = 0
        d = {}
        for line in lines:
            data = [h.strip() for h in line.split("|")]
            entry = {}
            for index in range(0, len(headers)):
                entry[headers[index]] = data[index]
            d[str(i)] = entry
            i += 1

        if format == 'json':
            return json.dumps(d, indent=4, separators=(',', ': '))

        else:
            return (tables.dict_printer(d,
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
