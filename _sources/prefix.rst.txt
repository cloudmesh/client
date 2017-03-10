Prefix
======

Cloudmesh client is a client to enable easy access to multiple cloud
environments form a command shell and commandline. It is grown out of
the need to access multiple clouds for researchers and students easily
while reducing the entry barrier. In contrast to our earlier versions
of cloudmesh it explicitly separates the code to only target client code.
Due to this simplification it is also possible to install the client code
not only on Linux, OSX, but also Windows. We have tested the installation on
Windows 10.

If you like to contribute or like to participate in the further
development, please contact Gregor von Laszewski at
laszewski@gmail.com.


Repository
------------

* Documentation: http://cloudmesh.github.io/client  
* Code:

  * https://github.com/cloudmesh/client.git
    
* Issues: https://github.com/cloudmesh/client/issues
* Milestones: https://github.com/cloudmesh/client/milestones
* Contributors: https://github.com/cloudmesh/client/graphs/contributors


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
   Informatics West
   901 E. 10th St. |br|
   Bloomington, IN 47408 |br|

and my office is at 

   Smith Research Center |br|
   2805 E. 10th St. |br|
   Bloomington, IN 47405 |br|

   `Google Map <https://www.google.com/maps/place/Smith+Research+Center/@39.1737049,-86.500201,15z/data=!4m5!3m4!1s0x0:0x5ed344c7b840ce57!8m2!3d39.1737049!4d-86.500201>`_

.. |br| raw:: html

   <br />


Authors
-------

.. include:: ../../AUTHORS
   
Conventions
------------

We use some simple conventions in this documentation. To
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

Please note that these values could be specific to a particular cloud. As
shown by the example for the project in the above project is
dependent on the specific cloud which can be easily integrated in the
cloudmesh variables while using a `$` followed by the variable name.


Feature Requests
-----------------

Please e-mail feature requests and bugs to laszewski@gmail.com.

We will manage them through github as part of issues and milestones:

* Issues: https://github.com/cloudmesh/client/issues
* Milestones: https://github.com/cloudmesh/client/milestones

Questions unrelated to cloudmesh but relate to futuresystems
are best send through the form at

* https://portal.futuresystems.org/help

