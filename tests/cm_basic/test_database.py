# noinspection PyPep8
""" run with

python setup.py install; nosetests -v --nocapture tests/cm_basic/test_database.py:Test_database.test_001

nosetests -v --nocapture tests/cm_basic/test_database.py

or

nosetests -v tests/cm_basic/test_database.py

"""

from pprint import pprint

from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase
from cloudmesh_client.db.model import DEFAULT, COUNTER, VM_OPENSTACK
from cloudmesh_client.util import HEADING


# noinspection PyMethodMayBeStatic,PyPep8Naming
class Test_database:
    def setup(self):
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass


    def test_000(self):
        HEADING("testing DEFAULT add")
        cm = CloudmeshDatabase()
        result = cm.info()
        print (result['username'])
        assert "var" in str(result)
        assert "VARCHAR" in str(result)

    def test_001(self):
        HEADING("testing DEFAULT add")
        cm = CloudmeshDatabase()
        m = DEFAULT("hallo", "world")
        cm.add(m)

        n = cm.query(DEFAULT).filter_by(name='hallo').first()

        print(n.__dict__)

        # assert n.__dict__["name"] == 'hallo'
        # assert n.__dict__["value"] == 'world'

        pprint(n.__dict__)

    def test_002(self):
        HEADING("testing list")
        cm = CloudmeshDatabase()
        m = DEFAULT("hallo", "world")

        n = cm.find("default", scope="first", name='hallo')
        first = list(n)[0]
        pprint(n)

        assert n["name"] == 'hallo'
        assert n["value"] == 'world'

    def test_003(self):
        HEADING("testing find")
        cm = CloudmeshDatabase()
        m = DEFAULT("hallo", "world")

        n = cm.find("default", scope="all", name='hallo')
        print(list(n))
        assert (len(list(n)) > 0)


    def test_004(self):
        cm = CloudmeshDatabase(user="gregor")

        cm.info()


        m = COUNTER("counter", 2, user="gregor")
        cm.add(m)

        o = cm.get(COUNTER, name='counter', user="gregor")

        print("OOO", o)

        cm.counter_set(name="counter", user="gregor", value=0)

        for i in range(0, 10):
            cm.counter_incr(name="counter", user="gregor")

        print(cm.counter_get(name="counter", user="gregor"))

        cm.info()
        c = cm.first(cm.all(COUNTER))
        print ("CCC", c)
        assert c["value"] == '10'




"""
    def test_005(self):
        cm = CloudmeshDatabase()

        m = DEFAULT("newfield", "world")
        m.newfield__hhh = 13.9



        cm.add(m)


        n = cm.find("default", scope="first", name='newfield')

        pprint(n)


    def test_006(self):
        cm = CloudmeshDatabase()
        m = DEFAULT("other", "world")
        m.other = "ooo"
        cm.add(m)

        print("\n\n")
        pprint(cm.get(DEFAULT, other='other').__dict__)

"""