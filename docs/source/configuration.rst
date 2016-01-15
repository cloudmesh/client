Configuration
=============

During the installation of cloudmesh it will automatically generate
a configuration file in the directory:

   ~/.cloudmesh/cloudmesh.yaml

If this file is missing, you can run the command:

    cm help to automatically generate it from defaults.

The file will be a template and it can either be modified with your
favourite editor, or if you are at indiana university and want to use the
kilo cloud you can use the command

    cm remote register

This will add the appropriate information into the yaml file.
The file will be looking as follows.
You will have several options to
modify the file as explained bellow

.. literalinclude:: ../../cloudmesh_client/etc/cloudmesh.yaml

You can modify the file by hand and replace the ``TBD`` values
according to your information about your cloud. You can add new clouds
or delete the once that you do not want.

.. warning:: Just as private keys should be kept private so does
             the cloudmesh.yaml
             file. Please, make sure the file is protected as it contains
	         sensitive information.


Get Registration from Indiana University
----------------------------------------

In case you have an account on http::/portal.futuresystems.org the
integration can be done automatically for you with the account
information available to you as previously explained.


The best way is to configure first your ssh client to conveniently log into india the machine where you can
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

   cm register remote

This will update your cloudmesh.yaml file with the information retrieved
from india. While retrieving the information on india from the file::

  ~/.cloudmesh/clouds/india/kilo/openrc.sh
  ~/.cloudmesh/clouds/india/juno/openrc.sh

Make sure you add a valid tenant to the yaml file. More information
about using india can be found at http://portal.futuresystems.org


Registration of clouds
-----------------------

The register command is quite powerful and useful and we encourage you to
take a closer look at the manual pages. This includes command such as

To find out more about the registration command::

   cm register help

To edit the yaml file with the edior defined by the Shell variable `$EDITOR`::

   register edit

To list the `cloudmesh.yaml` file::

   register list



