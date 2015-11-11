Configuration
=============

.. todo:: implement

First you need to initialize cloudmesh by invoking the command:

::

   cm

This will create for you a default configuration file::
   
   ~/.cloudmesh/cloudmesh.yaml

The file will be looking as follows. You will have several options to
modify the file as explained bellow

.. literalinclude:: ../../cloudmesh_client/etc/cloudmesh.yaml

You can modify the file by hand and replace the ``TBD`` values
according to your information about your cloud. YOu can add new clouds
or delete the once that you do not want.

.. warning:: please make sure the file is protected as it contains
	     sensitive information.


Get Registration from India
----------------------------

In case you have an account on http::/portal.futuresystems.org the
integration can be done automatically for you with the account
information available to you. The best way is to configure first your
ssh client to conveniently log into india the machine where you can
find the configuration information. To do so, please edit the
following file 

::

   ~/./ssh/config

and add the following lines to it

::

   Host india
       User: albert
       Hostname: india.futuresystems.org

please replace albert with your portalname that you have used for
registration with futuresystems.org. Once you have done this please
verify that you have access to india with a command such as::

  ssh india uname -a

Next register the FutureSystems clouds into your cloudmesh yaml file with
the command::

   cm register remote juno
   cm register remote kilo

This will update your cloudmesh.yaml file with the information retrieved
from india. While retrieving the information on india from the file::

  ~/.cloudmesh/clouds/india/juno/openrc.sh

Make sure you add a valid tenant to the yaml file. More information
about using india can be found at http://portal.futuresystems.org


Registration of clouds
-----------------------

The register command is quite powerful and useful and we encourage you to
take a closer look at the manual pages. This includes command such as

::

   cm register help

::

   register edit

::

   register list



