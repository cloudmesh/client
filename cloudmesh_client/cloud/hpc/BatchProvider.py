from cloudmesh_client.cloud.hpc.provider.slurm.BatchProviderSLURM import BatchProviderSLURM
from cloudmesh_client.common.ConfigDict import ConfigDict


def BatchProvider(name, user=None):
    try:
        d = ConfigDict("cloudmesh.yaml")
        details = d["cloudmesh"]["hpc"]["clusters"][name]

        if details["cm_type"].lower() in ["slurm"]:
            return BatchProviderSLURM()
        else:
            ValueError("batch  provider not supported.")

    except Exception, e:
        import traceback
        print(traceback.format_exc())
        print(e)
