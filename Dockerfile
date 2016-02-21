
FROM    ubuntu:14.04
MAINTAINER laszewski@gmail.com

### update system
RUN apt-get update

### prepare system
RUN apt-get install libpng-dev -y
RUN apt-get install zlib1g-dev -y

### install python
RUN apt-get install -y \
    git python python-dev python-distribute python-pip libjpeg-dev
RUN pip install -U pip
RUN apt-get remove python-six -y


### prepare cloudmesh directories
RUN mkdir -p $HOME/.cloudmesh
ADD . $HOME/cloudmesh_client
WORKDIR $HOME/cloudmesh_client

### install requirements
RUN pip install -r requirements.txt 
RUN pip install -r requirements-doc.txt 
RUN pip install -r requirements-test.txt

### install cloudmesh
RUN python setup.py install

### run tests
RUN cm help
RUN nosetests -v --nocapture tests/cm_basic

### run cloudmesh
RUN cm

