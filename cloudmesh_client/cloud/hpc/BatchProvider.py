from cloudmesh_client.cloud.hpc.provider.slurm.BatchProviderSLURM import BatchProviderSLURM
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Error import Error


# noinspection PyPep8Naming
def BatchProvider(name, user=None):
    """
    Returns a provider for a given batch system that is defined
    in the cloudmesh.yaml file. Here you find a section such as::

        hpc:
            active:
            - india
            clusters:
              india:
                cm_heading: India HPC CLuster
                cm_host: india
                cm_label: indiahpc
                cm_type: slurm
                cm_type_version: 14.11.9
                credentials:
                  username: TBD
                  project: None
                default:
                  queue: delta
                  experiment_dir: /N/u/{username}/experiment
                  prefix:
                    username: null

    You can define a new resource by copying this section under india and
    give it a name according to your cluster. Fill out the username,
    and if appropirate define a project, which is the
    account this queue is charged under

    Ussage::

      provider = BatchProvider("india")

    Additional functions are defined as it inherits from BatchProviderBase
    and the provider type which is in the above example slurm

    :param name: name of the cluster in the cloudmesh yaml file
    :param user: cloudmesh user name associated with this queue.
    :return: the provider
    """
    try:
        d = ConfigDict("cloudmesh.yaml")
        details = d["cloudmesh"]["hpc"]["clusters"][name]

        if details["cm_type"].lower() in ["slurm"]:
            return BatchProviderSLURM()
        else:
            ValueError("batch  provider not supported.")

    except Exception as e:
        Error.traceback(e)
