import os
import shutil

import cloudmesh_client.version
from cloudmesh_client.cloud.register import CloudRegister
from cloudmesh_client.common.ConfigDict import ConfigDict, Config
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.todo import TODO
from cloudmesh_client.common.util import path_expand
from cloudmesh_client.db import CloudmeshDatabase
from cloudmesh_client.shell.console import Console
from .common.Printer import Printer
from .db.CloudmeshDatabase import *
from .db.general.model import *
from .db.libcloud.model import *
from .db.openstack.model import *
#from .default import Default
#from .var import Var

__version__ = cloudmesh_client.version.__version__


def create_cloudmesh_yaml(filename):
    if not os.path.exists(filename):
        path = os.path.dirname(filename)
        if not os.path.isdir(path):
            Shell.mkdir(path)
        etc_path = os.path.dirname(cloudmesh_client.__file__)
        etc_file = os.path.join(etc_path, "etc", "cloudmesh.yaml")
        to_dir = path_expand("~/.cloudmesh")
        shutil.copy(etc_file, to_dir)
        os.system("chmod -R go-rwx " + path_expand("~/.cloudmesh"))
        Console.ok("~/.cloudmesh/cloudmesh.yaml created")


def setup_yaml():
    filename = path_expand("~/.cloudmesh/cloudmesh.yaml")
    create_cloudmesh_yaml(filename)


setup_yaml()
