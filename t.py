#!/usr/bin/env python

import os

# os.system("python setup.py install")
# os.system("py.test --capture=no tests/cm_basic/test_cloud_model.py")
os.system("py.test --capture=no tests/cm_basic/test_database.py")
