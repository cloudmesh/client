""" run with

nosetests -v --nocapture tests/test_configdict.py

or

nosetests -v tests/test_configdict.py

"""
from __future__ import print_function
from cloudmesh_base.util import HEADING
from cloudmesh_common.ConfigDict import ConfigDict

class Test_pass:

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001_read(self):
        HEADING()
        d = ConfigDict("cloudmesh_etc/cloudmesh.yaml")
        print (d.json())

        assert True
	
"""	def main():
    d = ConfigDict("cmd3.yaml")
    print (d, end='')
    d.info()

    print (d["meta"])
    print (d["meta.kind"])
    print (d["meta"]["kind"])

    # this does not yet work
    d.data["meta"]["test"] = 'Gregor'
    print (d)
    d.save()

    import os
    os.system("cat cmd3.yaml")

    print(d.json)
    print(d.filename)

if __name__ == "__main__":
    main()
"""
