

Cloudmesh Client
==============================================================

Cloudmesh client is a simple client to enable access to multiple cloud
environments form a command shell and commandline. It is grown out of
the need to simplify access to multiple clouds for researchers and students
easily. In contrast to our earlier versions of cloudmesh it explicitly
separates the code to only target client code. Due to this simplification
it is also possible to install the client code not only on Linux, OSX, but
also Windows. We have tested the installation on Windows 10.

Automated Builds
----------------

+----------+-----------------+---------------+
| Master   | |master-status| | |master-docs| |
+----------+-----------------+---------------+
| Dev/VM   | |dev-status|    | |dev-docs|    |
+----------+-----------------+---------------+
| libcloud | |lib-status|    | |lib-docs|    |
+----------+-----------------+---------------+

Current TODO
-------------

* https://github.com/cloudmesh/client/blob/dev/TODO.md

Features
--------

* Heterogeneous cloud management

* Heterogeneous High Performance Computing (HPC) job management

* Supported clouds

  * OpenStack
  * Azure (not yet integrated, earlier versions of cloudmesh support it)
  * Amazon (not yet integrated, earlier versions of cloudmesh support it)
  * SDSC comet virtual clusters

* Supported Provider Templates

  * Futuesystems.org
  * chameleoncloud.org
  * SDSC Comet virtual clusters
  * Openstack (any general Openstack Cloud)
  * HP Chameleon
  * AWS  (not yet integrated, earlier versions of cloudmesh support it)
  * Azure (not yet integrated, earlier versions of cloudmesh support it)

* Heterogeneous Cloud Commandline client
* Heterogeneous Cloud Command Shell
* Heterogeneous Slurm Commandline client
* Heterogeneous Slurm Command Shell

* Integration with ~/.ssh/config

Status
-------

This project is under heavy development.

Links
------

The documentation to this project is located at

* http://cloudmesh.github.io/client

The source code is located at

*  https://github.com/cloudmesh/client

The travis build is found at

* https://travis-ci.org/cloudmesh/client



.. |dev-docs| image:: http://readthedocs.org/projects/cloudmesh-client/badge/?version=vm
   :target: http://cloudmesh-client.readthedocs.org/en/vm
   :alt: Documentation for unstable branch

.. |master-docs| image:: http://readthedocs.org/projects/cloudmesh-client/badge/?version=master
   :target: http://cloudmesh-client.readthedocs.org/en/master/
   :alt: Documentation for master branch

.. |master-status| image:: https://travis-ci.org/cloudmesh/client.svg?branch=master
    :target: https://travis-ci.org/cloudmesh/client

.. |dev-status| image:: https://travis-ci.org/cloudmesh/client.svg?branch=vm
    :target: https://travis-ci.org/cloudmesh/client

.. |lib-docs| image:: http://readthedocs.org/projects/cloudmesh-client/badge/?version=libcloud
   :target: http://cloudmesh-client.readthedocs.org/en/master/
   :alt: Documentation for master branch

.. |lib-status| image:: https://travis-ci.org/cloudmesh/client.svg?branch=libcloud
    :target: https://travis-ci.org/cloudmesh/client
