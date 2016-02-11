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

.. warning:: The instalation with pip is not yet working at this
	     time. Please use the instalation from source

Users can install the cloudmesh client via pip

.. prompt:: bash

    pip install cloudmesh_client


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
   git clone https://github.com/cloudmesh/base.git 
   git clone https://github.com/cloudmesh/client.git
   cd base
   python setup.py install
   cd ../client
   python setup.py install


Updating an existing source distribution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

During the development phase of cloudmesh you may need to update the
code from source, as cloudmesh client uses three different
repositories please do not forget to update them accordingly

.. prompt:: bash
  
   export CLOUDMESH_HOME=$HOME/github/cloudmesh
   cd $CLOUDMESH_HOME/base
   git pull
   python setup.py install
   cd $CLOUDMESH_HOME/client
   python setup.py install


