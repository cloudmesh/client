""" run with

python setup.py install; nosetests -v --nocapture tests/cm_basic/test_model.py:Test_model.test_001

nosetests -v --nocapture tests/cm_basic/test_model.py

or

nosetests -v tests/cm_basic/test_model.py

"""
from __future__ import print_function

from pprint import pprint

from cloudmesh_client.util import HEADING
from cloudmesh_client import CloudmeshDatabase

# noinspection PyMethodMayBeStatic,PyPep8Naming
class Test_model:

    cm = CloudmeshDatabase()

    def setup(self):
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    # noinspection PyMethodMayBeStatic
    def test_001(self):
        HEADING("cm.tables")
        pprint(self.cm.tables)
        assert True

    def test_002(self):
        HEADING("loop over tablenames")
        for t in self.cm.tables:
            print(t.__tablename__)
        assert "DEFAULT" in str(self.cm.tables)
