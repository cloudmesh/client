from __future__ import print_function

from cloudmesh_client.common.ConfigDict import ConfigDict, Config
import os
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base


import os
from datetime import datetime


# noinspection PyPep8Naming
class database(object):
    """
    A simple class with all the details to create and
    provide some elementary methods for the database.

    This class is a state sharing class also known as Borg Pattern.
    Thus, multiple instantiations will share the same sate.

    TODO: An import to the model.py will instantiate the db object.
    """
    __monostate = None

    def __init__(self):
        """Initializes the database and shares the state with other instantiations of it"""
        self.debug = False
        self.filename = None
        self.endpoint = None
        self.engine = None
        self.Base = None
        self.meta = None
        self.user = ConfigDict("cloudmesh.yaml")["cloudmesh.profile.username"]

        if not database.__monostate:
            database.__monostate = self.__dict__
            self.activate()

        else:
            self.__dict__ = database.__monostate

    def activate(self):
        """activates the shared variables"""

        # engine = create_engine('sqlite:////tmp/test.db', echo=debug)

        self.filename = Config.path_expand(
            os.path.join("~", ".cloudmesh", "cloudmesh.db"))
        self.endpoint = 'sqlite:///{:}'.format(self.filename)
        self.engine = create_engine(self.endpoint)
        self.Base = declarative_base(bind=self.engine)

        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)
        # self.session = sessionmaker(bind=self.engine)


db = database()


def tables(kind=None):
    """
    :return: the list of tables in model
    """
    if kind is None:
        classes = [cls for cls in db.Base.__subclasses__()]
    else:

        classes = []
        for cls in db.Base.__subclasses__():
            if cls.kind == kind:
                classes.append(cls)
    return classes


def tablenames():
    """
    :return: the list of table names in model
    """
    names = [name.__tablename__ for name in tables()]
    return names


def table(name):
    """
    :return: the table class based on a given table name.
             In case the table does not exist an exception is thrown
    """
    for t in tables():
        if t.__tablename__ == name:
            return t

    raise ("ERROR: unkown table {}".format(name))
