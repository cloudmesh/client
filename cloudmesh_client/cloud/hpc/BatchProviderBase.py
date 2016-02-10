from cloudmesh_client.cloud.counter import Counter
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.ConfigDict import ConfigDict


# noinspection PyUnusedLocal,PyBroadException
class BatchProviderBase(object):
    prefix = "job"
    jobid = 0

    @classmethod
    def queue(cls, **kwargs):
        ValueError("Not yet implemented")

    @classmethod
    def delete(cls, **kwargs):
        ValueError("Not yet implemented")

    @classmethod
    def run(cls, **kwargs):
        ValueError("Not yet implemented")

    @classmethod
    def counter(cls):
        cls.jobid = Counter.get()
        return cls.jobid

    @classmethod
    def incr(cls):
        Counter.incr()
        cls.jobid = Counter.get()
        return cls.jobid

    @classmethod
    def jobname(cls, counter=None):
        if counter is None:
            counter = cls.counter()
        data = {
            "counter": counter,
            "prefix": cls.prefix
        }
        return "{prefix}-{counter}".format(**data)

    @classmethod
    def create_remote_dir(cls, cluster, directory):
        Shell.ssh(cluster, "mkdir -p {dir}".format(dir=directory))

    @classmethod
    def read_config(cls, cluster):
        """
        reads in the cluster config from the yaml file and returns the specific cluster information

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
                        username: gregor
                        project: None
                    default:
                        queue: delta
                        experiment_dir: ./experiment

        :param cls:
        :param cluster:
        :return:
        """

        try:
            config = cls.config
        except:
            cls.config = None
        if cls.config is None:
            cls.config = ConfigDict("cloudmesh.yaml")["cloudmesh.hpc"]
            cls.experiment_name_format = cls.config["experiment"]["name"]
        return cls.config["clusters"][cluster]
