# build the cm-docker with
# start docker
# eval "$(docker-machine env default)"
#
# docker build -t cm-docker .
#
# docker run -ti cm-docker bash
# docker run -ti -v ~/.ssh:/root/.ssh -v ~/.cloudmesh:/root/.cloudmesh cm-docker bash
# docker cp ~/.ssh <DOCKERID>:/root/.ssh

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

### setup ssh
RUN mkdir -p /root/.ssh

### prepare cloudmesh directories
RUN mkdir -p .cloudmesh
ADD . cloudmesh_client
WORKDIR cloudmesh_client

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

