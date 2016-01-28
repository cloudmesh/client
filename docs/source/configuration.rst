Configuration
=============

During the installation of cloudmesh it will automatically generate
a configuration file in the directory:

   ~/.cloudmesh/cloudmesh.yaml

If this file is missing, you can run the command:

    cm help to automatically generate it from defaults.

The file will be a template and it can either be modified with your
favorite editor, or if you are at Indiana University and want to use the
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

please replace albert with your portal name that you have used for
registration with futuresystems.org. Once you have done this please
verify that you have access to india with a command such as::

  ssh india uname -a

Next register the FutureSystems clouds into your cloudmesh yaml file with
the command::

   cm register remote

This will update your cloudmesh.yaml file with the information retrieved
from india. While retrieving the information on india from the file::

  ~/.cloudmesh/clouds/india/kilo/openrc.sh

Make sure you add a valid tenant to the yaml file. More information
about using india can be found at http://portal.futuresystems.org


Registration of other clouds
-----------------------------

The register command is quite powerful and useful and we encourage you to
take a closer look at the manual pages. This includes command such as

To find out more about the registration command::

   cm register help

To edit the yaml file with the editor defined by the Shell variable `$EDITOR`::

   register edit

To list the `cloudmesh.yaml` file::

   register list

Registration of Cybera Cloud
-------------------------------

Cybera an organization from Canada provides an easy accessible
openstack cloud. This cloud should only be used while following their
access policies documented at:

* http://www.cybera.ca/projects/cloud-resources/rapid-access-cloud/faq/#What_is_RAC

YOu may ask for permission, if you do not fit this category. Once you
have created an account at:

* https://rac-portal.cybera.ca/

YOu can access to Openstack portal at

* https://cloud.cybera.ca/auth/login/

Just as Chameleon Cloud the Cybera cloud allows openstack rc and ec2
rc files.

Registration of Cybera Openstack Cloud
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you have an account ana a project it is simple to configure
cloudmesh to include chameleon cloud in its resource set. To do so,
edit the file:

   ~/.cloudmesh/cloudmesh.yaml

Edit the follwoing lines::

                OS_PASSWORD: TBD
                OS_TENANT_NAME: TBD
                OS_TENANT_ID: TBD
                OS_PROJECT_NAME: TBD
                OS_USERNAME: TBD

Let us assume you have the username `albert` and the project id
`FG-101`, Than the lines need to be changed to::

                OS_PASSWORD: <your user password>
                OS_TENANT_NAME: FG-101
                OS_TENANT_ID: FG-101
                OS_PROJECT_NAME: FG-101
                OS_USERNAME: albert


You can find this information also in the openrc.sh file which you can
download via the Openstack Horizon interface by following this link:

* https://cloud.cybera.ca/project/access_and_security/api_access/openrc/

Registration of Cybera EC2 Cloud
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cybera cloud also support the usage of the EC2 interface which
is a pit more complex to set up than the openstack configuration.
First, you have to download a configuration directory, that is
packaged as a zip file. This file can be found at

* https://cloud.cybera.ca/project/access_and_security/api_access/ec2/

Let us assume you have the username albert and
the project FG-101. Than the zip file will be called::

  FG-101-x509.zip

Let us set some environment variables to make the configuration
description easier

.. prompt:: bash

   export C_USERNAME=<your cybera username>
   export C_PROJECT=<your cybera project name>
  
Unpack the zip file and place the entire directory in the .cloudmesh
directory with. (We assume that you are in the directory where your
browser downloaded the zip file and you have uncompressed it)

.. prompt:: bash

	    mkdir ~/.cloudmesh/clouds/cybera/$C_PROJECT
	    cp $C_PROJECT ~/.cloudmesh/clouds/cybera/$C_PROJECT
	    ls ~/.cloudmesh/clouds/cybera/$C_PROJECT

The directory should include the files::

  cacert.pem
  cert.pem
  ec2rc.sh
  pk.pem

Take a look at the ec2rc.sh file

.. prompt:: bash

	    cat ~/.cloudmesh/clouds/cybera/$C_PROJECT/ec2rc.sh
	    
Now you can edit the cloudmesh yaml file at::

   ~/.cloudmesh/cloudmesh.yaml

locate the cybera-ec2 entry and change the TBD values with the
values you see in the ec2rc.sh file::

  EC2_ACCESS_KEY: <find the value in the ec2rc.sh file>
  EC2_SECRET_KEY: <find the value in the ec2rc.sh file>
  EC2_USER_ID: <find the value in the ec2rc.sh file>

For the following lines in the cloudmesh file, please replace the TBD
values with the cybera project ID that you use for this cloud::
  
  EC2_PRIVATE_KEY: ~/.cloudmesh/clouds/cybera/TBD/pk.pem
  EC2_CERT: ~/.cloudmesh/clouds/cybera/TBD/cert.pem
  NOVA_CERT: ~/.cloudmesh/clouds/cybera/TBD/cacert.pem
  EUCALYPTUS_CERT: ~/.cloudmesh/clouds/cybera/TBD/cacert.pem



  
Chameleon Cloud
----------------
  
Registration of Chameleon Openstack Cloud
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

NSF sponsors an experimental cloud environment called Chameleon at

* https://www.chameleoncloud.org

It is a KVM based Openstack cloud of version kilo. The documentation
can be found here:

* https://www.chameleoncloud.org/docs/user-guides/openstack-kvm-user-guide/

When you have an account and a project it is simple to configure
cloudmesh to include chameleon cloud in its resource set. To do so,
edit the file:

   ~/.cloudmesh/cloudmesh.yaml

Edit the follwoing lines::

                OS_PASSWORD: TBD
                OS_TENANT_NAME: TBD
                OS_TENANT_ID: TBD
                OS_PROJECT_NAME: TBD
                OS_USERNAME: TBD

Let us assume you have the username `albert` and the project id
`FG-101`, Than the lines need to be changed to::

                OS_PASSWORD: <your user password>
                OS_TENANT_NAME: FG-101
                OS_TENANT_ID: FG-101
                OS_PROJECT_NAME: FG-101
                OS_USERNAME: albert


You can find this information also in the openrc.sh file which you can
download via the Openstack Horizon interface by following this link:

* https://openstack.tacc.chameleoncloud.org/dashboard/project/access_and_security/api_access/openrc/


Registration of Chameleon EC2 Cloud
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The chameleon cloud also support the usage of the EC2 interface which
is a pit more complex to set up than the openstack configuration.
First, you have to download a configuration directory, that is
packaged as a zip file. This file can be found at

* https://openstack.tacc.chameleoncloud.org/dashboard/project/access_and_security/api_access/ec2/

Let us assume you have the username albert and
the project FG-101. Than the zip file will be called::

  FG-101-x509.zip

Let us set some environment variables to make the configuration
description easier

.. prompt:: bash

   export C_USERNAME=<your chameleon username>
   export C_PROJECT=<your chameleon project name>
  
Unpack the zip file and place the entire directory in the .cloudmesh
directory with. (We assume that you are in the directory where your
browser downloaded the zip file and you have uncompressed it)

.. prompt:: bash

	    mkdir ~/.cloudmesh/clouds/chameleon/$C_PROJECT
	    cp $C_PROJECT ~/.cloudmesh/clouds/chameleon/$C_PROJECT
	    ls ~/.cloudmesh/clouds/chameleon/$C_PROJECT

The directory should include the files::

  cacert.pem
  cert.pem
  ec2rc.sh
  pk.pem

Take a look at the ec2rc.sh file

.. prompt:: bash

	    cat ~/.cloudmesh/clouds/chameleon/$C_PROJECT/ec2rc.sh
	    
Now you can edit the cloudmesh yaml file at::

   ~/.cloudmesh/cloudmesh.yaml

locate the chameleon-ec2 entry and change the TBD values with the
values you see in the ec2rc.sh file::

  EC2_ACCESS_KEY: <find the value in the ec2rc.sh file>
  EC2_SECRET_KEY: <find the value in the ec2rc.sh file>
  EC2_USER_ID: <find the value in the ec2rc.sh file>

For the following lines in the cloudmesh file, please replace the TBD
values with the chameleon project ID that you use for this cloud::
  
  EC2_PRIVATE_KEY: ~/.cloudmesh/clouds/chameleon/TBD/pk.pem
  EC2_CERT: ~/.cloudmesh/clouds/chameleon/TBD/cert.pem
  NOVA_CERT: ~/.cloudmesh/clouds/chameleon/TBD/cacert.pem
  EUCALYPTUS_CERT: ~/.cloudmesh/clouds/chameleon/TBD/cacert.pem



Registration of CloudLab Openstack Cloud
--------------------------------------

.. todo:: not yet tested but should work. add cloud registration here

Registration of AWS Cloud
--------------------------------------

.. todo:: not yet supported but used to be so we work on it ASAP. add cloud registration here

Registration of Azure Cloud
--------------------------------------

.. todo:: not yet supported but used to be so we work on it ASAP. add cloud registration here

Registration of devcloud
--------------------------------------

.. todo:: not tested, but should work as is regular openstack. add cloud registration here

Registration of a libcloud available cloud
--------------------------------------

.. todo:: not yet supported. add cloud registration here

