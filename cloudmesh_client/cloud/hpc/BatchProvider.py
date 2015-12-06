from cloudmesh_client.cloud.hpc.BatchProviderBase import BatchProviderBase
from cloudmesh_client.cloud.hpc.BatchProviderSLURM import BatchProviderSLURM
from cloudmesh_client.common.ConfigDict import ConfigDict


class BatchProvider(BatchProviderBase):

    def __init__(self, name, user=None, flat=True):
        super(BatchProvider, self).__init__(name)

        try:
            d = ConfigDict("cloudmesh.yaml")
            details = d["cloudmesh"]["hpc"]["clusters"][name]

            if details["cm_type"] == "slurm":
                self.provider = BatchProviderSLURM(name)
                self.provider_class = BatchProviderSLURM

            else:
                ValueError("batch  provider not yet supported")

        except Exception, e:
            import traceback
            print(traceback.format_exc())
            print(e)

