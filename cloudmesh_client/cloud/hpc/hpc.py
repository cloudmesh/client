from cloudmesh_base.Shell import Shell
from cloudmesh_client.common import tables
from cloudmesh_client.common.TableParser import TableParser

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
        #
        # TODO: this will not work as some jobs could have error in their names
        # if result.__contains__('error'):
        #    return result

        parser = TableParser()
        d = parser.parse_to_dict(result)

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


        parser = TableParser()
        d = parser.parse_to_dict(result)

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
