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
        """test if cloudmesh.yaml is loaded"""
        HEADING()
        d = ConfigDict("cloudmesh.yaml",
                       load_order=["cloudmesh_etc"],
                       verbose=True)

        assert d["cloudmesh"]["profile"]["firstname"] == "TBD"

        try:
            d = ConfigDict("cloudmesh.yam",
                           load_order=["cloudmesh_etc"],
                           verbose=True)
            print("the file cloudmesh.yam should not exists")
            assert False
        except Exception, e:
            assert str(e).startswith("could not find")

    def test_002_set(self):
        """testing to set a value in the dict"""
        HEADING()
        # copy the cloudmesh_etc/cloudmesh.yaml file to /tmp
        d = ConfigDict("cloudmesh.yaml",
                       load_order=["/tmp"],
                       verbose=True)
        d["cloudmesh"]["profile"]["firstname"] = "Gregor"
        d.save()

        d = ConfigDict("cloudmesh.yaml",
                       load_order=["/tmp"],
                       verbose=True)
        assert d["cloudmesh"]["profile"]["firstname"] == "Gregor"


    def test_003_json(self):
        """test if json is produced"""
        HEADING()
        d = ConfigDict("cloudmesh.yaml",
                       load_order=["cloudmesh_etc"],
                       verbose=True)

        assert d.json.startswith('{')

        try:
            assert  not isinstance(d.json, str)
            print ("json should be string")
            assert False
        except Exception, e:
            assert isinstance(d.json, str)

    def test_004_yaml(self):
        """test if yaml is produced"""
        HEADING()
        d = ConfigDict("cloudmesh.yaml",
                       load_order=["cloudmesh_etc"],
                       verbose=True)
        result = d.yaml

        try:
            assert result.startswith("meta")
        except Exception, e:
            print ("not valid yaml file.")
            assert False




    def test_005_info(self):
        """test if some general information is there"""
        # read yaml file from file
        #  check if d.filename is the same as the filename we have
        HEADING()
        name = "cloudmesh.yaml"
        d = ConfigDict("cloudmesh.yaml",
                       load_order=["cloudmesh_etc"],
                       verbose=True)
        assert d.filename == name



"""	def main():
    d = ConfigDict("cmd3.yaml")
    print (d, end='')
    d.info()

    print (d["meta"])
    print (d["meta.kind"])
    print (d["meta"]["kind"])

    # this does not yet work
    print (d)
    d.save()

    import os
    os.system("cat cmd3.yaml")

    print(d.json)
    print(d.filename)

if __name__ == "__main__":
    main()
"""
