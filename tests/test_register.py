""" run with

nosetests -v --nocapture tests/test_register.py

or

nosetests -v tests/test_register.py

"""

from cloudmesh_base.util import HEADING
import os


class Test_register:
    """
        tests for india only
    """
    def setup(self):
        os.system("python setup.py install")

    def test_001(self):
        """testing cm register india
        """
        HEADING()
        try:
            os.system("cm register india")

        except Exception:
            assert False
    def test_002(self):
        """testing cm register india --force
        """
        HEADING()
        try:
            os.system("cm register india --force")
        except Exception:
            assert False

    def test_003(self):
        """testing cm register india --force
        """
        HEADING()
        try:
            os.system("cm register random1 --force")
            assert False
        except Exception:
            assert True
    def test_004(self):
        """testing cm register india --force
        """
        HEADING()
        try:
            os.system("cm register india --foo")
            assert False
        except Exception:
            assert True

    def test_005(self):
        """
        testing cm register CLOUD CERT
        """
        HEADING()
        try:
            os.system("cm register india .cloudmesh/clouds/juno/cacert.pem")
            assert True
        except Exception:
            assert False

    def test_006(self):
        """
        testing cm register CLOUD CERT
        """
        HEADING()
        try:
            os.system("cm register india .cloudmesh/clouds/juno/d/cacert.pem")
            assert False
        except Exception:
            assert True

    def test_007(self):
        """
        testing cm register CLOUD CERT
        """
        HEADING()
        try:
            os.system("cm register india .cloudmesh/clouds/juno/wrong.pem")
            assert False
        except Exception:
            assert True


