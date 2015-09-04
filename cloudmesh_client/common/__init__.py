import os

from cloudmesh_base.util import path_expand

dot_cloudmesh = os.path.join(path_expand("~"), ".cloudmesh")
cloudmesh_yaml = os.path.join(path_expand("~"), ".cloudmesh", "cloudmesh.yaml")
cloudmesh_db = os.path.join(path_expand("~"), ".cloudmesh", "cloudmesh.db")
