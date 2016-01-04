FROM python:2.7
ADD . /code
WORKDIR /code

RUN git clone https://github.com/cloudmesh/base.git
RUN git clone https://github.com/cloudmesh/client.git
RUN git clone https://github.com/cloudmesh/portal.git

RUN cd /code/base/
RUN pip install -r requirements.txt
RUN python setup.py install

RUN cd /code/client/
RUN pip install -r requirements.txt
RUN python setup.py install

