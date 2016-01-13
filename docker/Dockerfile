FROM ubuntu:latest
FROM python:2.7
ADD . /code
WORKDIR /code

RUN pwd

RUN git clone https://github.com/cloudmesh/base.git
RUN git clone https://github.com/cloudmesh/client.git
RUN git clone https://github.com/cloudmesh/portal.git

WORKDIR /code/base
RUN ls
RUN pip install -r requirements.txt
RUN python setup.py install

WORKDIR /code/client
RUN ls
RUN pip install -r requirements.txt
RUN python setup.py install

