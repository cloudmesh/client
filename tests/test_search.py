""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_base.util import HEADING
import os


class Test_search:
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        """testing cm search with all the arguments"""
        HEADING()
        try:
            os.system("cm search flavor --order=name,disk name!=m1.tiny vcpus=[1-4]")
            assert False
        except Exception:
            assert True
