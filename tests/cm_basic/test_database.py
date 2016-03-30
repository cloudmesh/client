# noinspection PyPep8
""" run with

python setup.py install; nosetests -v --nocapture tests/cm_basic/test_database.py:Test_database.test_001

nosetests -v --nocapture tests/cm_basic/test_database.py

or

nosetests -v tests/cm_basic/test_database.py

"""

from pprint import pprint

from cloudmesh_client.db import DEFAULT, COUNTER, VM_OPENSTACK
from cloudmesh_client.util import HEADING

from cloudmesh_client.db import CloudmeshDatabase


# noinspection PyMethodMayBeStatic,PyPep8Naming
class Test_database:

    cm = CloudmeshDatabase()


    def setup(self):
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass


    def test_000(self):
        HEADING("testing DEFAULT add")
        
        result = self.cm.info()
        print (result['username'])
        assert "var" in str(result)
        assert "VARCHAR" in str(result)

    def test_001(self):
        HEADING("testing DEFAULT add")
        
        m = DEFAULT("hallo", "world")
        self.cm.add(m)

        n = self.cm.query(DEFAULT).filter_by(name='hallo').first()

        print(n.__dict__)

        # assert n.__dict__["name"] == 'hallo'
        # assert n.__dict__["value"] == 'world'

        pprint(n.__dict__)

    def test_002(self):
        HEADING("testing list")
        
        m = DEFAULT("hallo", "world")

        n = self.cm.find("default", scope="first", name='hallo')
        first = list(n)[0]
        pprint(n)

        assert n["name"] == 'hallo'
        assert n["value"] == 'world'

    def test_003(self):
        HEADING("testing find")
        
        m = DEFAULT("hallo", "world")

        n = self.cm.find("default", scope="all", name='hallo')
        print(list(n))
        assert (len(list(n)) > 0)



    def test_004(self):
        

        self.cm.info()


        m = COUNTER("counter", 2)
        self.cm.add(m)

        o = self.cm.get(COUNTER, name='counter')

        print("OOO", o)

        self.cm.counter_set(name="counter", value=0)

        for i in range(0, 10):
            self.cm.counter_incr(name="counter")

        print(self.cm.counter_get(name="counter"))

        self.cm.info()
        c = self.cm.first(self.cm.all(COUNTER))
        print ("CCC", c)
        assert c["value"] == '10'


    def test_005(self):
        

        self.cm.info()


        m = COUNTER("counter", 2, user="gregor")
        self.cm.add(m)

        o = self.cm.get(COUNTER, name='counter', user="gregor")

        print("OOO", o)

        self.cm.counter_set(name="counter", user="gregor", value=0)

        for i in range(0, 10):
            self.cm.counter_incr(name="counter", user="gregor")

        print(self.cm.counter_get(name="counter", user="gregor"))

        self.cm.info()
        c = self.cm.first(self.cm.all(COUNTER))
        print ("CCC", c)
        assert c["value"] == '10'




"""
    def test_005(self):
        

        m = DEFAULT("newfield", "world")
        m.newfield__hhh = 13.9



        self.cm.add(m)


        n = self.cm.find("default", scope="first", name='newfield')

        pprint(n)


    def test_006(self):
        
        m = DEFAULT("other", "world")
        m.other = "ooo"
        self.cm.add(m)

        print("\n\n")
        pprint(self.cm.get(DEFAULT, other='other').__dict__)

"""