

FROM    ubuntu:14.04
MAINTAINER laszewski@gmail.com

RUN apt-get update && apt-get install -y git
RUN apt-get install -y python python-dev python-distribute python-pip

RUN pip install --upgrade pip
RUN pip --version

RUN mkdir $HOME/.cloudmesh
RUN mkdir -p $HOME/github/cloudmesh

WORKDIR $HOME/github/cloudmesh

RUN git clone https://github.com/cloudmesh/base.git
RUN git clone https://github.com/cloudmesh/client.git

WORKDIR $HOME/github/cloudmesh/base

RUN pwd
RUN pip install -r requirements.txt && \
    pip install .

WORKDIR $HOME/github/cloudmesh/client

RUN pwd
RUN pip install -r requirements.txt && \
    pip install .

# RUN ln -s `pwd` $(dirname `which python`)/../lib/python2.7/site-packages/cloudmesh_client

RUN nosetests -v --nocapture tests/test_model.py
RUN nosetests -v --nocapture tests/test_pass.py
RUN nosetests -v --nocapture tests/test_configdict.py
RUN nosetests -v --nocapture tests/test_shell.py
RUN nosetests -v --nocapture tests/test_tables.py
RUN nosetests -v --nocapture tests/test_default.py
RUN nosetests -v --nocapture tests/test_flatdict.py

RUN pip install -r requirements-doc.txt
RUN make doc
RUN cm help
