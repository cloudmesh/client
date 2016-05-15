from __future__ import print_function
from cloudmesh_client.extend.my import my_i, my_c
from cloudmesh_client.common.DynamicClass import DynamicClass

def z_a(args):
    print ("z_a", args)

def z_c(cls, args):
    print ("z_c", args)

def z_b(cls, args):
    print ("z_b", args)


class A(DynamicClass):
    pass

a = A()
a.add_instance_method(my_i)
a.my_i("i am my_i")

A.add_classmethod(my_c)
a.my_c("i am my_c")

A.load_classmethod("cloudmesh_client.extend.my.my_cc")
a.my_cc("i am my_cc")

b = A()

b.my_cc("i am my_cc")

A.z_b = z_b

A().z_b("i am z_b")

A.load_classmethod("cloudmesh_client.extend.my.my_ccc")
A().my_ccc("YOURS")
