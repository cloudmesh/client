from cloudmesh_base.Shell import Shell
class Experiment(object):

    @classmethod
    def rm(cls, cluster, id=None, format=None):
        data = {
            "CLUSTER": cluster,
            "ID": id,
        }
        result = None
        if id is not None:
            try:
                result = Shell.ssh(cluster, "rm -rf experiment/{ID}".format(**data))
            except Exception, e:
                pass
        else:
            try:
                result = Shell.ssh(cluster, "rm -rf experiment/*").split("\n")
            except Exception, e:
                pass

        return result

    @classmethod
    def list(cls, cluster, id=None, format=None):
        data = {
            "CLUSTER": cluster,
            "ID": id,
        }
        result = None
        if id is not None:
            try:
                result = Shell.ssh(cluster, "ls experiment/{ID}".format(**data))
                result = result.split("\n")
            except Exception, e:
                result = None
        else:
            try:
                result = Shell.ssh(cluster, "ls experiment").split("\n")
                ids = sorted([int(i) for i in result])
                if format not in [None, 'txt']:
                   result = ids
            except Exception, e:
                result = None

        return result

"""
        elif arguments["experiment"] and arguments["output"]:
            # hpc experiment output ID [--cluster=CLUSTER]
            result = Shell.ssh(cluster, "ls experiment {ID}".format(**arguments))
            print (result)
"""
