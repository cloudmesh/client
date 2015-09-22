Register Command
======================================================================


Manual
--------
The manual page of the register command can be found at: `register <../man/man.html#register>`_


Examples
--------

register info
^^^^^^^^^^^^^

It looks out for the cloudmesh.yaml file in the current directory, and then in ~/.cloudmesh::

  PS> cm register info
    File C:\Users\erika\.cloudmesh\cloudmesh.yaml exists



register list [--yaml=FILENAME]
^^^^^^^^^^^^^
Lists the clouds specified in the cloudmesh.yaml file::

    PS> cm register list
    Clouds specified in the configuration file C:\Users\erika\.cloudmesh\cloudmesh.yaml

      india
      aws
      azure

register list ssh
^^^^^^^^^^^^^
Lists hosts from ~/.ssh/config::

    PS> cm register list ssh
    The following hosts are defined in ~/.ssh/config

    india

register cat [--yaml=FILENAME]
^^^^^^^^^^^^^
Outputs the cloudmesh.yaml file::

    PS> cm register cat

register edit [--yaml=FILENAME]
^^^^^^^^^^^^^
Edits the cloudmesh.yaml file::

    PS> cm register edit
    editing file C:\Users\erika\.cloudmesh\cloudmesh.yaml

register rc HOST [OPENRC]
^^^^^^^^^^^^^
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

    PS> cm register rc india
    Reading rc file from india
    export OS_USERNAME=
    export OS_PASSWORD=
    export OS_TENANT_NAME=
    export OS_AUTH_URL=
    export OS_CACERT=



register merge FILEPATH
^^^^^^^^^^^^^
Replaces the TBD in cloudmesh.yaml with the contents present in FILEPATH's FILE::

    PS> cm register merge ~/.cloudmesh/cloudmesh1.yaml
    Overwritten the TBD of cloudmesh.yaml with ~/.cloudmesh/cloudmesh1.yaml contents


register form [--yaml=FILENAME]
^^^^^^^^^^^^^
Interactively fills out the form wherever we find TBD::

    PS> cm register form --yaml=cloudmesh1.yaml
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
Checks the yaml file for completness::

    PS> cm register check
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
Displays the host details in json format::

    PS> cm register json azure
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

register india [--force]
^^^^^^^^^^^^^
Copies the cloudmesh/clouds/india/juno directory from india to the ~/.cloudmesh/clouds/india/juno local directory::

    PS> cm register india
    register india
    Directory already exists. Would you like to overwrite the ~/.cloudmesh/clouds/india directory y/n?  (Y/n) y
    fetching information from india ...
    Enter passphrase for key '/C/Users/erika/.ssh/id_rsa':
    registration complete. ok.

register CLOUD CERT [--force]
^^^^^^^^^^^^^
Copies the CERT to the ~/.cloudmesh/clouds/host directory and registers that cert in the coudmesh.yaml file.
For india, CERT will be in india:.cloudmesh/clouds/india/juno/cacert.pem and would be copied to ~/.cloudmesh/clouds/india/juno::

    PS> cm register india ~/.cloudmesh/clouds/india/juno/cacert.pem
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

register CLOUD --dir
^^^^^^^^^^^^^
Copies the entire directory from the cloud and puts it in ~/.cloudmesh/clouds/host
For india, The directory would be copied to ~/.cloudmesh/clouds/india::

    PS> cm register india --dir=~/.cloudmesh/clouds/india/juno
    ~/.cloudmesh/clouds/india/juno
    register
    Fetching directory...
    Enter passphrase for key '/C/Users/erika/.ssh/id_rsa':
    Directory fetched
    Clouds specified in the configuration file C:\Users\erika\.cloudmesh\cloudmesh.yaml

      india
      aws
      azure

