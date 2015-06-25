Installation
============

Cloudmesh client is veriy easy to install. In contrast to previous
efforts we could simplify the instalation while we manage the database
locally by the user and not use LDAP or any other system as they are
difficult to install on Windows.

The instalation of cloudmesh is provided for

* Linux
* OSX
* Windows

For each of these operating systems we are provide specific
instalation instructions.

Prepare the system
------------------

OSX
^^^

On OSX we recommend that you use python 2.7.10. This version of python
is easy to install while downloading the dmg and installing it on the
system. You will still have access to the python version distributed
with the original OSX operating system.

To test out which version you have activated, you can use in the
commandline::

  python --version
  pip --version

They should show something similar to::

  Python 2.7.10
  pip 7.0.3

Oon OSX as well as the other operating systems we **require** you to
use virtualenv. First you need to find which version of python you
use. You can say::

  which python

It will give you the path of the python interpreter. Let us assume the
interpreter was found in `/usr/local/bin/python`.  Next you can create
a virtual ENV with::

  virtualenv -p /user/local/bin/python ~/ENV

You will need to activate the virtualenv::

  source ~/ENV/bin/activate

If sucessfull, your terminal will have (ENV) as prefix to the prompt::

  (ENV)machinename:dirname user$

As OSX comes with older versions of pip at this time, it is important
that you first prepare the environment before you install cloudmesh
client. To do so please isseue the following commands::

   pip install pip -U
   easy_install readline
   easy_install pycrypto
   pip install urllib3


It is recommended that you test the version of the python interpreter
and pip again::
   
   pip --version

pip 7.0.3
   
::

   python --version


Python 2.7.10



Windows
^^^^^^^

Special instructions for Windows are available in the Section :ref:`windows-install`

Pip
---

Not yet available

Source
------

User and Contributor
^^^^^^^^^^^^^^^^^^^^

::

   mkdir github/cloudmesh
   cd github/cloudmesh
   git clone https://github.com/cloudmesh/base.git 
   git clone https://github.com/cloudmesh/cmd3.git  
   git clone https://github.com/cloudmesh/client.git   
   cd base
   git checkout sh
   python setup.py install
   cd ../cmd3
   git checkout sh
   python setup.py install
   cd ../client
   python setup.py install

Developer with ssh access to git reporsitory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   mkdir github/cloudmesh
   cd github/cloudmesh
   git clone git@github.com:cloudmesh/base.git   
   git clone git@github.com:cloudmesh/cmd3.git
   git clone git@github.com:cloudmesh/client.git
   cd base
   git checkout sh
   python setup.py install
   cd ../cmd3
   git checkout sh
   python setup.py install
   cd ../client
   python setup.py install


Testing
-------

::

   pip install tox

in the source dir say::

  tox

Nose tests can be started with::

  nosetests

  
