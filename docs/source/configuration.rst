Configuration
=============

.. todo:: implement

First you need to initialize cloudmesh by invoking the command:

::

   cm init

This will create for you a default configuration file::
   
   ~/.cloudmesh/cloudmesh.yaml

The file will be looking as follows. You will have several options to
modify the file as explained bellow

.. literalinclude:: ../../etc/cloudmesh.yaml

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
ssh client to conveniently log into india the machine wher eyou can
find the configuration information. To do so, please edit the
following file 

::

   ~/./ssh/config

and add the following lines to it

::

   Host india
       User: gregor
       Hostname: india.futuresystems.org

please replace gregor with your portalname that you have used for
registration with futuresystems.org. Once you have done this please
verify that you have access to india with a command such as::

  ssh india uname -a

Next register india into your cloudmesh yaml file with the command::  

   cm register india

This will update your cloudmesh.yaml file with the information retrieved
from india. While retriving the information on india from the file::

  ~/.cloudmesh/clouds/india/juno/openrc.sh

Make sure you add a valid tennat to the yaml file. More information
about using india can be found at http://portal.futuresystems.org


Registration of clouds
-----------------------

See manual page ...

::

   cm register help

::

   register edit

::

   register list



