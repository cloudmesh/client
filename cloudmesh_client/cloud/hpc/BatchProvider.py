from cloudmesh_client.cloud.hpc.provider.slurm.BatchProviderSLURM import BatchProviderSLURM
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Error import Error

# noinspection PyPep8Naming
def BatchProvider(name, user=None):
    try:
        d = ConfigDict("cloudmesh.yaml")
        details = d["cloudmesh"]["hpc"]["clusters"][name]

        if details["cm_type"].lower() in ["slurm"]:
            return BatchProviderSLURM()
        else:
            ValueError("batch  provider not supported.")

    except Exception, e:
        Error.traceback(e)
