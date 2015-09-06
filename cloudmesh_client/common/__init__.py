import os

from cloudmesh_client.common.ConfigDict import Config

dot_cloudmesh = os.path.join(Config.path_expand("~"), ".cloudmesh")
cloudmesh_yaml = os.path.join(Config.path_expand("~"), ".cloudmesh", "cloudmesh.yaml")
cloudmesh_db = os.path.join(Config.path_expand("~"), ".cloudmesh", "cloudmesh.db")
