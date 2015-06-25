""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_base.util import HEADING


class Test_search:
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """test setting and getting default values"""
        HEADING()
        assert True
