
FROM    ubuntu:14.04
MAINTAINER laszewski@gmail.com

### update system
RUN apt-get update

### install depencencies
RUN apt-get install -y \
  git python python-dev python-distribute python-pip libjpeg-dev \
&& pip install --upgrade pip

### prepare cloudmesh directories
RUN mkdir -p $HOME/.cloudmesh

### cloudmesh/client
ADD . $HOME/cloudmesh_client
WORKDIR $HOME/cloudmesh_client
RUN pip install -r requirements.txt \
&&  pip install . \
&&  nosetests -v --nocapture \
      tests/test_model.py \
      tests/test_pass.py \
      tests/test_configdict.py \
      tests/test_shell.py \
      tests/test_tables.py \
      tests/test_default.py \
      tests/test_flatdict.py

