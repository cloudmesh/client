import importlib

class DynamicClass(object):

    def add_instance_method(self, f):
        setattr(self, f.__name__, f)

    @classmethod
    def add_classmethod(cls, f):
        setattr(cls, f.__name__, f)

    def load_instancemethod(self, location):
        module_name, class_name = location.rsplit(".", 1)
        f = getattr(importlib.import_module(module_name), class_name)
        self.add_instance_method(f)

    @classmethod
    def load_classmethod(cls, location):
        module_name, class_name = location.rsplit(".", 1)
        f = getattr(importlib.import_module(module_name), class_name)
        cls.add_classmethod(f)