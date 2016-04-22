class DictDB(dict):
    """

    Implements a persistent dictionary using sqlite

    Usage:

        element = {"name":, "abc",
                    "address": "here",
                    "email": "abc@example.com"}

        The name in the dict is identifies where to store it.

        d = PersistentData(os.path.join("~", ".cloudmesh/cloudmesh.db"))

        d.add(element)

        d.delete("name": "abc")
            # deletes all elements from the db where ethe name is matching abc

        d.json
            # exports to json

        d.yaml
            # exports a yaml as a string

        d.get("name": "abc")
            gets the first match

        d.find("name": "abc")
            finds the first match


    """

    def __init__(self, filename, d=None, attributes=None):
        """
        initializes the dict database

        :param filename: filename where to store the database. The name can include ~.
        :param d: an optional dict that is provided for initialization. If the elements
                  are already in the database they will be overwritten with the new dict.
                  Typically we initialize without a dict.
        :param attributes: An optional list of attributes to be passed
        """
        pass

    def attributes(self, attribute_names):
        """
        defines the attributes that each record can have. If a database has previously
        defined and new attributes are added the database records are updated.

        :param attribute_names: The attribute names
        """
        pass

    def add(self, d):
        """
        adds the dict to the database. The attribute "name" is used to define a
        unique name for the object in the database

        :param d: the dict that at minimum must contain a name attribute
        """
        pass

    def delete(self, operator="and", **kwargs):
        """
        deletes all elements in that match the query formulated by kwargs and the operator
        operators that are allowed are = and, or

        :param kwargs: the attributes that we look for
        :param operator: the operator and / or
        """
        pass

    def find(self, operator="and", **kwargs):
        """
        finds all elements in that match the query formulated by kwargs and the operator
        operators that are allowed are = and, or

        :param kwargs: the attributes that we look for
        :param operator: the operator and / or
        """
        pass

    def get(self, operator="and", **kwargs):
        """
        finds the first elements in that match the query formulated by kwargs and the operator
        operators that are allowed are = and, or

        :param kwargs: the attributes that we look for
        :param operator: the operator and / or
        """
        pass

    @property
    def json(self):
        """
        :return: the json object of the database
        """
        return None

    @property
    def yaml(self):
        """
        :return: a yaml string of the database
        """
        return None

    def backup(self, filename=None):
        """
        backs up the current database. If the filename is omitted, the backup will be
        created in the same directory as the database with the postfix .bak.#
        where # is the largest number that has not yet been assigned. For example.,
        lets assume a backup exists with the name file.bak.9, than the next higher
        number is used (e.g. 10) and the backup file file.back.10 is used.

        :param filename: the backup filename.
        :return:
        """
        pass
