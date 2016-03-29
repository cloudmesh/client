from __future__ import print_function

from cloudmesh_client.common.ConfigDict import ConfigDict, Config
import os
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from ..borg import borg

import os
from datetime import datetime

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

# noinspection PyPep8Naming

@singleton
class database(object):
    """
    A simple class with all the details to create and
    provide some elementary methods for the database.

    This class is a state sharing class also known as Borg Pattern.
    Thus, multiple instantiations will share the same sate.

    TODO: An import to the model.py will instantiate the db object.
    """
    def __init__(self):
        """Initializes the database and shares the state with other instantiations of it"""

        self.debug = False
        self.filename = None
        self.endpoint = None
        self.engine = None
        self.Base = None
        self.meta = None
        self.user = ConfigDict("cloudmesh.yaml")["cloudmesh.profile.username"]

        self.filename = Config.path_expand(
            os.path.join("~", ".cloudmesh", "cloudmesh.db"))
        self.endpoint = 'sqlite:///{:}'.format(self.filename)
        self.engine = create_engine(self.endpoint)
        self.Base = declarative_base(bind=self.engine)

        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)
        # self.session = sessionmaker(bind=self.engine)

    def tables(self, kind=None):
        """
        :return: the list of tables in model
        """
        if kind is None:
            classes = [cls for cls in self.Base.__subclasses__()]
        else:

            classes = []
            for cls in self.Base.__subclasses__():
                if cls.kind == kind:
                    classes.append(cls)
        return classes

    def tablenames(self):
        """
        :return: the list of table names in model
        """
        names = [name.__tablename__ for name in self.tables()]
        return names

    def table(self, name):
        """
        :return: the table class based on a given table name.
                 In case the table does not exist an exception is thrown
        """
        for t in self.tables():
            if t.__tablename__ == name:
                return t

        raise ("ERROR: unkown table {}".format(name))


