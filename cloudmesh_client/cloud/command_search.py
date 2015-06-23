from cloudmesh_base.Shell import Shell
from cmd3.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.ConfigDict import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import cloudmesh_client.common.tables as tables
from cloudmesh_client.db.models import VM,FLAVOR,DEFAULT,IMAGE
import cloudmesh_client.db.models
import cloudmesh_client.db.models as models
from sqlalchemy import text

class command_search(object):

    @classmethod
    def do_search(cls, table, filter):
        filename = Config.path_expand("~/.cloudmesh/cloudmesh.db")
        endpoint = 'sqlite:///{:}'.format(filename)
        engine = create_engine(endpoint)
        Base = declarative_base(bind=engine)
        Session = sessionmaker(bind=engine)
        session = Session()

        where = ""
        if filter:
            for i in range(len(filter)):
                split = filter[i].split('=')
                where = '{} = \'{}\''.format(split[0], split[1])
                filter[i] = where
            where = """ AND """.join(filter)
            where = 'WHERE {}'.format(where)

        print where

        _table = table.upper()
        sql = text(""" SELECT * FROM {} {}""".format(_table, where))

        try:
            if table == 'vm':
                #r = session.query(VM).all()
                r = session.query(VM).from_statement(sql).all()
            elif table == 'flavor':
                r = session.query(FLAVOR).from_statement(sql).all()
            elif table == 'image':
                r = session.query(IMAGE).from_statement(sql).all()
            elif table == 'default':
                r = session.query(DFAULT).from_statement(sql).all()
            else:
                Console.error("Please specify a valid table")
                return
        except Exception:
            Console.error("Please specify a valid search")
            return

        if r:
            print "{} TABLE".format(_table)
            result = dict()
            for u in r:
                _id = u.id
                values = {}
                for key in u.__dict__.keys():
                    if not key.startswith("_sa"):
                        values[key] = u.__dict__[key]
                result[_id] = values

            output = models.dict_printer(result, order=None, header=None, output="table", sort_keys=True)
            print(output)
        else:
            print("Nothing found")

