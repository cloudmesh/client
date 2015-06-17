Installation
============

Prepare the system
------------------

OSX
^^^

::

   easy_install readline
   easy_install pycrypto
   pip install pip -U


::
   
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

  
