import json
from cloudmesh_client.cloud.hpc.BatchProvider import BatchProvider


# TODO: is this outdated and superseded by hpc.py?
class Squeue(object):
    @staticmethod
    def squeue_to_json(input_str):
        d = {}
        for i, line in enumerate(input_str.splitlines()):
            if not line.startswith('Warning:') and not line.__contains__(
                    'NODELIST(REASON)'):
                d[i] = {}
                # noinspection PyPep8
                d[i]['jobid'], \
                d[i]['partition'], \
                d[i]['name'], \
                d[i]['user'], \
                d[i]['st'], \
                d[i]['time'], \
                d[i]['nodes'], \
                d[i]['nodelist(reason)'] = line.split()

        json_str = json.dumps(d, indent=4, separators=(',', ': '))
        # assert returned value is string
        assert isinstance(json_str, str)
        # convert to json obj
        return json.loads(json_str)

    @staticmethod
    def get(user=None, name=None):
        squeue_json = Squeue.read_squeue()
        # assert returned value is string
        assert isinstance(squeue_json, str)
        # convert to json obj
        json_obj = json.loads(squeue_json)

        d = {}
        for i, key in enumerate(json_obj.keys()):
            # both user, name parameters are specified
            if user and name:
                if user == json_obj[key]["user"] and name == json_obj[key]["name"]:
                    d[i] = json_obj[key]
            # only user parameter is specified
            elif user:
                if user == json_obj[key]["user"]:
                    d[i] = json_obj[key]
            # only name parameter is specified
            elif name:
                if name == json_obj[key]["name"]:
                    d[i] = json_obj[key]
            # no parameters specified, return all
            else:
                d[i] = json_obj[key]

        # return json dump
        return json.dumps(d, indent=4, separators=(',', ': '))

    @staticmethod
    def read_squeue():
        # read squeue from comet
        # TODO: check this function
        name = None
        provider = BatchProvider(name)
        return provider.read_squeue(format="json")


if __name__ == "__main__":
    # TODO: user should be read from yaml file
    print(Squeue.read_squeue())
    print(Squeue.get(name="NGBW-JOB", user="cipres"))
    # print(Squeue.get(name="NGBW-JOB"))
    # print(Squeue.get(user="cipres"))
    # print(Squeue.get())
