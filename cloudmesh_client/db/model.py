from __future__ import print_function

import os
from datetime import datetime

from sqlalchemy import Column, Integer, String, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

from cloudmesh_client.common.ConfigDict import Config
from cloudmesh_client.common.ConfigDict import ConfigDict

"""

kind = the general type of the object that can be helpful for the location
       of similar objects accross providers

        examples: vm, image, flavor, ...

type = the table name of the object

provider name of the providor

            example: "openstack", "libcloud", "aws", ...


category = name of the category, this can be the name of the clod,
            batch system or other
            from the name of the category other information can be derived
            while retrieving it from the yaml file

            examples: kilo, chameleon, cybera-e, aws, ...
                      e..g. the names of the clouds

please note that kind and type seem to be confusingly named as the kind is used in

"""