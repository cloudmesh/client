""" run with

python setup.py install; nosetests -v --nocapture tests/cm_basic/test_model.py:Test_model.test_001

nosetests -v --nocapture tests/cm_basic/test_model.py

or

nosetests -v tests/cm_basic/test_model.py

"""
from __future__ import print_function

from pprint import pprint

from cloudmesh_client import CloudmeshDatabase
from cloudmesh_client.common.Printer import Printer
from cloudmesh_client.common.util import HEADING


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

    def test_003(self):
        HEADING("table info")
        d = self.cm.info()

        print(Printer.write(d))
        assert 'default' in str(d)
