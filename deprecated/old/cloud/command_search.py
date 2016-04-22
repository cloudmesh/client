from cloudmesh_base.Shell import Shell
from cmd3.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.ConfigDict import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from cloudmesh_client.db.models import VM, FLAVOR, DEFAULT, IMAGE
import cloudmesh_client.db.models as models
from sqlalchemy import text
from cloudmesh_base.hostlist import Parameter
import cloudmesh_client.db.CloudmeshDatabase as cm
import re


class command_search(object):
    @classmethod
    def do_search(cls, table, order, filter):
        c = cm()

        if filter:
            for i in range(len(filter)):

                regex = re.compile("(!=|>=|<=|=|>|<)", re.I)
                sep = regex.search(filter[i]).groups()
                if sep:
                    separator = sep[0]
                else:
                    Console.error("Please specify a valid filter")
                    return

                split = filter[i].split(separator)

                if '[' in filter[i]:
                    parameters = Parameter.expand(split[1])
                    parameters = ['{} = \'{}\''.format(split[0], parameters[j]) for j in range(len(parameters))]
                    parameters = """ OR """.join(parameters)
                    where = '( {} )'.format(parameters)
                    filter[i] = where
                else:
                    where = '{} {} \'{}\''.format(split[0], separator, split[1])
                    filter[i] = where

            where = """ AND """.join(filter)
            where = ' WHERE {}'.format(where)
        else:
            where = ""

        _table = table.upper()
        sql = text(""" SELECT * FROM {}{}""".format(_table, where))

        try:
            if table == 'vm' or table == 'flavor' or table == 'image':
                model = globals()[_table]
                r = c.session.query(model).from_statement(sql).all()
            else:
                Console.error("Please specify a valid table")
                return
        except Exception:
            Console.error("Please specify a valid search")
            return

        if r:

            print "{} TABLE".format(_table)
            result = c.object_to_dict(r)
            if order:
                _order = order.split(',')
            else:
                _order = None
            output = models.Printer.write(result, order=_order, header=None, output="table", sort_keys=True)
            print(output)
        else:
            print("Nothing found")
