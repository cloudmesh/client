from cloudmesh_base.Shell import Shell
from cloudmesh_client.common import tables
import json


class Hpc(object):

    @classmethod
    def read_squeue(cls, format='json'):
        result = Shell.ssh("comet", "squeue")
        d = {}
        for i, line in enumerate(result.splitlines()):
            if not line.startswith('Warning:') and not line.__contains__('NODELIST(REASON)'):
                d[i] = {}
                d[i]['jobid'], d[i]['partition'], \
                d[i]['name'], d[i]['user'], d[i]['st'],\
                d[i]['time'], d[i]['nodes'],\
                d[i]['nodelist(reason)'] = line.split()

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
                                               'nodelist(reason)'],
                                        output=format))

    @classmethod
    def read_sinfo(cls, format='json'):
        result = Shell.ssh("comet", "sinfo")
        d = {}
        for i, line in enumerate(result.splitlines()):
            if not line.startswith('Warning:') and not line.__contains__('NODELIST'):
                d[i] = {}
                d[i]['partition'], d[i]['avail'], \
                d[i]['timelimit'], d[i]['nodes'], d[i]['state'],\
                d[i]['nodelist'] = line.split()

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
