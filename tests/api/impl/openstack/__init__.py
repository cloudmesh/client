from cloudmesh_client.api.impl.openstack import OpenstackProvider, OpenstackNode

from nose.tools import nottest

def test_make_provider():
    return OpenstackProvider()

def test_make_node():
    return OpenstackNode(model=None, provider=None)

@nottest
def test_boot():
    p = test_make_provider()
    node = p.boot()
    print node


if __name__ == '__main__':
    test_boot()