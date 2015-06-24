from __future__ import print_function
from cmd3.console import Console
from cloudmesh_client.common.ConfigDict import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from cloudmesh_client.db.models import DEFAULT
from cloudmesh_client.db.models import dict_printer
from sqlalchemy import MetaData, Table

class command_default(object):
    @classmethod
    def list(cls):
        filename = Config.path_expand("~/.cloudmesh/cloudmesh.db")
        endpoint = 'sqlite:///{:}'.format(filename)
        engine = create_engine(endpoint)
        Base = declarative_base(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        table = session.query(DEFAULT).all()
        meta = MetaData()
        meta.reflect(bind=engine)

        default = Table("default", meta, autoload=True, autoload_with=engine)
        columns = [c.name for c in default.columns]
        print ('Default Columns: {}'.format(columns))

        """ #Not sure if I have to search through DEFAULT table
        table = session.query(DEFAULT).all()
        if table:
            result = dict()
            for u in table:
                _id = u.id
                values = {}
                for key in u.__dict__.keys():
                    if not key.startswith("_sa"):
                        values[key] = u.__dict__[key]
                result[_id] = values

            output = dict_printer(result, order=None, header=None, output="table", sort_keys=True)
            print(output)
        else:
            print("Nothing found")
        """


    @classmethod
    def set(cls, key, value):
        Console.ok("Set")
        print(key, value)

    @classmethod
    def get(cls, key):
        Console.ok("Get")
        print(key)
