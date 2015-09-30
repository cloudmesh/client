Installation
============

We assume that you have prepared your system on which yo like to
install the cloudmesh client. We recommend that you use python 2.7.10,
pip 7.1.2 and have virtualenv installed. Furthermore we recommend
that on Linux systems you have readline installed as it is a
convenient tool for command line manipulation.

In the next sections we will walk you through a setup that has been
proven to work for developers and users and is very easy to replicate.


Cloudmesh Client via pip
----------------------------------

Users can install the cloudmesh client via pip::

    pip install cloudmesh_client


Cloudmesh Installation from Source
-----------------------------------

Developers that wish to contribute to the source can obtein the code from
github. We assume that we conduct a source code install into the directory::
  
  ~/github/cloudmesh

If you like to use a different directory, that is also possible, but
the instructions we provide here assumes are targeted towards this
base directory.

Preparing the Virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Firts we set up a virtual environment based on the environment we are
on:

Linux::

  virtualenv ~/ENV
  source ~/ENV/bin/activate
   
OSX::

  virtualenv -p /usr/local/bin/python
  source ~/ENV/bin/activate
   
Windows::

  virtualenv $HOME/ENV
  source $HOME/bin/activate
  
.. todo:: Gurav. there was an error here as it talked about cygwin,
	  but we use here powershell, can you verify if this works. I
	  think i myself are using this without virtualenv
   

User and Contributor
^^^^^^^^^^^^^^^^^^^^
If you are a user and external contributor and do not have write access to
the repositories you can install the code from source as follows::

   mkdir -p github/cloudmesh
   cd github/cloudmesh
   git clone https://github.com/cloudmesh/base.git 
   git clone https://github.com/cloudmesh/client.git
   cd base
   python setup.py install
   cd ../client
   python setup.py install

Developer with ssh access to git repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are a developer and have access to all repositories, you can
use the following commands to get the source code. However if you miss
access to one of the directories, please replace it with an https
based git clone as described in the previous section.

::

   mkdir -p github/cloudmesh
   cd github/cloudmesh
   git clone git@github.com:cloudmesh/base.git   
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

   cd $HOME/github/cloudmesh
   cd base
   git pull
   python setup.py install
   cd ../client
   python setup.py install



.. todo:: It may be advantageous to create a CLOUDMESH_HOME variable
	  and install the source into it. THis way we can use
	  CLOUDMESH_HOME instead of HOME and are independent from the
	  directory. However at this time this is not needed as it
	  complicates the setup. As we all develop in the same tree
	  its easier for now to go without the CLOUDMESH_HOME. Also
	  setting this up on windows is yet another complication we do
	  not need.
	  

Testing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. todo:: This section is incomplete and we need to make sure that tox
	  works. We also need to explain how travis works and how we
	  can run nosetests locally


For now we do not assume that you need to run any tests after you
install the source. We will address deployment tests later.

::

   pip install tox

in the source dir say::

  tox

Nose tests can be started with::

  nosetests

  
