Register Command
======================================================================


The manual page of the register command can be found at: `register <../man/man.html#register>`_


As we are managing multiple clouds with cloudmesh we need to register
them first. To make it easy for you cloudmesh reads the registered
clouds from an easy to manage yaml file. This yam file is installed by
default into the file::

  %HOME/.cloudmesh/cloudmesh.yaml

A number of templates in that file exist that refer to commonly used
clouds. YOu can fill out the yaml file with your information, add new
clouds, or delete templates of clouds that you do not use. We have
several different typoes of clouds that we support. This includes
OpenStack, AWS, and Azure clouds.

.. todo:: at this time we have not integrated our AWS and Azure IaaS
	  abstractions. We will make them available in future.

As it may be inconvenient to edit this file and look at the yaml
format, we provide two administrative commands. The command::

  $ register info

  File C:\Users\erika\.cloudmesh\cloudmesh.yaml exists
  
identifies if the `cloudmesh.yaml` file exists.

To list the clouds that are defined in the cloudmesh.yaml file, you
can use the command::

  $ register list
  Clouds specified in the configuration file $HOME/.cloudmesh/cloudmesh.yaml

      india
      aws
      azure

.. todo:: Erica, we want a table here with print_dict and list in the
	  columns name, iaas (openastak, azure, ...), version (kilo,
	  n/a if None)
	  
+--------+-----------+---------+
| Name   | IaaS      | version |
+--------+-----------+---------+
| india  | openstack |  juno   |
| india  | openstack |  juno   |
+--------+-----------+---------+


register list ssh
^^^^^^^^^^^^^
Lists hosts from ~/.ssh/config::

    $ cm register list ssh
    The following hosts are defined in ~/.ssh/config

    india

register cat
^^^^^^^^^^^^^

register cat [--yaml=FILENAME]

Outputs the cloudmesh.yaml file::

    $ cm register cat

register edit
^^^^^^^^^^^^^

register edit [--yaml=FILENAME]

Edits the cloudmesh.yaml file::

    $ cm register edit
    editing file C:\Users\erika\.cloudmesh\cloudmesh.yaml

register rc HOST
^^^^^^^^^^^^^

register rc HOST

Reads the Openstack OPENRC file from a host that
is described in ./ssh/config and adds it to the
configuration cloudmesh.yaml file. We assume that
the file has already a template for this host. If
not it can be created from other examples before
you run this command.

The hostname can be specified as follows in the
./ssh/config file.

::

    Host india
        Hostname india.futuresystems.org
        User yourusername

If the host is india and the OPENRC file is
ommitted, it will automatically fill out the
location for the openrc file. To obtain the
information from india simply type in

register rc india::

    $ cm register rc india
    Reading rc file from india
    export OS_USERNAME=
    export OS_PASSWORD=
    export OS_TENANT_NAME=
    export OS_AUTH_URL=
    export OS_CACERT=



register merge FILEPATH
^^^^^^^^^^^^^

register merge

Replaces the TBD in cloudmesh.yaml with the contents present in FILEPATH's FILE::

    $ cm register merge ~/.cloudmesh/cloudmesh1.yaml
    Overwritten the TBD of cloudmesh.yaml with ~/.cloudmesh/cloudmesh1.yaml contents


register form
^^^^^^^^^^^^^

register form [--yaml=FILENAME]

Interactively fills out the form wherever we find TBD::

    $ cm register form --yaml=cloudmesh1.yaml
    Filling out form
    C:\Users\erika\.cloudmesh\cloudmesh1.yaml
    Please enter email[TBD]:
    Editing the credentials for cloud india
    Please enter OS_TENANT_NAME[TBD]:
    Editing the credentials for cloud aws
    Please enter EC2_ACCESS_KEY[TBD]:
    Please enter EC2_SECRET_KEY[TBD]:
    Please enter keyname[TBD]:
    Please enter userid[TBD]:
    Editing the credentials for cloud azure
    Please enter managementcertfile[TBD]:
    Please enter servicecertfile[TBD]:
    Please enter subscriptionid[TBD]:
    Please enter thumbprint[TBD]:

register check [--yaml=FILENAME]
^^^^^^^^^^^^^

register check

Checks the yaml file for completness::

    $ cm register check
    Checking the yaml file
    ERROR: The file has 11 values to be fixed

      email: TBD
      username: TBD
      flavor: TBD
      EC2_ACCESS_KEY: TBD
      EC2_SECRET_KEY: TBD
      keyname: TBD
      userid: TBD
      managementcertfile: TBD
      servicecertfile: TBD
      subscriptionid: TBD
      thumbprint: TBD

register json HOST
^^^^^^^^^^^^^

register json

Displays the host details in json format::

    $ cm register json azure
    {
        "cm_heading": "Microsoft Azure Virtual Machines",
        "cm_label": "waz",
        "cm_host": "windowsazure.com",
        "default": {
            "flavor": "ExtraSmall",
            "image": "b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_2-LTS-amd64-server-20150610-en-us-30GB",
            "location": "East US"
        },
        "credentials": {
            "managementcertfile": "TBD",
            "servicecertfile": "TBD",
            "subscriptionid": "TBD",
            "thumbprint": "TBD"
        },
        "cm_type": "azure",
        "cm_type_version": null
    }

register india
^^^^^^^^^^^^^

register india [--force]

Copies the cloudmesh/clouds/india/juno directory from india to the ~/.cloudmesh/clouds/india/juno local directory::

    $ cm register india
    register india
    Directory already exists. Would you like to overwrite the ~/.cloudmesh/clouds/india directory y/n?  (Y/n) y
    fetching information from india ...
    Enter passphrase for key '/C/Users/erika/.ssh/id_rsa':
    registration complete. ok.

register CLOUD
^^^^^^^^^^^^^

from cert
~~~~~~~~~~~

register CLOUD CERT [--force]


Copies the CERT to the ~/.cloudmesh/clouds/host directory and registers that cert in the coudmesh.yaml file.
For india, CERT will be in india:.cloudmesh/clouds/india/juno/cacert.pem and would be copied to ~/.cloudmesh/clouds/india/juno::

    $ cm register india ~/.cloudmesh/clouds/india/juno/cacert.pem
    register
    Fetching certificate from india...
    Enter passphrase for key '/C/Users/erika/.ssh/id_rsa':
    certificate fetched. ok
    registering cert in cloudmesh.yaml file
    cert registered in cloudmesh.yaml file.
    Clouds specified in the configuration file C:\Users\erika\.cloudmesh\cloudmesh.yaml

      india
      aws
      azure

from dir
~~~~~~~~~~~

register CLOUD --dir

Copies the entire directory from the cloud and puts it in ~/.cloudmesh/clouds/host
For india, The directory would be copied to ~/.cloudmesh/clouds/india::

    $ cm register india --dir=~/.cloudmesh/clouds/india/juno
    ~/.cloudmesh/clouds/india/juno
    register
    Fetching directory...
    Enter passphrase for key '/C/Users/erika/.ssh/id_rsa':
    Directory fetched
    Clouds specified in the configuration file C:\Users\erika\.cloudmesh\cloudmesh.yaml

      india
      aws
      azure

