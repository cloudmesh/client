""" run with

python setup.py install; nosetests -v --nocapture tests/cm_basic/test_model.py:Test_model.test_001

nosetests -v --nocapture tests/cm_basic/test_model.py

or

nosetests -v tests/cm_basic/test_model.py

"""
from __future__ import print_function

from pprint import pprint

from cloudmesh_client.util import HEADING
import cloudmesh_client.db
from cloudmesh_client.db import database

# noinspection PyMethodMayBeStatic,PyPep8Naming
class Test_model:

    db = database()

    def setup(self):
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    # noinspection PyMethodMayBeStatic
    def test_001(self):
        HEADING("db.tables")
        pprint(self.db.tables())
        assert True

    def test_002(self):
        HEADING("db.tablenames")
        print(self.db.tablenames())
        assert True

    def test_003(self):
        HEADING("loop over tablenames")
        for name in self.db.tablenames():
            print(self.db.table(name))
        assert True
