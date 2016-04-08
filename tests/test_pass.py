""" run with

nosetests -v --nocapture

or

nosetests -v

"""

from cloudmesh_client.common.util import HEADING


# noinspection PyMethodMayBeStatic,PyPep8Naming
class Test_pass:
    def setup(self):
        pass

    # noinspection PyPep8Naming
    def tearDown(self):
        pass

    def test_dummy(self):
        HEADING()
        assert True
