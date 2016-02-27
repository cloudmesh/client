from cloudmesh_client.common.Shell import Shell


# noinspection PyBroadException
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
            except Exception as e:
                pass
        else:
            try:
                result = Shell.ssh(cluster, "rm -rf experiment/*").split("\n")
            except Exception as e:
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
            except Exception as e:
                result = None
        else:
            try:
                result = Shell.ssh(cluster, "ls experiment").split("\n")
                ids = sorted([int(i) for i in result])
                if format not in [None, 'txt']:
                    result = ids
            except Exception as e:
                result = None

        return result

    @classmethod
    def output(cls, cluster, id=None, format=None):
        data = {
            "CLUSTER": cluster,
            "ID": id,
        }
        result = None
        if id is None:
            ids = list(cluster)
        else:
            ids = [id]
        result = []
        for i in ids:
            try:
                result.append(Shell.ssh(cluster, "cat experiment/{}/*.out".format(i)))
            except:
                result.append("")
        # if result == []:
        #    result = None
        return result
