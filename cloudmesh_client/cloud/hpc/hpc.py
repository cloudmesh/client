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
                d[i]['JOBID'], d[i]['PARTITION'], \
                d[i]['NAME'], d[i]['USER'],d[i]['ST'],\
                d[i]['TIME'], d[i]['NODES'],\
                d[i]['NODELIST(REASON)'] = line.split()

        if format == 'json':
            return json.dumps(d, indent=4, separators=(',', ': '))

        else:
            return (tables.dict_printer(d,
                                        order=['JOBID',
                                               'PARTITION',
                                               'NAME',
                                               'USER',
                                               'ST',
                                               'TIME',
                                               'NODES',
                                               'NODELIST(REASON)'],
                                        output=format))