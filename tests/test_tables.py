""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_base.util import HEADING


class Test_tables:

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_dummy(self):
        HEADING()
        assert True
