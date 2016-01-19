Cloudmesh Client Toolkit
============================================

The *cloudmesh client* toolkit is a lightweight client interface of accessing
heterogeneous clouds, clusters, and workstations right from the users computer.
The user can manage his own set of resources he would like to utilize. Thus
the user has the freedom to customize their cyber infrastructure they use.
Cloudmesh client includes an API, a commandline client, and a commandline shell.
It strives to abstract backends to databases that are used to manage the workflow
utilizing the different infrastructure and also the services. Switching for example
to stage virtual machines from openstack clouds to amazon is as simple as
specifying the name of the cloud. Moreover, cloudmesh client can be installed on
Linux, MacOSX, and even Windows. Currently we support backends to SLURM, SSH, Openstack,
Heat. In the past we supported AWS and Azure. We are in the process of integrating them
back into the client.


This documentation and code is available on github at:

* Documentation: http://cloudmesh.github.io/client/
* Code: https://github.com/cloudmesh/client

.. toctree::

   prefix


.. toctree::
   :caption: Installation

   system
   installation
   configuration

.. toctree::
   :caption: Manuals

   commands/index
   man/man

.. toctree::
   :caption: API

   api
   modules/modules

.. toctree::
   :caption: Appendix

   appendix


.. toctree::
   :caption: Future
   docker


.. toctree::
   :caption: Old

   old


.. toctree::
   :caption: Developers Manual
   :maxdepth: 4

   hacking

.. toctree::
   :caption: Code
   :maxdepth: 4

   code/cloudmesh_base/modules
   code/cloudmesh_client/modules

   code/cloudmesh_base	      
   code/cloudmesh_client

#.. toctree::
#   :caption: outdated
#   :maxdepth: 4

#   choco
#   cloudmesh_base
#   cloudmesh_client
#   commands_nova
#   commands_register
#   docker
#   man
#   old1
#   system-cygwin



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


