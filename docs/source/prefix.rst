Prefix
======

Cloudmesh client is a simple client to enable access to multiple cloud
environments form a command shell and commandline. It is grown out of
the need to simplify access to multiple clouds for researchers and
students easily. In contrast to our earlier versions of cloudmesh it
explicitly separates the code to only target client code. Due to this
simplification it is also possible to install the client code not only
on Linux, OSX, but also Windows. We have tested the installation on
Windows 10.

If you like to contribute or like to participate in the further
development, please contact Gregor von Laszewski at
laszewski@gmail.com.


Repositories
------------

* Documentation: http://cloudmesh.github.io/client  
* Code:

  * https://github.com/cloudmesh/base.git
  * https://github.com/cloudmesh/client.git

* Issues: https://github.com/cloudmesh/client/issues
* Milestones: https://github.com/cloudmesh/client/milestones
* Contributors: https://github.com/cloudmesh/client/graphs/contributors

As we have so far a tight integrated group, we are typically not
forking the repository, but cloning it directly. Members are than able
to work on the clones. We may change this in case we see need for forks.


Automated Builds and Reports
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Documentation: http://cloudmesh-client.readthedocs.org/
* Code: https://travis-ci.org/cloudmesh/client

Contact
-------

For more info please contact Gregor von Laszewski, laszewski@gmail.com
   
   `Gregor von Laszewski <http://gregor.cyberaide.org>`_ |br|
   E-mail: laszewski@gmail.comn  |br|
   Indiana University |br|
   School of Informatics and Computing |br|
   Informatics West |br|
   901 E. 10th St. |br|
   Bloomington, IN 47408 |br|

and my office is at 

   611 N. Park Ave. |br|
   Bloomington, IN 47408 |br|
   
   `Google Map <https://www.google.com/maps/place/611+N+Park+Ave,+Bloomington,+IN+47408/@39.1721978,-86.5248349,17z/data=!3m1!4b1!4m2!3m1!1s0x886c66c69d3f454f:0x14b53a197e1ac505>`_

.. |br| raw:: html

   <br />


Authors
-------

.. include:: ../../AUTHORS

Conventions
------------

We will be using some simple conventions in this documentation. To
indicate a command to be executed on the terminal we use `$` at the
beginning of the line:

.. prompt:: bash

	    echo "Hello World"


A command started in the cloudmesh client shell is preceded by `cm>`:

.. prompt:: bash, cm>

	    help

Often we are in the need to refer to a username or project. We will be
using the username `albert` and the project id `FG-101`. It will be up
to you to replace them with information related to your username and
project. Alternatively we assume that you have set the shell variables
$CM_USERNAME and $CM_PROJECT with for example:

.. prompt:: bash

	    export CM_USERNAME=albert
	    export CM_PROJECT=FG101

In this case we use in the documentation the values::

  $CM_PROJECT
  $CM_USERNAME

These values are typically set in the cloudmesh yaml file and if used
they can be read from it into variables within cloudmesh scripts:

.. prompt:: bash, cm>

	    var cloud=kilo
	    var username=cloudmesh.profile.username
	    var project=cloudmesh.clouds.$cloud.credentials.OS_TENANT_NAME

Please note that these values could be specific to a cloud as
indicated by the example for the project in the above project is
dependent on the specific cloud which can be easily integrated in the
cloudmesh variables while using a `$` followed by the variable name.


Feature Requests
-----------------

Please e-mail feature requests and bugs to laszewski@gmail.com.


We will manage them through github as part of issues and milestones:

* Issues: https://github.com/cloudmesh/client/issues
* Milestones: https://github.com/cloudmesh/client/milestones

Questions unrelated to cloudmesh but relate to futuresystems such as
network issues and outages are best send through the form at

* https://portal.futuresystems.org/help

