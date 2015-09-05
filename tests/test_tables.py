""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_base.util import HEADING

from cloudmesh_client.common.tables import dict_printer
from pprint import pprint

class Test_tables:

    """
    define tests for dict printer so you test

    yaml
    json
    table
    csv
    dict

    printing

    """
    def setup(self):
        self.d = {
            "a:" : {
                "id": "a",
                "x": 1,
                "y": 2,
                },
            "b:" : {
                "id": "b",
                "x": 3,
                "y": 4,
                },
            }

    def tearDown(self):
        pass

    def test_001_yaml(self):
        """dict_printer of a yaml object"""
        HEADING()
        output = dict_printer(self.d, order=None, header=None, output="yaml", sort_keys=True)
        print(output)
        assert ":" in output

    def test_002_json(self):
        """dict_printer of a json object"""
        HEADING()
        output = dict_printer(self.d, order=None, header=None, output="json", sort_keys=True)
        print(output)
        assert "{" in output

    def test_003_table(self):
        """dict_printer of a table object"""
        HEADING()
        output = dict_printer(self.d, order=None, header=None, output="table", sort_keys=True)
        print(output)
        assert "id" in str(output)

    def test_004_dict(self):
        """dict_printer of a dict object"""
        HEADING()
        output = dict(dict_printer(self.d, order=None, header=None, output="dict", sort_keys=True))
        pprint(output)
        assert "id" in str(output)

    def test_005_csv(self):
        """dict_printer of a csv object"""
        HEADING()
        output = dict_printer(self.d, order=None, header=None, output="csv", sort_keys=True)
        print(output)
        assert "id" in str(output)


