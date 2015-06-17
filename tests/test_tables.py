""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_base.util import HEADING


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
        self.d = {""} # put your dict here, may be generated than you can use as self.d
        pass

    def tearDown(self):
        pass

    def test_dummy(self):
        HEADING()
        assert True

    def test_001_yaml(self):
        HEADING()
        assert False

    def test_002_json(self):
        HEADING()
        assert False

    def test_003_table(self):
        HEADING()
        assert False

    def test_004_dict(self):
        HEADING()
        assert False

    def test_005_csv(self):
        HEADING()
        assert False


