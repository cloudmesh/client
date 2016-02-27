""" run with

python setup.py install; nosetests -v --nocapture tests//cm_basic/test_model.py:Test_model.test_001

nosetests -v --nocapture tests/cm_basic/test_model.py

or

nosetests -v tests/cm_basic/test_model.py

"""
from __future__ import print_function

from pprint import pprint

from cloudmesh_client.util import HEADING
import cloudmesh_client.db
import cloudmesh_client.db.model


class Test_model:
    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        HEADING()
        pprint(cloudmesh_client.db.tables())
        assert True

    def test_002(self):
        HEADING()
        print(cloudmesh_client.db.tablenames())
        assert True

    def test_003(self):
        HEADING()
        for name in cloudmesh_client.db.tablenames():
            print(cloudmesh_client.db.table(name))
        assert True
