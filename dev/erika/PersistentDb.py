__author__ = 'ERIKA'

import sqlite3 as sqlite
import json
import os
import os.path

# TODO: change + string to remove + but use a .format( ) which is more like python3
# you can do
# data = {'tablename': self.table_name, ....}
# ".... {tablename} .... ".format(**data)
# or a bit less readable
# " .... {:} .....".format(self.table_name, ...) ....

class PersistentDb:
    table_name = ""

    def __init__(self, filename, d=None, **attributes):
        if '~' in filename:
            filename = os.path.expanduser(filename)
        self.con = sqlite.connect(filename)
        self.table_name = d
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE if not exists " + d + " (" + ','.join("%s %s" % (key, value) for (key, value) in
                                                                             attributes.items()) + ")")

    def add_attributes(self, **attribute_names):
        """
        defines the attributes that each record can have. If a database was previously defined and
        new attributes are added the database records are updated.
        :param attribute_names: The attribute names
        :param d: The dictionary/table name
        """
        existing_attribute_names = list(map(lambda x: x[0], self.con.execute(
            "SELECT * from " + self.table_name).description))
        list_new_attributes = set(existing_attribute_names).union(
            attribute_names.keys()) - set(existing_attribute_names)
        for col in list_new_attributes:
            self.cur.execute("ALTER TABLE " + self.table_name +
                             " ADD COLUMN %s %s" % (col, attribute_names[col]))

    def add_attribute(self, name, type):
        """
        Alters the table with an additional column
        :param name: Name of the attribute
        :param type: Type of the attribute
        """
        self.cur.execute("ALTER TABLE %s ADD COLUMN %s %s" %
                         (self.table_name, name, type))

    def get_attribute_type(self, name):
        """
        This returns the data type of the attribute
        :param name: Name of the attribute
        :return: The type of the attribute
        """
        result = self.cur.execute(
            'PRAGMA table_info(%s)' % self.table_name).fetchall()
        for res in result:
            if res[1] == name:
                return res[2]

    def add(self, name, **kwargs):
        """
        adds the dict to the database. The attribute "name" is used to define a
        unique name for the object in the database
        :param record: the dict that at minimum must contain a name attribute
        """

        kwargs['name'] = name
        column_names = ', '.join(kwargs.keys())
        placeholders = ', '.join('?' * len(kwargs.values()))
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(
            self.table_name, column_names, placeholders)
        self.cur.execute(sql, tuple(kwargs.values()))
        self.con.commit()

    def delete(self, operator, **kwargs):
        """
        deletes all elements in that match the query formulated by kwargs and the operator
        operators that are allowed are = and, or
        :param kwargs: the attributes that we look for
        :param operator: the operator and / or
        """
        self.cur.execute("DELETE FROM person WHERE " + (" %s " % operator).join("%s=%r" % (key, value) for (key, value)
                                                                                in kwargs.items()))
        self.con.commit()

    def find(self, operator, **kwargs):
        """
        Finds all the elements that match the query formulated by kwargs and the operator.
        :param operator: The operators and / or
        :param kwargs: The attributes that we look for
        """
        result = self.cur.execute("SELECT * FROM person WHERE " + (" %s " % operator).join("%s=%r" % (key, value) for
                                                                                           (key, value) in kwargs.items()))
        recs_list = result.fetchall()
        print recs_list

    def get(self, operator, **kwargs):
        """
        Finds the first element that match the query formulated by kwargs and the operator
        :param operator: The operators and / or
        :param kwargs: The attributes that we look for
        """
        result = self.cur.execute("SELECT * FROM person WHERE " + (" %s " % operator).join("%s=%r" % (key, value) for
                                                                                           (key, value) in kwargs.items()))
        rec = result.fetchone()
        print rec

    @property
    def json(self):
        """
        :return: The json object of the database
        """
        self.con.row_factory = sqlite.Row  # Use the dictionary cursor to fetch data by column names
        result = self.con.cursor().execute("SELECT * FROM person ").fetchall()
        return json.dumps([dict(row) for row in result])

    def backup(self, file_name):
        """
        backs up the current database. If the filename is omitted, the backup will be
        created in the same directory as the database with the postfix .bak.#
        where # is the largest number that has not yet been assigned. For example.,
        lets assume a backup exists with the name file.bak.9, than the next higher
        number is used (e.g. 10) and the backup file file.back.10 is used.
        :param file_name: the backup filename
        """
        backup_file_no = len([name for name in os.listdir(
            '.') if os.path.isfile(name) and (file_name in name)]) + 1
        backup_file = open(file_name + ".bak." + str(backup_file_no), "w")
        backup_file.write(self.json)
        backup_file.close()

# TODO: somehow we need also in windows something like ~/.cloudmesh/client.db, see if you can use path_expand in base
# TODO: if db is not there it should be created

# TODO: can you create larger example with https://pypi.python.org/pypi/fake-factory

pd = PersistentDb("F:/python/sqliteMultiDimensional/testDb.db", "person",
                  NAME='VARCHAR NOT NULL', ADDRESS='VARCHAR', EMAIL='VARCHAR', OCCUPATION='IT')
pd.add("abc", address="here", email="abcexample.com", occupation="IT")
pd.add("abc", address="idk")


# Delete a record
#pd.delete('and', name='abc', address='here')

# Find
#pd.find("", name='abc')

# Get the first record
#pd.get('and', name='erika', address='IN')

# print pd.json

# pd.backup("new_backup")

pd.add_attributes(GENDER='VARCHAR')

print pd.get_attribute_type('NAME')
