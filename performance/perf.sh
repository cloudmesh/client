#! /bin/sh
source ~/ENV2/bin/activate
python --version
pip --version
python setup.py install
cm performance/perf.cm

source ~/ENV3/bin/activate
python --version
pip --version
python setup.py install
cm performance/perf.cm


