from __future__ import print_function

import getpass
from pprint import pprint

from cloudmesh_client.db.model import database, DEFAULT
from sqlalchemy.orm import sessionmaker
from cloudmesh_base.util import banner
from sqlalchemy import inspect
from cloudmesh_base.hostlist import Parameter
from cloudmesh_client.db.model import tables, tablenames, table


class CloudmeshDatabase(object):
    def __init__(self, cm_user=None):
        """
        initializes the CloudmeshDatabase for a specific user.
        The user is used to add entries augmented with it.

        :param cm_user: The username that is used to be added to the objects in teh database
        """





        self.db = database()
        self.db.Base.metadata.create_all()
        self.session = self.connect()

        if cm_user is None:
            self.cm_user = getpass.getuser()
        else:
            self.cm_user = cm_user


    def connect(self):
        """
        before any method is called we need to connect to the database

        :return: the session of the database
        """
        Session = sessionmaker(bind=self.db.engine)
        self.session = Session()
        return self.session


    def save(self):
        self.session.commit()
        self.session.flush()

    def delete(self, item):
        """
        NOTTESTED
        :param item:
        :return:
        """
        result = self.session.delete(item)
        self.save()

    def dict(self, table):
        """
        returns a dict from all elements in the table

        :param table:
        :return:
        """
        return self.object_to_dict(self.session.query(table).all())

    def json(self, table):
        """
        returns a json representation from all elements in the table

        :param table:
        :return:
        """
        d = self.dict(table)
        return json.dumps(d)

    def info(self, what=None, kind=None):
        """
        prints information about the database
        """
        count_result = {}
        if kind is None:
            kinds = tablenames()
        else:
            kinds = Parameter.expand(kind)
        if what is None:
            infos = "table,count"
        else:
            infos = Parameter.expand(what)

        banner("Databse table information", c="-")
        inspector = inspect(self.db.engine)

        if "table" in infos:
            for table_name in inspector.get_table_names():
                if table_name in kinds:
                    print(table_name + ":")
                    for column in inspector.get_columns(table_name):
                        print("  ", column['name'], column['type'])

        sum = 0
        if "count" in infos:
            for tablein in inspector.get_table_names():
                if table_name in kinds:
                    t = table(table_name)
                    rows = self.session.query(t).count()
                    count_result[table_name] = rows
                    print("Count {:}: {:}".format(table_name, rows))
                    sum = sum + rows
            count_result['sum'] = sum

        return count_result

    def query(self, table):
        return self.session.query(table)

    def add(self, o):
        self.session.add(o)
        self.session.commit()
        self.session.flush()

    # TODO: change name to kwargs
    def get(self, table, name):
        return  self.session.query(table).filter_by(name=name).first()


def main():
    cm = CloudmeshDatabase(cm_user="gregor")

    m = DEFAULT("hallo", "world")
    m.newfield__hhh = 13.9
    cm.add(m)


    n = cm.query(DEFAULT).filter_by(name='hallo').first()

    print ("\n\n")

    pprint (n.__dict__)


    o = cm.get(DEFAULT, 'hallo')


    print ("\n\n")

    pprint (o.__dict__)


    m = DEFAULT("other", "world")
    m.other = "ooo"
    cm.add(m)

    print ("\n\n")
    pprint (cm.get(DEFAULT, 'other').__dict__)


    cm.info()

    """


    cm.info()
    # print(cm.list(VM))
    """

if __name__ == "__main__":
    main()
