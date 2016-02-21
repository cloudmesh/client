Installation
============

We assume that you have prepared your system (see Section
:ref:`_my-reference-label`) on which you like to install the cloudmesh
client. We recommend that you use python 2.7.10, pip 7.1.2 and use
virtualenv. Furthermore we recommend that on Linux systems you have
readline installed as it is a convenient tool for command line
manipulation. In the next sections we will walk you through a setup
that has been proven to work for developers and users and is very easy
to replicate.


Install Cloudmesh Client via pip
----------------------------------

.. warning:: at this time we recommend you use the source install and not
the pip install

Users can install the cloudmesh client via pip

.. prompt:: bash

   cd ~
   pip install cloudmesh_client

Please note that the directory in which you call pip install does not have a
directory called cloudmesh_client THis may prevent pip from working properly.


Cloudmesh Installation from Source
-----------------------------------

Developers that wish to contribute to the source can obtain the code from
github. We assume that we conduct a source code install into the directory::
  
  ~/github/cloudmesh

If you like to use a different directory, that is also possible, but
the instructions we provide here assumes are targeted towards this
base directory.

Please use the following commands

.. prompt:: bash

   mkdir -p github/cloudmesh
   cd github/cloudmesh
   git clone https://github.com/cloudmesh/client.git
   cd client
   python setup.py install


Updating an existing source distribution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

During the development phase of cloudmesh you may need to update the
code from source, as cloudmesh client uses three different
repositories please do not forget to update them accordingly

.. prompt:: bash
  
   export CLOUDMESH_HOME=$HOME/github/cloudmesh
   cd $CLOUDMESH_HOME/client
   git pull
   python setup.py install


