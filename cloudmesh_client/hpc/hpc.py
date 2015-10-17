from cloudmesh_base.Shell import Shell
from cloudmesh_client.common import tables
import json


def read_squeue():
    result = Shell.ssh("comet", "squeue")
    d = {}
    for i, line in enumerate(result.splitlines()):
        if not line.startswith('Warning:'):
            d[i] = {}
            d[i]['JOBID'], d[i]['PARTITION'], d[i]['NAME'], d[i]['USER'],d[i]['ST'], d[i]['TIME'], d[i]['NODES'],\
            d[i]['NODELIST(REASON)'] = line.split()
    print(json.dumps(d, indent=4, separators=(',', ': ')))

    # print(tables.dict_printer(d))
