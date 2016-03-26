# noinspection PyPep8
""" run with

python setup.py install; nosetests -v --nocapture tests/cm_basic/test_CloudmeshDatabase.py:Test_CloudmeshDatabase.test_001

nosetests -v --nocapture tests/cm_basic/test_CloudmeshDatabase.py

or

nosetests -v tests/cm_basic/test_CloudmeshDatabase.py

"""

from pprint import pprint

from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.db.model import DEFAULT
from cloudmesh_client.util import HEADING


# noinspection PyMethodMayBeStatic,PyPep8Naming
class Test_CloudmeshDatabase:
    def setup(self):
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_001_query(self):
        HEADING("testing DEFAULT add")
        cm = CloudmeshDatabase(user="gregor")
        m = DEFAULT("hallo", "world")
        cm.add(m)

        n = cm.query(DEFAULT).filter_by(name='hallo').first()

        print(n.__dict__)

        # assert n.__dict__["name"] == 'hallo'
        # assert n.__dict__["value"] == 'world'

        pprint(n.__dict__)

    def test_002_find_first(self):
        HEADING("testing list")
        cm = CloudmeshDatabase(user="gregor")
        m = DEFAULT("hallo", "world")

        n = cm.find("default", scope="first", name='hallo')
        first = list(n)[0]
        pprint(n)

        assert n["name"] == 'hallo'
        assert n["value"] == 'world'

    def test_002_find_all(self):
        HEADING("testing find")
        cm = CloudmeshDatabase(user="gregor")
        m = DEFAULT("hallo", "world")

        n = cm.find("default", scope="all", name='hallo')
        print(list(n))
        assert (len(list(n)) > 0)
