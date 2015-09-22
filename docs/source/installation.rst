Installation
============


Cloudmesh Instalation from Source
----------------------------------

In the following we assume that we will install the source code in::
  
  ~/github/cloudmesh

Preparing the Virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Linux::

  virtualenv ~/ENV
  source ~/ENV/bin/activate
   
OSX::

  virtualenv -p /usr/local/bin/python
  source ~/ENV/bin/activate
   
Windows::

  virtualenv ~/ENV
  source /cygdrive/c/home/$USER/ENV/Scripts/activate
   
.. note:: in case you have multiple users on the machine you need to
	  replace the * with your username
   

User and Contributor
^^^^^^^^^^^^^^^^^^^^
If you are a user and external contributer and do not have write access to
the repositories you can install the code from source as follows::

   mkdir -p github/cloudmesh
   cd github/cloudmesh
   git clone https://github.com/cloudmesh/base.git 
   git clone https://github.com/cloudmesh/client.git
   cd base
   python setup.py install
   cd ../client
   python setup.py install

Developer with ssh access to git reporsitory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are a developer and have access to all repositories, you can
use the following commands to get the source code. However if you miss
access to one of the directories, please replace it with an https
based git clone as described in the previous section.

::

   mkdir -p github/cloudmesh
   cd github/cloudmesh
   git clone git@github.com:cloudmesh/base.git   
   git clone git@github.com:cloudmesh/cmd3.git
   git clone git@github.com:cloudmesh/client.git
   cd base
   python setup.py install
   cd ../client
   python setup.py install


Updating an existing source distribution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

During the development phase of cloudmesh you may need to update the
code from source, as cloudmesh client uses three different
repositories please do not forget to update them accordingly::

   cd github/cloudmesh
   cd base
   git pull
   python setup.py install
   cd ../client
   python setup.py install



Testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   pip install tox

in the source dir say::

  tox

Nose tests can be started with::

  nosetests

  
