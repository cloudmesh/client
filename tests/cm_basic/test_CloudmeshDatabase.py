""" run with

python setup.py install; nosetests -v --nocapture tests//cm_basic/test_CloudmeshDatabase.py:Test_CloudmeshDatabase.test_001

nosetests -v --nocapture tests/cm_basic/test_CloudmeshDatabase.py

or

nosetests -v tests/cm_basic/test_CloudmeshDatabase.py

"""
import os

from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.util import HEADING
from cloudmesh_client.util import banner
from cloudmesh_client.cloud.list import List
from pprint import pprint
from cloudmesh_client.db.model import database, table, tablenames, \
    FLAVOR, DEFAULT, KEY, IMAGE, VM, GROUP, RESERVATION
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from pprint import pprint

class Test_CloudmeshDatabase:

    def setup(self):

        pass

    def tearDown(self):
        pass

    def test_001_query(self):
        """testing cm list --cloud ... default"""
        HEADING()
        cm = CloudmeshDatabase(user="gregor")
        m = DEFAULT("hallo", "world")
        cm.add(m)

        n = cm.query(DEFAULT).filter_by(name='hallo').first()

        print (n.__dict__)

        #assert n.__dict__["name"] == 'hallo'
        #assert n.__dict__["value"] == 'world'

        pprint(n.__dict__)

    def test_002_find_first(self):
        """testing cm list --cloud ... default"""
        HEADING()
        cm = CloudmeshDatabase(user="gregor")
        m = DEFAULT("hallo", "world")

        n = cm.find("default", scope="first", name='hallo')
        first = n.keys()[0]
        pprint (n)

        assert n["name"] == 'hallo'
        assert n["value"] == 'world'

    def test_002_find_all(self):
        """testing cm list --cloud ... default"""
        HEADING()
        cm = CloudmeshDatabase(user="gregor")
        m = DEFAULT("hallo", "world")

        n = cm.find("default", scope="all", name='hallo')
        print(n.keys())
        assert (len(n.keys()) > 0)

    def test_003_find_filter(self):
        """testing cm list --cloud ... default"""
        HEADING()
        cm = CloudmeshDatabase(user="gregor")
        m = DEFAULT("hallo", "world")

        n = cm.find("default",
                    scope="all",
                    name='hallo')
        print(n.keys())
        assert (len(n.keys()) > 0)
